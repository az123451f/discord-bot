# Discord Bot Setup Guide

A customizable Discord bot built with discord.py.

## 📋 Prerequisites

- Python 3.8 or higher
- A Discord account
- A LemonHost account (for hosting)

---

## 🤖 Step 1: Create Your Discord Bot

1. **Go to Discord Developer Portal**

   - Visit [https://discord.com/developers/applications](https://discord.com/developers/applications)
   - Click "New Application"
   - Give it a name and click "Create"

2. **Create a Bot User**

   - In your application, go to the "Bot" tab on the left
   - Click "Add Bot" and confirm
   - Under "Privileged Gateway Intents", enable:
     - ✅ Presence Intent
     - ✅ Server Members Intent
     - ✅ Message Content Intent
   - Click "Save Changes"

3. **Get Your Bot Token**

   - Under the "Bot" tab, click "Reset Token"
   - Copy the token (you'll need this later)
   - ⚠️ **NEVER share this token publicly!**

4. **Invite Bot to Your Server**
   - Go to the "OAuth2" → "URL Generator" tab
   - Under "Scopes", select:
     - ✅ `bot`
     - ✅ `applications.commands`
   - Under "Bot Permissions", select:
     - ✅ Send Messages
     - ✅ Read Message History
     - ✅ Use Slash Commands
     - ✅ Embed Links
     - (Add more permissions as needed)
   - Copy the generated URL at the bottom
   - Paste it in your browser and invite the bot to your server

---

## 💻 Step 2: Local Setup & Testing

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**

   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Edit `.env` and replace `your_bot_token_here` with your actual bot token

3. **Run the Bot Locally**

   ```bash
   python bot.py
   ```

4. **Test Commands**
   - In your Discord server, try these slash commands:
     - `/ping` - Check bot responsiveness
     - `/hello` - Get a greeting
     - `/info` - View bot information

---

## 🌐 Step 3: Deploy to LemonHost

### A. Prepare Your Files

1. Make sure you have these files ready:
   - `bot.py`
   - `cogs/basic.py`
   - `requirements.txt`
   - `.env` (with your token)

### B. LemonHost Setup

1. **Create a LemonHost Account**

   - Go to [LemonHost](https://lemonhost.net/) or your preferred hosting provider
   - Sign up for a Python hosting plan

2. **Create a New Bot Instance**

   - Log in to your LemonHost panel
   - Create a new Python bot instance
   - Select Python 3.8+ as your environment

3. **Upload Files**

   - Upload all bot files to your LemonHost instance:
     - `bot.py`
     - `cogs/` folder with all cog files
     - `requirements.txt`
   - You can use SFTP/FTP or the web file manager

4. **Set Environment Variables**

   - In LemonHost panel, find "Environment Variables" or "Config"
   - Add: `DISCORD_TOKEN` = `your_bot_token_here`
   - This is more secure than uploading your `.env` file

5. **Install Dependencies**

   - In the LemonHost console/terminal, run:
     ```bash
     pip install -r requirements.txt
     ```

6. **Start the Bot**
   - Set the startup command to: `python bot.py`
   - Start the bot from the LemonHost panel
   - Check the console logs to verify it's online

### C. Verify Deployment

1. Check the console logs for:

   ```
   Bot is online as YourBotName
   Synced X command(s)
   ```

2. In Discord, verify your bot shows as "Online"

3. Test slash commands to ensure everything works

---

## 🔧 Adding Custom Features

### Creating New Commands

1. Create a new cog file in the `cogs/` folder
2. Follow this template:

```python
import discord
from discord.ext import commands
from discord import app_commands

class YourCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="yourcommand", description="Description here")
    async def your_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Your response!")

async def setup(bot):
    await bot.add_cog(YourCog(bot))
```

3. Restart the bot to load the new commands

### Event Handlers

Add event handlers in `bot.py`:

```python
@bot.event
async def on_member_join(member):
    # Do something when a user joins
    pass
```

---

## 📚 Useful Resources

- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs)
- [discord.py Examples](https://github.com/Rapptz/discord.py/tree/master/examples)

---

## ⚠️ Troubleshooting

**Bot won't start:**

- Check that your token is correct in the environment variables
- Ensure all intents are enabled in Discord Developer Portal

**Commands not showing:**

- Wait a few minutes for Discord to sync commands
- Try using the command anyway (sometimes they work before appearing)
- Restart the bot

**Bot goes offline randomly:**

- Check LemonHost logs for errors
- Ensure your hosting plan has enough resources
- Verify your token hasn't been reset

---

## 🎯 Next Steps

Now that your bot is running, you can:

- Add custom commands for your specific needs
- Implement moderation features
- Add database integration
- Create interactive buttons and menus
- Build custom functionality

Happy coding! 🚀
