import lightbulb


plugin = lightbulb.Plugin('help_cmd')  # Create a new plugin instance named 'help_cmd'

@plugin.command
@lightbulb.command('help', 'list all available commands')  # Define the slash command
@lightbulb.implements(lightbulb.SlashCommand)  # Implement the SlashCommand interface
async def command_list_cmd(ctx: lightbulb.Context):
    # Command to list all available commands for the bot.

    command_list = [
        "/google",
        "/wolfram",
        "/profiles",
        "/userinput",
        "/get"
    ]
    
    response = "Available commands:\n" + "\n".join(command_list)
    await ctx.respond(content=response)

def load(bot):
    # Load the help plugin into the bot.
    
    bot.add_plugin(plugin)  # Add the plugin to the bot's list of plugins
