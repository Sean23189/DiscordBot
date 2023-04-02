import requests
import lightbulb

# Create a new plugin instance with the name "get"
plugin = lightbulb.Plugin("get")

# Define a function that returns a random quote from the ZenQuotes API
def get_quote() -> str:
    # Send a GET request to the ZenQuotes API with a timeout of 5 seconds
    response = requests.get("https://zenquotes.io/api/random", timeout=5)
    # Parse the JSON response data
    json_data = response.json()
    # Extract the quote and author information from the JSON data and format it
    quote = json_data[0]['q'] + "\n-" + json_data[0]['a']
    # Return the formatted quote
    return quote

# Define a function that returns a URL for a random cat image from TheCatAPI
def get_cat() -> str:
    # Send a GET request to TheCatAPI with a timeout of 5 seconds
    response = requests.get("https://api.thecatapi.com/v1/images/search", timeout=5)
    # Parse the JSON response data
    json_data = response.json()
    # Extract the URL for the first image in the response data
    cat_url = json_data[0]['url']
    # Return the URL
    return cat_url

# Define a command for the "get" plugin
@plugin.command
# Define an option for the "get" command with the name "get"
@lightbulb.option("get", "get")
# Define the "get" command with a short description
@lightbulb.command("get", "get anything you like")
# Implement the SlashCommand interface for the "get" command
@lightbulb.implements(lightbulb.SlashCommand)
async def get_cmd(ctx: lightbulb.Context):
    # Check the value of the "get" option provided by the user
    if ctx.options.get == "cat":
        # If the value is "cat", call the "get_cat" function and respond with the URL
        cat_url = get_cat()
        await ctx.respond(content=cat_url)
    elif ctx.options.get == "quote":
        # If the value is "quote", call the "get_quote" function and respond with the quote
        quote = get_quote()
        await ctx.respond(content=quote)
    elif ctx.options.get == "username":
        # If the value is "username", format the username of the user who sent the command and respond with it
        username = f"{ctx.author.username}#{ctx.author.discriminator}"
        await ctx.respond(content=username)

# Define a function to load the "get" plugin into a Lightbulb bot
def load(bot):
    bot.add_plugin(plugin)
