import discord
from discord.ext import commands
import youtube_dl
import os
from keep_alive import keep_alive
import time
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check


client = commands.Bot(command_prefix="-")

@client.event
async def on_ready():
  print('Online ^-^ als {0.user}'
  .format(client))

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='LernRaum')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
  
async def on_message(self, message):
  if message.content.startswith(" -Chillout "):
    where = message.content.split(" ") [1]
    channel = get(message.guild.channels, name=where)
    voiceChannel.play(discord.FFmpegPCMAudio('Wind.mp3'))




@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command()
async def hilf (ctx, member : discord.Member):
    try:
        await member.kick(reason= None )
        await ctx.send("SOO der KEK ist endlich weg "+member.mention) #simple kick command to demonstrate how to get and use member mentions
    except:
        await ctx.send("Keine rechte dafür :( ")

@client.command()
async def kick(ctx, member : discord.Member):
    try:
        await member.kick(reason= None )
        await ctx.send("Soo der KEK ist jetzt immer weg "+member.mention) #simple kick command to demonstrate how to get and use member mentions
    except:
        await ctx.send(" So nicht xD ")

@client.command()
async def ban (ctx, member : discord.Member):
    try:
        await member.ban(reason= None)
        await ctx.send("Banned "+member.mention) #simple kick command to demonstrate how to get and use member mentions
    except:
        await ctx.send("Keine rechte dafür :( ")

@client.command()
async def bann (ctx, member : discord.Member):
    try:
        await member.ban(reason= None )
        await ctx.send("Ich hoffe der bleibt auch weg ^^"+member.mention) #simple kick command to demonstrate how to get and use member mentions
    except:
        await ctx.send("Keine rechte dafür :( ")

keep_alive()
client.run(os.getenv('TOKEN'))