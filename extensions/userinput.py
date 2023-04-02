import lightbulb

# Define a plugin with the name 'userinput'
plugin = lightbulb.Plugin("userinput")

# Define a command called 'userinput' which takes an argument called 'input_text'
@plugin.command
@lightbulb.option("input_text", "The text you want to store")
@lightbulb.command("userinput", "Store any message forever!")
@lightbulb.implements(lightbulb.SlashCommand)
async def store_input(ctx: lightbulb.Context):
    # Get the username and discriminator of the user who invoked the command
    username = ctx.author.username
    discriminator = ctx.author.discriminator

    # Get the 'input_text' option passed in by the user
    input_text = ctx.options.input_text

    # Write the username, discriminator, and input text to a file
    with open("userinput.txt", "a", encoding="utf-8") as file:
        file.write(f"{username}#{discriminator}: {input_text}\n")

    # Get the line number of the newly added message
    with open("userinput.txt", "r", encoding="utf-8") as file:
        line_number = len(file.readlines())

    # Respond to the user to confirm that their message was stored
    await ctx.respond(f"Stored message '{input_text}' for user {username}#{discriminator} on line {line_number}.")

# Define a command called 'searchinput' which takes an argument called 'search'
@plugin.command
@lightbulb.option("search", "The line number to search for", int)
@lightbulb.command("searchinput", "Search for a line in the userinput file")
@lightbulb.implements(lightbulb.SlashCommand)
async def search_input(ctx: lightbulb.Context):
    # Get the 'search' option passed in by the user
    search_line_number = ctx.options.search

    # Read the lines from the userinput file
    with open("userinput.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Check if the requested line number exists in the file
    if len(lines) < search_line_number:
        await ctx.respond("That line does not exist.")
    else:
        # Get the requested message and respond to the user with it
        message = lines[search_line_number - 1].strip()
        await ctx.respond(message)

# Define a function to load the plugin into the bot
def load(bot):
    bot.add_plugin(plugin)
