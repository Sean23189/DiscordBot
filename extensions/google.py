import os
import requests
import lightbulb

# get API key and custom search engine ID from environment variables
API_KEY = os.getenv("GOOGLEAPIKEY")
CX = os.getenv("CUSTOMSEARCHENGINEID")

# create a new Lightbulb plugin for the Google search command
plugin = lightbulb.Plugin("google")

# function that takes a search query and returns the top search result
def get_top_result(query: str) -> str:
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={query}"
    # add timeout of 5 seconds to requests.get to prevent the program from hanging indefinitely
    response = requests.get(url, timeout=5)
    json_data = response.json()
    top_result = json_data['items'][0]['title'] + "\n" + json_data['items'][0]['link']
    return top_result

# define a Lightbulb command that takes a search query and responds with the top search result
@plugin.command
@lightbulb.option("query", "search query", type=str)
@lightbulb.command("google", "search for anything on google")
@lightbulb.implements(lightbulb.SlashCommand)
async def google_cmd(ctx: lightbulb.Context):
    query = ctx.options.query
    top_result = get_top_result(query)
    await ctx.respond(content=top_result)

# define a function that loads the plugin into the bot
def load(bot):
    bot.add_plugin(plugin)
