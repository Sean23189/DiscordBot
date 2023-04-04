import random
import requests
import hikari
import lightbulb

plugin = lightbulb.Plugin('get')

def get_quote() -> str:
    response = requests.get('https://zenquotes.io/api/random', timeout=5)
    json_data = response.json()
    quote = json_data[0]['q'] + '\n-' + json_data[0]['a']
    return quote

def get_cat() -> str:
    response = requests.get('https://api.thecatapi.com/v1/images/search', timeout=5)
    json_data = response.json()
    cat_url = json_data[0]['url']
    return cat_url

@plugin.command
@lightbulb.option('get', 'get')
@lightbulb.command('get', 'get anything you like')
@lightbulb.implements(lightbulb.SlashCommand)
async def get_cmd(ctx: lightbulb.Context):
    if ctx.options.get == 'cat':
        hex_color = random.randint(0, 0xFFFFFF)
        embed = hikari.Embed(title="Here is your cat!", color=hex_color)
        cat_url = get_cat()
        embed.set_image(cat_url)
        await ctx.respond(embed)
    elif ctx.options.get == 'quote':
        quote = get_quote()
        await ctx.respond(content=quote)
    elif ctx.options.get == 'username':
        username = f'{ctx.author.username}#{ctx.author.discriminator}'
        await ctx.respond(content=username)

def load(bot):
    bot.add_plugin(plugin)
