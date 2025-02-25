import discord
import random
import asyncio
from discord.ext import commands
from datetime import datetime, time
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

DISCORD_TOKEN = 'token'

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

try:
    model = AutoModelForCausalLM.from_pretrained("gpt2").to(device)
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True 
bot = commands.Bot(command_prefix='/', intents=intents)

summoned_users = {}
penalty_users = {}

#Aw9at l3amal hhh 
def is_within_summoning_hours():
    now = datetime.now().time()
    return time(11, 0) <= now <= time(23, 30)

# HAADY LY FEHA LMOCHKILLL  
async def summon_users(channel):
    role_name = "1337plx"
    role = discord.utils.get(channel.guild.roles, name=role_name)

    # [Debug]: Check if the role exists
    print(f"DEBUG: Retrieved role - {role}")

    if not role:
        await channel.send(f"Role '{role_name}' not found. gha chufi tany wsf.")
        return

    # [debug] Print all roles in the server
    print("\n--- All Roles in the Server ---")
    for r in channel.guild.roles:
        print(f"Role found: {r.name}")
    print("\n--- Members & Their Roles ---")

    eligible_users = []
    await channel.guild.chunk()  # Loads all members
    for member in channel.guild.members:
        if member.bot:
            continue
        print(f"Total Members in Guild: {len(channel.guild.members)}")

        # [Debug] Print each member's roles
        member_roles = [r.name for r in member.roles]
        print(f"{member.name}: {member_roles}")

        # [debug] Fixed role-check condition
        if role in member.roles:
            print(f"✅ {member.name} is eligible!")  # Debug confirmation
            eligible_users.append(member)
        else:
            print(f"❌ {member.name} does NOT have '{role.name}'.")

    print(f"\nFinal Eligible Users: {[m.name for m in eligible_users]}")  # [Debug] output

    if not eligible_users:
        await channel.send("HAAAL3AAR HAAL3AAR RA MABAN LII WALOO.")
        return

    selected_users = random.sample(eligible_users, min(3, len(eligible_users)))
    summoned_users[channel.id] = selected_users

    mentions = ' '.join(user.mention for user in selected_users)
    await channel.send(f"{mentions} Come to Bocal now!")

    await wait_for_responses(channel, selected_users)

async def wait_for_responses(channel, selected_users):
    def check(m):
        return m.channel == channel and m.content == '/here' and m.author in selected_users

    try:
        responses = await bot.wait_for('message', timeout=120 * 60, check=check)  # 120 minutes
        await handle_responses(responses, channel)
    except asyncio.TimeoutError:
        for user in selected_users:
            if user not in penalty_users:
                penalty_users.append(user)
                await channel.send(f"{user.mention} You did not respond in time! Warning issued.")

async def handle_responses(responses, channel):
    user_responses = [response.author for response in responses]

    for user in user_responses:
        await ask_bocal_questions(user, channel)

async def ask_bocal_questions(user, channel):
    input_text = "Pretend to be a staff in 42 network and bocal me, like give a coding challenge in C and ask me 2 questions about technical things in programming (just C), do like a technical interview, and please send the response directly without the intros"
    
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_length=500)
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    await channel.send(f"{user.mention} Here you go, show us what you got:\n{decoded_output}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ({bot.user.id})')
    print('Bot is ready and online Wa9ila.')

@bot.command()
async def summon(ctx):
    print(f"Received summon command from {ctx.author}")

    if ctx.guild is None: 
        await ctx.send("This command can only be used in a server.")
        return

    if is_within_summoning_hours():
        await summon_users(ctx.channel)
    else:
        await ctx.send("Bocal is between 11 AM and 12 AM.")

@bot.command()
async def bocalme(ctx):
    if ctx.guild is None:  #check if it s DM
        await summon_users(ctx)
    else:
        await ctx.send("This command can only be used in DMs.")

@bot.command()
async def test(ctx):
    await ctx.send("Bot is working!")

@bot.command()
async def check_roles(ctx):
    for member in ctx.guild.members:
        print(f"{member.name}: {[role.name for role in member.roles]}")

bot.run(DISCORD_TOKEN)
