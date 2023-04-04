import os  # For retrieving environment variables
import lightbulb  # For creating the Discord bot instance

bot = lightbulb.BotApp(
    token=os.getenv('DISCORDBOTTOKEN'), # Retrieve the Discord bot token
    logs='DEBUG' # Set the logging level to debug
)

# Load all extensions from the './extensions' directory
bot.load_extensions_from('./extensions')

# Start the bot
bot.run()
