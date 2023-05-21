import os
import aiohttp
import asyncio
import json
import wolframalpha
import lightbulb

API_KEYS = {
    'GOOGLEAPIKEY': os.getenv('GOOGLEAPIKEY'),
    'CUSTOMSEARCHENGINEID': os.getenv('CUSTOMSEARCHENGINEID'),
    'WOLFRAMAPIKEY': os.getenv('WOLFRAMAPIKEY'),
    'RAPIDAPIKEY': os.getenv('RAPIDAPIKEY'),
}

plugin = lightbulb.Plugin('ask')


# Function to create a Wolfram Alpha API client
def get_wolfram_api_client():
    return wolframalpha.Client(API_KEYS['WOLFRAMAPIKEY'])


# Function to make a call to the Wolfram Alpha API
async def call_wolfram_api(query):
    client = get_wolfram_api_client()
    try:
        result = await loop.run_in_executor(None, client.query, query)
        return next(result.results).text
    except StopIteration:
        return "No results found."
    except Exception as e:
        return f"Error occurred during Wolfram Alpha API call: {str(e)}"


# Function to get the top search result from Google Custom Search API
async def get_top_result(query: str):
    url = f'https://www.googleapis.com/customsearch/v1?key={API_KEYS["GOOGLEAPIKEY"]}&cx={API_KEYS["CUSTOMSEARCHENGINEID"]}&q={query}'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as response:
                json_data = await response.json()
                if 'items' in json_data and len(json_data['items']) > 0:
                    return json_data['items'][0]['title'] + '\n' + json_data['items'][0]['link']
                else:
                    return "No results found."
        except aiohttp.ClientError as e:
            return f"Error occurred during Google API call: {str(e)}"


# Function to get the definition and example from Urban Dictionary API
async def get_urban_dictionary_results(query):
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    headers = {
        "X-RapidAPI-Key": API_KEYS["RAPIDAPIKEY"],
        "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
    }
    params = {"term": query}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                data = await response.json()
                if 'list' in data and len(data['list']) > 0:
                    first_result = data['list'][0]
                    definition = first_result['definition'].replace("[", "").replace("]", "").strip()
                    example = first_result['example'].replace("[", "").replace("]", "").strip()
                    return definition, example
        except aiohttp.ClientError as e:
            print(f"Error occurred during Urban Dictionary API call: {str(e)}")

    return None, None


# Function to fetch results from Wolfram Alpha, Google, and Urban Dictionary APIs
async def fetch_results(query):
    tasks = [
        call_wolfram_api(query),
        get_top_result(query),
        get_urban_dictionary_results(query),
    ]
    try:
        results = await asyncio.gather(*tasks)
        wolfram_response, google_result, (urban_definition, urban_example) = results
        return wolfram_response, google_result, urban_definition, urban_example
    except Exception as e:
        print(f"Error occurred during API calls: {str(e)}")

    return None, None, None, None


# Command to ask a question and fetch results
@plugin.command
@lightbulb.option('query', 'search query', type=str)
@lightbulb.command('ask', 'Ask about anything')
@lightbulb.implements(lightbulb.SlashCommand)
async def ask_cmd(ctx: lightbulb.Context):
    query = ctx.options.query
    if not query:
        await ctx.respond(content="Please provide a search query.")
        return

    wolfram_response, google_result, urban_definition, urban_example = await fetch_results(query)

    if wolfram_response is None or google_result is None:
        await ctx.respond(content="An error occurred during API calls.")
        return

    message = f"Here are your results using the query '{query}':\n\n"

    message += f"**WolframAlpha:**\n{wolfram_response}\n\n"
    message += f"**Google:**\n{google_result}\n\n"

    if urban_definition and urban_example:
        message += f"**Urban Dictionary:**\nDefinition: {urban_definition}\nExample: {urban_example}"
    else:
        message += "**Urban Dictionary:**\nNo definition found."

    if len(message) <= 2000:
        await ctx.respond(content=message)
    else:
        await ctx.respond(content="The response message exceeds the character limit.")


# Function to load the plugin
def load(bot):
    bot.add_plugin(plugin)


loop = asyncio.get_event_loop()

