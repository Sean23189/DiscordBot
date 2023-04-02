import lightbulb

plugin = lightbulb.Plugin("userinput")

@plugin.command
@lightbulb.option("input_text", "The text you want to store")
@lightbulb.command("userinput", "Store any message forever!")
@lightbulb.implements(lightbulb.SlashCommand)
async def store_input(ctx: lightbulb.Context):
    username = ctx.author.username
    discriminator = ctx.author.discriminator
    input_text = ctx.options.input_text
    with open("userinput.txt", "a") as f:
        f.write(f"{username}#{discriminator}: {input_text}\n")
    with open("userinput.txt", "r") as f:
        line_number = len(f.readlines())
    await ctx.respond(f"Stored message '{input_text}' for user {username}#{discriminator} on line {line_number}.")

@plugin.command
@lightbulb.option("search", "The line number to search for", int)
@lightbulb.command("searchinput", "Search for a line in the userinput file")
@lightbulb.implements(lightbulb.SlashCommand)
async def search_input(ctx: lightbulb.Context):
    search_line_number = ctx.options.search
    with open("userinput.txt", "r") as f:
        lines = f.readlines()
    if len(lines) < search_line_number:
        await ctx.respond("That line does not exist.")
    else:
        message = lines[search_line_number - 1].strip()
        await ctx.respond(message)

def load(bot):
    bot.add_plugin(plugin)
