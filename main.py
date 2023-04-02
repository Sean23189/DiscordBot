import os
import lightbulb


bot = lightbulb.BotApp(token=os.getenv("DISCORDBOTTOKEN"), default_enabled_guilds=(986235093569916948), logs="DEBUG")

bot.load_extensions_from("./extensions")
bot.run()
