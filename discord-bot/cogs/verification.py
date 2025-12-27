import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timedelta
import asyncio

class VerificationButtons(discord.ui.View):
    """Persistent buttons for verification and emergency SOS."""
    
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view
    
    @discord.ui.button(
        label="Verify",
        style=discord.ButtonStyle.success,
        custom_id="verify_button",
        emoji="✨"
    )
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle verification button click."""
        # Get roles
        unverified_role = discord.utils.get(interaction.guild.roles, name="Unverified")
        member_role = discord.utils.get(interaction.guild.roles, name="Member")
        
        if not unverified_role or not member_role:
            await interaction.response.send_message(
                "❌ System configuration error. Please contact a server administrator.",
                ephemeral=True
            )
            return
        
        # Check if user is already verified
        if member_role in interaction.user.roles:
            await interaction.response.send_message(
                "✨ You are already verified and have full access.",
                ephemeral=True
            )
            return
        
        # Remove unverified, add member role
        try:
            await interaction.user.remove_roles(unverified_role)
            await interaction.user.add_roles(member_role)
            
            # Clean verification success embed
            embed = discord.Embed(
                description=f"# Welcome to the Community\n{interaction.user.mention}, you have been successfully verified.",
                color=0x2b2d31  # Dark theme background match or soft accent
            )
            embed.set_image(url="https://media.discordapp.net/attachments/1079234836696731708/1126966838883356743/line.gif") # Aesthetic line
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Verification failed: {str(e)}",
                ephemeral=True
            )

class Verification(commands.Cog):
    """Verification system with aesthetic design and auto-kick."""
    
    def __init__(self, bot):
        self.bot = bot
        self.pending_kicks = {}  # Store users pending kick
        self.auto_kick_check.start()  # Start background task
    
    def cog_unload(self):
        """Stop background task when cog unloads."""
        self.auto_kick_check.cancel()
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Add persistent view when bot starts."""
        self.bot.add_view(VerificationButtons())
        print("Verification system loaded!")
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Give new members the Unverified role and schedule auto-kick."""
        unverified_role = discord.utils.get(member.guild.roles, name="Unverified")
        
        if unverified_role:
            try:
                await member.add_roles(unverified_role)
                
                # Schedule auto-kick in 24 hours
                kick_time = datetime.utcnow() + timedelta(hours=24)
                self.pending_kicks[member.id] = {
                    'guild_id': member.guild.id,
                    'kick_time': kick_time,
                    'username': str(member)
                }
                
                print(f"✅ {member} joined and received Unverified role. Auto-kick scheduled for {kick_time}")
                
            except Exception as e:
                print(f"Error assigning role to {member}: {e}")
    
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Remove from auto-kick list when verified."""
        # Check if they got the Member role
        member_role = discord.utils.get(after.guild.roles, name="Member")
        
        if member_role in after.roles and member_role not in before.roles:
            # They got verified! Remove from kick list
            if after.id in self.pending_kicks:
                del self.pending_kicks[after.id]
                print(f"✅ {after} verified! Removed from auto-kick list.")
    
    @tasks.loop(minutes=5)  # Check every 5 minutes
    async def auto_kick_check(self):
        """Check for users who need to be kicked."""
        current_time = datetime.utcnow()
        to_kick = []
        
        for user_id, data in self.pending_kicks.items():
            if current_time >= data['kick_time']:
                to_kick.append(user_id)
        
        for user_id in to_kick:
            data = self.pending_kicks[user_id]
            guild = self.bot.get_guild(data['guild_id'])
            
            if guild:
                try:
                    member = guild.get_member(user_id)
                    if member:
                        unverified_role = discord.utils.get(guild.roles, name="Unverified")
                        
                        # Only kick if they still have Unverified role
                        if unverified_role in member.roles:
                            await member.kick(reason="Did not verify within 24 hours")
                            print(f"⏰ Kicked {data['username']} for not verifying within 24 hours")
                    
                    # Remove from pending kicks
                    del self.pending_kicks[user_id]
                    
                except Exception as e:
                    print(f"Error kicking {data['username']}: {e}")
    
    @auto_kick_check.before_loop
    async def before_auto_kick_check(self):
        """Wait for bot to be ready before starting the task."""
        await self.bot.wait_until_ready()
    
    @app_commands.command(name="setup_verify", description="Deploy the aesthetic verification module")
    async def setup_verify(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        """Deploy the verification embed."""
        target_channel = channel or interaction.channel
        
        # MINIMAL & CLEAN ESTHETIC
        embed = discord.Embed(
            title="Verification Required",
            description="To access the server, please verify your account by clicking the button below.\n\n*Unverified members are automatically removed after 24 hours.*",
            color=0x2b2d31
        )
        
        # Clean footer
        embed.set_footer(text="Secure Verification")
        embed.timestamp = datetime.utcnow()
        
        # Keep the server icon as thumbnail (branding)
        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)
        
        # Respond to interaction first
        await interaction.response.send_message(
            f"✨ Deploying minimal verification in {target_channel.mention}...",
            ephemeral=True
        )
        
        # Then send the embed
        try:
            view = VerificationButtons()
            await target_channel.send(embed=embed, view=view)
            await interaction.edit_original_response(content=f"✨ Done! Deployed in {target_channel.mention}")
        except discord.Forbidden:
            await interaction.edit_original_response(content=f"❌ Missing permissions in {target_channel.mention}!")
        except Exception as e:
            await interaction.edit_original_response(content=f"❌ Error: {str(e)}")

    
    @app_commands.command(name="pending_kicks", description="View users pending auto-kick")
    async def pending_kicks(self, interaction: discord.Interaction):
        """Show list of users who will be auto-kicked."""
        if not self.pending_kicks:
            await interaction.response.send_message("✅ No users pending auto-kick!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="⏰ Pending Auto-Kicks",
            description="Users who will be kicked if they don't verify:",
            color=0xe74c3c  # Red
        )
        
        for user_id, data in self.pending_kicks.items():
            time_left = data['kick_time'] - datetime.utcnow()
            hours = int(time_left.total_seconds() // 3600)
            minutes = int((time_left.total_seconds() % 3600) // 60)
            
            embed.add_field(
                name=data['username'],
                value=f"Kicks in: {hours}h {minutes}m",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    """Required function to add this cog to the bot."""
    await bot.add_cog(Verification(bot))
