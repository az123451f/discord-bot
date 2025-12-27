import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from keep_alive import keep_alive

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f'Bot is online as {bot.user}')
    print(f'Bot ID: {bot.user.id}')
    print('------')
    
    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.event
async def on_message(message):
    """Called when a message is sent in a channel the bot can see."""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Process commands
    await bot.process_commands(message)

# Load cogs (command modules)
async def load_cogs():
    """Load all cog files from the cogs directory."""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog: {filename}')
            except Exception as e:
                print(f'Failed to load cog {filename}: {e}')

async def main():
    """Main function to start the bot."""
    keep_alive() # Start the web server
    async with bot:
        await load_cogs()
        
        # Get token from environment variable
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            print('ERROR: DISCORD_TOKEN not found in environment variables!')
            print('Please create a .env file with your Discord bot token.')
            return
        
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
