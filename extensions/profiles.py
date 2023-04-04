import lightbulb
import hikari
import sqlite3

plugin = lightbulb.Plugin('profiles')

@plugin.command
@lightbulb.command('profile', 'View your personal profile!')
@lightbulb.implements(lightbulb.SlashCommand)
async def profile_cmd(ctx):
    fullname = ctx.author.username + '#' + ctx.author.discriminator
    embed = hikari.Embed(
        title='Profile of ' + fullname,
        color=hikari.Color.from_rgb(0, 255, 0)
    )

    embed.add_field(name='UNFINISHED', value='UNFINISHED')
                    
    await ctx.respond(embed=embed)

def load(bot):
    bot.add_plugin(plugin)
