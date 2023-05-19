import wolframalpha  # Import the wolframalpha library
import os  # Import the os module for accessing environment variables
import lightbulb  # Import the lightbulb library for creating Commands


plugin = lightbulb.Plugin('wolfram')  # Create a new plugin instance named 'wolfram'

def call_wolfram_api(query):
    # Call the Wolfram Alpha API with the provided query and return the result.
    
    appid = os.environ['WOLFRAMAPIKEY']  # Get the Wolfram Alpha API key from environment variables
    client = wolframalpha.Client(appid)
    result = client.query(query)  # Query the API with the given query
    return next(result.results).text  # Return the text from the first result

@plugin.command
@lightbulb.option('query', 'search query', type=str)  # Define an option for the query parameter
@lightbulb.command('wolframalpha', 'search for anything via WolframAlpha')  # Define the slash command
@lightbulb.implements(lightbulb.SlashCommand)  # Implement the SlashCommand interface
async def wolfram_cmd(ctx: lightbulb.Context):
    # Command to search for a query using Wolfram Alpha API and display the result.
    
    query = ctx.options.query  # Get the query parameter from the command invocation
    response = call_wolfram_api(query)  # Call the function to query the Wolfram Alpha API
    await ctx.respond(content=response)  # Send the response as the bot's message

def load(bot):
    # Load the Wolfram plugin into the bot.
    
    bot.add_plugin(plugin)  # Add the plugin to the bot's list of plugins
