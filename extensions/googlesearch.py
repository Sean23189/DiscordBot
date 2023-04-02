import requests
import lightbulb
import os

API_KEY = os.getenv("GOOGLEAPIKEY")
CX = os.getenv("CUSTOMSEARCHENGINEID")

plugin = lightbulb.Plugin("google")


def get_top_result(query: str) -> str:
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={query}"
    response = requests.get(url)
    json_data = response.json()
    top_result = json_data['items'][0]['title'] + "\n" + json_data['items'][0]['link']
    return top_result


@plugin.command
@lightbulb.option("query", "search query", type=str)
@lightbulb.command("google", "search for anything on google")
@lightbulb.implements(lightbulb.SlashCommand)
async def google_cmd(ctx: lightbulb.Context):
    query = ctx.options.query
    top_result = get_top_result(query)
    await ctx.respond(content=top_result)

def load(bot):
    bot.add_plugin(plugin)
