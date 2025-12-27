import discord
from discord.ext import commands
from discord import app_commands

class Basic(commands.Cog):
    """Basic commands for the bot."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Check if the bot is responsive")
    async def ping(self, interaction: discord.Interaction):
        """Responds with the bot's latency."""
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'🏓 Pong! Latency: {latency}ms')
    
    @app_commands.command(name="hello", description="Say hello to the bot")
    async def hello(self, interaction: discord.Interaction):
        """Greets the user."""
        await interaction.response.send_message(f'👋 Hello, {interaction.user.mention}!')
    
    @app_commands.command(name="info", description="Get information about the bot")
    async def info(self, interaction: discord.Interaction):
        """Shows bot information."""
        embed = discord.Embed(
            title="Bot Information",
            description="A custom Discord bot",
            color=discord.Color.blue()
        )
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.set_footer(text=f"Bot ID: {self.bot.user.id}")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Required function to add this cog to the bot."""
    await bot.add_cog(Basic(bot))
