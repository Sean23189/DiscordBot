import os
import asyncio
import aiohttp
import wolframalpha
import lightbulb

GOOGLEAPIKEY = os.getenv('GOOGLEAPIKEY')
CUSTOMSEARCHENGINEID = os.getenv('CUSTOMSEARCHENGINEID')
WOLFRAMAPIKEY = os.getenv('WOLFRAMAPIKEY')
RAPIDAPIKEY = os.getenv('RAPIDAPIKEY')

plugin = lightbulb.Plugin('ask')

async def call_wolfram_api(query):
    client = wolframalpha.Client(WOLFRAMAPIKEY)
    try:
        result = await asyncio.wait_for(client.query(query), timeout=10)
        response = next(result.results).text
        return response
    except StopIteration:
        return "No results found."
    except Exception as _:
        return "Error occurred during Wolfram Alpha API call."

async def get_top_result(query: str):
    url = (
        f'https://www.googleapis.com/customsearch/v1'
        f'?key={GOOGLEAPIKEY}&cx={CUSTOMSEARCHENGINEID}'
        f'&q={query}'
    )

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                json_data = await response.json()
                if 'items' in json_data and len(json_data['items']) > 0:
                    return json_data['items'][0]['title'] + '\n' + json_data['items'][0]['link']
                else:
                    return "No results found."
        except aiohttp.ClientError as _:
            return "Error occurred during Google API call."

async def get_urban_dictionary_results(query):
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    headers = {
        "X-RapidAPI-Key": RAPIDAPIKEY,
        "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
    }
    params = {"term": query}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                data = await response.json()
                if 'list' in data and len(data['list']) > 0:
                    first_result = data['list'][0]
                    definition = (
                        first_result['definition']
                        .replace("[", "")
                        .replace("]", "")
                        .strip()
                    )
                    example = (
                        first_result['example']
                        .replace("[", "")
                        .replace("]", "")
                        .strip()
                    )
                    return definition, example
        except aiohttp.ClientError as _:
            pass

    return None, None

async def fetch_results(query):
    wolfram_response = await call_wolfram_api(query)
    tasks = [
        get_top_result(query),
        get_urban_dictionary_results(query),
    ]
    try:
        results = await asyncio.gather(*tasks)
        google_result, (urban_definition, urban_example) = results
    except Exception as _:
        raise RuntimeError("An error occurred during API requests.")

    return wolfram_response, google_result, urban_definition, urban_example

@plugin.command
@lightbulb.option('query', 'search query', type=str)
@lightbulb.command('ask', 'Ask about anything', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def ask_cmd(ctx: lightbulb.Context):
    query = ctx.options.query
    if not query:
        await ctx.respond(content="Please provide a search query.")
        return

    try:
        results = await asyncio.wait_for(fetch_results(query), timeout=10)
        wolfram_response, google_result, urban_definition, urban_example = results
    except asyncio.TimeoutError:
        await ctx.respond(content="API request timed out.")
        return
    except RuntimeError as error:
        await ctx.respond(content=str(error))
        return
    except Exception as _:
        await ctx.respond(content="An unexpected error occurred.")
        return

    message = f"Here are your results using the query '{query}':\n\n"
    message += f"**WolframAlpha:**\n{wolfram_response}\n\n"
    message += f"**Google:**\n{google_result}\n\n"

    if urban_definition and urban_example:
        message += (
            f"**Urban Dictionary:**\n"
            f"Definition: {urban_definition}\n"
            f"Example: {urban_example}"
        )
    else:
        message += "**Urban Dictionary:**\nNo definition found."

    if len(message) <= 2000:
        await ctx.respond(content=message)
    else:
        await ctx.respond(content="The response message exceeds the character limit.")

def load(bot):
    bot.add_plugin(plugin)

loop = asyncio.get_event_loop()
