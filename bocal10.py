import json
import random
import asyncio
import discord
import requests
from discord.ext import commands
from datetime import datetime, time

#1st of all ... i will pray for your knees to break if you steal this , i see you ... Mr ...
API_key = "token"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_key}"
DISCORD_TOKEN = 'token'

# gemini setting 
# total chlada but works
def generate_text(prompt):
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_json = response.json()
        candidates = response_json.get("candidates", [{}])
        if candidates:
            content_parts = candidates[0].get("content", {}).get("parts", [])
            if content_parts:
                return content_parts[0].get("text", "Luuckkyyy youu! Something went wrong.")
        
        return "Bingoo you are luckyy! Something went wrong while generating the challenge."
    else:
        print("API Error:", response.status_code, response.text)
        return "Bingoo you are luckyy! Something went wrong while generating the challenge."


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix='/', intents=intents)

summoned_users = {}
penalty_users = set()

# [to change after ...]
def is_within_summoning_hours():
    now = datetime.now().time()
    return time(11, 0) <= now or now <= time(3, 30)

async def summon_users(channel):
    role_name = "1337plx"
    role = discord.utils.get(channel.guild.roles, name=role_name)

    if not role:
        await channel.send(f"Role '{role_name}' not found. gha chuf tany wsf.")
        return

    eligible_users = [member for member in channel.guild.members if role in member.roles and not member.bot]
    
    if not eligible_users:
        await channel.send("No new eligible users to summon.")
        return
    
    selected_users = random.sample(eligible_users, min(3, len(eligible_users)))
    summoned_users[channel.id] = selected_users
    mentions = ' '.join(user.mention for user in selected_users)
    await channel.send(f"{mentions} Come to Bocal now!")

    await wait_for_responses(channel, selected_users)

# total chlada but works
async def wait_for_responses(channel, selected_users):
    def check(m):
        return m.channel == channel and m.content == '/here' and m.author in selected_users

    try:
        response = await bot.wait_for('message', timeout=120 * 60, check=check)
        await handle_responses([response], channel)
    except asyncio.TimeoutError:
        for user in selected_users:
            if user not in penalty_users:
                penalty_users.add(user)
                await channel.send(f"{user.mention} Penalty for not responding !!.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        await channel.send("An error occurred while waiting for responses. Please try again later.")

async def handle_responses(responses, channel):
    user_responses = [response.author for response in responses]
    for user in user_responses:
        await ask_bocal_questions(user, channel)

# [to change after ...] / works but with x2 issues 
async def ask_bocal_questions(user, channel):
    input_text = "Generate exactly ONE C programming challenge (easy to medium not very hard) and ask exactly TWO technical questions about C (easy to medium not very hard). Provide the challenge and questions directly without any introduction or repetition, formatted properly, without repetition."
    challenge_text = generate_text(input_text)
    await channel.send(f"Yeeh mr7baa")
    await channel.send(f"{user.mention}, here is your challenge show us what you got : {challenge_text}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ({bot.user.id})')
    print('Bot is ready and online Wa9ila.')

#the summon command changed to bocal starts now
@bot.command()
@commands.has_role('Admin')
async def bocal_starts_now(ctx):
    if not discord.utils.get(ctx.author.roles, name="Admin"):
        await ctx.send("W9af 3nd 7addk you clearly don’t have permission to use this command.")
        return

    if ctx.guild is None:
        await ctx.send("Bro are you dyslexic? This command can only be used in a server dummy ...")
        return

    if is_within_summoning_hours():
        await summon_users(ctx.channel)
    else:
        await ctx.send("BBro are you dyslexic? bocal is between 11 AM and 12 AM.")

#bocalme removed and we'll be modified later...

@bot.command()
async def here(ctx):
    if ctx.author in summoned_users.get(ctx.channel.id, []):
        await ask_bocal_questions(ctx.author, ctx.channel)
    else:
        await ctx.send(f"{ctx.author.mention}?? Sir htta n3yito 3lik malk zrban")

@bot.command()
@commands.has_role('Admin')
async def test(ctx):
    await ctx.send("Bot is working!")

@bot.command()
@commands.has_role('Admin')
async def check_roles(ctx):
    for member in ctx.guild.members:
        print(f"{member.name}: {[role.name for role in member.roles]}")

bot.run(DISCORD_TOKEN)
