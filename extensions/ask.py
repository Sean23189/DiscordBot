import requests
import os  # Import the os module for accessing environment variables
import wolframalpha  # Import the wolframalpha library
import lightbulb  # Import the lightbulb library for creating Commands

API_KEY = os.getenv('GOOGLEAPIKEY')
CX = os.getenv('CUSTOMSEARCHENGINEID')

plugin = lightbulb.Plugin('ask')  # Create a new plugin instance named 'wolfram'

def call_wolfram_api(query):
    # Call the Wolfram Alpha API with the provided query and return the result.
    
    appid = os.environ['WOLFRAMAPIKEY']  # Get the Wolfram Alpha API key from environment variables
    client = wolframalpha.Client(appid)
    result = client.query(query)  # Query the API with the given query
    return next(result.results).text  # Return the text from the first result

def get_top_result(query: str) -> str:
    url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={query}'
    # add timeout of 5 seconds to requests.get
    response = requests.get(url, timeout=5)
    json_data = response.json()
    google_result = json_data['items'][0]['title'] + '\n' + json_data['items'][0]['link']
    return  google_result

@plugin.command
@lightbulb.option('query', 'search query', type=str)  # Define an option for the query parameter
@lightbulb.command('ask', 'Ask about anything')  # Define the slash command
@lightbulb.implements(lightbulb.SlashCommand)  # Implement the SlashCommand interface
async def ask_cmd(ctx: lightbulb.Context):
    # Command to search for a query using Wolfram Alpha API and display the result.
    
    query = ctx.options.query  # Get the query parameter from the command invocation
    google_result = get_top_result(query)
    wolfram_response = call_wolfram_api(query)  # Call the function to query the Wolfram Alpha API
    message = f"Here are your results:\n\nWolframAlpha:\n{wolfram_response}\n\nGoogle:\n{google_result}"
    await ctx.respond(content=message)  # Send the response as the bot's message

def load(bot):
    # Load the Wolfram plugin into the bot.
    
    bot.add_plugin(plugin)  # Add the plugin to the bot's list of plugins
