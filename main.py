import os
import lightbulb

# The ID of the default guild for the bot
DEFAULT_GUILDS = "986235093569916948"

# Create a new bot app instance with the specified token, default guilds, and logging level
bot = lightbulb.BotApp(
    token=os.getenv("DISCORDBOTTOKEN"), # Retrieve the Discord bot token from an environment variable
    default_enabled_guilds=(DEFAULT_GUILDS), # Set the default guild(s) for the bot
    logs="DEBUG" # Set the logging level to debug for verbose output
)

# Load all extensions from the "./extensions" directory
bot.load_extensions_from("./extensions")

# Start the bot
bot.run()
