import sqlite3
import lightbulb
import hikari

# Define a plugin with the name 'userinput'
plugin = lightbulb.Plugin('userinput')

# Connect to the SQLite database
connection = sqlite3.connect('userinput.db')
cursor = connection.cursor()

# Create the userinput table if it does not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS userinput
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user TEXT,
                   message TEXT)''')
connection.commit()

# Define a command called 'userinput' which takes an argument called 'input_text'
@plugin.command
@lightbulb.option('input_text', 'The text you want to store')
@lightbulb.command('userinput', 'Store any message forever!')
@lightbulb.implements(lightbulb.SlashCommand)
async def store_input(ctx: lightbulb.Context):
    # Get the username and discriminator of the user who invoked the command
    # Set variable fullname to the username + discriminator (ex. Test#1234)
    fullname = ctx.author.username + '#' + ctx.author.discriminator

    # Get the 'input_text' option passed in by the user
    input_text = ctx.options.input_text

    # Insert the username, discriminator, and input text into the userinput table
    cursor.execute('INSERT INTO userinput (user, message) VALUES (?, ?)', (fullname, input_text))
    connection.commit()

    # Get the row number of the newly added message
    row_number = cursor.lastrowid

    # Respond to the user to confirm that their message was stored
    await ctx.respond(f'Stored message {input_text} for user {fullname} on row {row_number}.')

# Define a command called 'searchinput' which takes an argument called 'search'
@plugin.command
@lightbulb.option('search', 'The row number to search for', int)
@lightbulb.command('searchinput', 'Search for a row in the userinput table')
@lightbulb.implements(lightbulb.SlashCommand)
async def search_input(ctx: lightbulb.Context):
    # Get the 'search' option passed in by the user
    search_row_number = ctx.options.search

    fullname = ctx.author.username + '#' + ctx.author.discriminator

    # Select the row from the userinput table
    cursor.execute('SELECT message FROM userinput WHERE id = ?', (search_row_number,))
    result = cursor.fetchone()

    # Check if the requested row exists in the table
    if not result:
        await ctx.respond('That row does not exist.')
    else:
        # Get the requested message and respond to the user with it
        message = result[0]
        await ctx.respond(fullname + ": " + message)

@plugin.command()
@lightbulb.command('showall', 'Show all entries from the userinput table!')
@lightbulb.implements(lightbulb.SlashCommand)
async def showall(ctx):
    # Select all rows from the userinput table
    cursor.execute('SELECT * FROM userinput')
    results = cursor.fetchall()

    fullname = ctx.author.username + '#' + ctx.author.discriminator

    # Create a new embed
    embed = hikari.Embed(
        title='All Entries to the userinput table!',
        color=hikari.Color.from_rgb(255, 0, 0)
    )

    # Add each row as a field to the embed
    for row in results:
        embed.add_field(name=('Row N.' + str(row[0])), value=fullname + ": " + row[2])

    # Send the embed
    await ctx.respond(embed=embed)

# Define a function to unload the plugin from the bot
def unload(bot):
    connection.close()


# Define a function to load the plugin into the bot
def load(bot):
    bot.add_plugin(plugin)