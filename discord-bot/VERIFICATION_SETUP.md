# 🔮 Verification System Setup Guide

Your bot now has a beautiful, aesthetic verification system! Here's how to set it up.

---

## 📋 Step 1: Create Required Roles

In your Discord server, create these two roles:

1. **Unverified**

   - Color: Gray or Red
   - Permissions: Very limited (can only see verification channel)
   - Position: Below Member role

2. **Member**
   - Color: Your choice (e.g., Purple to match the aesthetic)
   - Permissions: Normal member permissions
   - Position: Above Unverified role

### Quick Role Setup:

1. Go to Server Settings → Roles
2. Click "Create Role"
3. Name it exactly "Unverified" (case-sensitive)
4. Set permissions (limit access)
5. Repeat for "Member" role

---

## 🎨 Step 2: Create Verification Channel

1. Create a new text channel called `#verification` or `#welcome`
2. Set permissions so:
   - **@Unverified** can VIEW and READ (but not send messages)
   - **@Member** CANNOT see this channel
   - **@everyone** CANNOT see this channel

---

## 🚀 Step 3: Deploy Verification Message

1. **Restart your bot** (so it loads the new verification cog)
2. In Discord, go to your verification channel
3. Use the command:
   ```
   /setup_verification
   ```
4. The bot will post a beautiful verification embed with a button!

---

## ✨ How It Works

### For New Members:

1. User joins the server
2. Bot automatically gives them the **Unverified** role
3. They can only see the verification channel
4. They click the "✨ Verify & Join The Frequency" button
5. Bot removes **Unverified** role and adds **Member** role
6. They now have full server access!

### Auto-Kick System:

- If a user doesn't verify within **24 hours**, they are automatically kicked
- The bot checks every 5 minutes for expired verifications
- Once verified, they're removed from the auto-kick list

---

## 🎯 Admin Commands

### `/setup_verification`

Deploy the verification embed in a channel.

```
/setup_verification #channel-name
```

### `/pending_kicks`

View all users who will be auto-kicked if they don't verify.

```
/pending_kicks
```

---

## 🎨 Customization Options

### Change Colors

Edit `verification.py` and change the color codes:

```python
color=0x9b59b6  # Purple - change this hex code
```

Popular colors:

- Purple: `0x9b59b6`
- Blue: `0x3498db`
- Pink: `0xe91e63`
- Green: `0x2ecc71`

### Add Banner Image

Uncomment and add your image URL in `verification.py`:

```python
embed.set_image(url="YOUR_IMAGE_URL_HERE")
```

### Change Auto-Kick Time

In `verification.py`, find:

```python
kick_time = datetime.utcnow() + timedelta(hours=24)
```

Change `hours=24` to any number you want!

---

## 🔧 Troubleshooting

**Button doesn't work:**

- Make sure bot has "Manage Roles" permission
- Ensure bot's role is ABOVE both Unverified and Member roles

**Roles not being assigned:**

- Check role names are exactly "Unverified" and "Member" (case-sensitive)
- Verify bot has "Manage Roles" permission

**Auto-kick not working:**

- Bot must stay online for auto-kick to work
- Check bot logs for any errors

---

## 🌟 What's Next?

Your verification system is ready! Test it by:

1. Creating a test account
2. Joining your server
3. Clicking the verification button
4. Checking if roles are assigned correctly

Enjoy your aesthetic verification system! 🎵✨
