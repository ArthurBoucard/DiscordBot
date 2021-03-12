#!/usr/bin/env python3
##
## PERSONNAL PROJECT, 2020
## DiscordBots
## File description:
## flip_a_coin
##

import asyncio  
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import random
import time
import datetime

TOKEN = open("token.txt", "r").read()
Client = discord.Client()
client = commands.Bot(command_prefix = "!")

@client.command() #Same function of a help
async def helpme(message):

    if message.author == client.user:
        return
    else:
        msg = '''Here is the list of all commands {0.author.mention}:
-coin -> Flips a coin: !coin
-ccc "name of channel" -> Creates category channel with two sub-text channels (chat and bot-chat)
-cvc "name of voice chat" "time (in hours, max = 12)"-> Creates a voice channel witch delete itself after "time" as passed'''.format(message)
        await message.send(msg)

@client.command() #Flips a coin
async def coin(ctx):

    if random.randint(0,1) == 1:
        await ctx.send('head'.format(ctx))
    else:
        await ctx.send('tail'.format(ctx))


list_ca_cat = [] #Catgory channel's category
list_ch_id = [] #Bot chats channel's id

@client.command() #Creates a category channel with two sub channels, store the variable in the above lists
async def ccc(ctx, arg):

    guild = ctx.message.guild
    category = await guild.create_category(arg)
    list_ca_cat.append(category)

    await guild.create_text_channel("chat",  category = category)

    channel = await guild.create_text_channel("bot chat",  category = category)
    channel = channel.id
    list_ch_id.append(channel)

t = time.localtime()
list_cvc_ch = [] #Voice channel's channel
list_cvc_time = [] #End time of Voice channel

@client.command() #Creates voice channel in the category channel of the bot chat's channel
async def cvc(ctx, arg):

    for i in range(0, len(list_ch_id)):
        if ctx.message.channel.id == list_ch_id[i]:
            guild = ctx.message.guild
            name = str(ctx.author)
            title = name[:name.rfind("#")] + " - " + arg
            channel = await guild.create_voice_channel(title,  category = list_ca_cat[i])
            list_cvc_ch.append(channel)
            current_time = datetime.datetime.now()
            hours_added = datetime.timedelta(hours = 12)
            new_time = current_time + hours_added
            list_cvc_time.append(new_time)

async def delete_old_cvc():
    while True:
        await asyncio.sleep(10)
        for i in range(0, len(list_cvc_time)):
            current_date = datetime.datetime.now()
            check = list_cvc_time[i] - current_date
            if list_cvc_time[i] > current_date and check < datetime.timedelta(minutes = 2):
                await list_cvc_ch[i].delete()

client.loop.create_task(delete_old_cvc())
client.run(TOKEN)