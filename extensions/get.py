import random
import requests
import hikari
import lightbulb

# Define a Lightbulb plugin named 'get'
plugin = lightbulb.Plugin('get')

# Define a function to retrieve a random quote using the ZenQuotes API
def get_quote() -> str:
    response = requests.get('https://zenquotes.io/api/random', timeout=5)
    json_data = response.json()
    quote = json_data[0]['q'] + '\n-' + json_data[0]['a']
    return quote

# Define a function to retrieve a random cat image URL using the TheCatAPI
def get_cat() -> str:
    response = requests.get('https://api.thecatapi.com/v1/images/search', timeout=5)
    json_data = response.json()
    cat_url = json_data[0]['url']
    return cat_url

# Define a Lightbulb command that allows users to get a random cat image, quote, or their own username
@plugin.command
@lightbulb.option('get', 'get')
@lightbulb.command('get', 'get anything you like')
@lightbulb.implements(lightbulb.SlashCommand)
async def get_cmd(ctx: lightbulb.Context):
    # If the user requested a cat image, generate an embed with a random hex color and the image
    if ctx.options.get == 'cat':
        hex_color = random.randint(0, 0xFFFFFF)
        embed = hikari.Embed(title="Here is your cat!", color=hex_color)
        cat_url = get_cat()
        embed.set_image(cat_url)
        await ctx.respond(embed)
    # If the user requested a quote, retrieve one using the ZenQuotes API and send it as a message
    elif ctx.options.get == 'quote':
        quote = get_quote()
        await ctx.respond(content=quote)
    # If the user requested their own username, send it as a message
    elif ctx.options.get == 'username':
        username = f'{ctx.author.username}#{ctx.author.discriminator}'
        await ctx.respond(content=username)

# Define a function to load the plugin into the bot
def load(bot):
    bot.add_plugin(plugin)
