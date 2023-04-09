import lightbulb  # importing lightbulb library for creating commands
import hikari     # importing hikari library for creating embeds
import sqlite3    # importing sqlite3 library for database operations

plugin = lightbulb.Plugin('profiles')  # creating a new plugin object for the 'profiles' feature

@plugin.command  # registering a command with the plugin object
@lightbulb.command('profile', 'View your personal profile!')  # defining the command
@lightbulb.implements(lightbulb.SlashCommand)  # implementing the command as a slash command
async def profile_cmd(ctx):  # defining the function that will execute when the command is triggered
    fullname = ctx.author.username + '#' + ctx.author.discriminator  # getting the username and discriminator
    embed = hikari.Embed(  # creating a new embed object
        title='Profile of ' + fullname,  # setting the title of the embed
        color=hikari.Color.from_rgb(0, 255, 0)  # setting the color of the embed
    )

    embed.add_field(name='UNFINISHED', value='UNFINISHED')  # adding a field to the embed (this will be updated with actual data later)
                    
    await ctx.respond(embed=embed)  # sending the embed as a response to the command

def load(bot):  # defining a function that will be used to load the plugin into the bot
    bot.add_plugin(plugin)  # adding the plugin object to the bot's plugins list
