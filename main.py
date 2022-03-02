from datetime import datetime
from pydoc import cli
import sys
from time import time
import discord
from discord.ext import commands
import DiscordUtils
import random



# client = discord.Client(activity=discord.Game(name='my Game'))

client = commands.Bot(command_prefix = '.')
music = DiscordUtils.Music()

@client.event
async def on_ready():
  print('Oh Shit is now connected')
  # Playing
  # await client.change_presence(activity=discord.Game(name="a game"))
  
  # Streaming
  # await client.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))
  
  # Listening
  # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

  # Watching
  # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="OnlyFans"))

  # Changing status
  # await client.change_presence(status=discord.Status.idle)

@client.command(aliases = ['cls'] ) 
async def clear(ctx, amount=1000):
  if (not ctx.author.guild_permissions.manage_messages):
    await ctx.send("Oops, you don't have permission")
    return
	
  await ctx.channel.purge(limit=amount+1)

@client.event
async def on_message(message):

  if message.channel.id == 948514702915428352  and message.content != '.cls':
    return

  channel = client.get_channel(948514702915428352)


  if message.author.id == 438657626910228481 :
    msg= str(message.author.name) + ' : ' + str(message.content)
  else : 
    msg= f'<@{message.author.id}> : ' + str(message.content)  
  
  await channel.send(msg)
  await client.process_commands(message)




@client.command(aliases = ['Hey','Hi','Hello','hey','hi'] )
async def hello(message):
  await message.channel.send('Hey buddy!')



@client.command()
async def loop(message,amount=10):
  for i in range (1,amount+1):
    await message.send('This is Line {}'.format(i))

@client.command()
async def tagall(ctx,*,txt):
  """Send message to @everyone."""

  await ctx.message.delete()
  await ctx.send(f'>>> @everyone\n{txt}\n')

@client.command(aliases = ['ui'] )
async def userinfo(message,member : discord.Member = None):

  if member == None :
    member = message.author
 
  # user = await client.fetch_user(member)
  memberAvatar = member.avatar_url
  await message.send(f'The user: <@{member}>\nName: {member.name}\nUsername: {member.id}\nID: {member}')
  await message.send(memberAvatar)

@client.command()
async def avatar(ctx, member : discord.Member = None):
  if member == None:
    member = ctx.author
  memberAvatar = member.avatar_url
  await ctx.send(memberAvatar)

@client.command()
async def advise(ctx):
  advises=["What you're supposed to do when you don't like a thing is change it. If you can't change it, change the way you think about it. Don't complain,"
  "Try to be a rainbow in someone's cloud.",
  "Never miss a good chance to shut up.",
  "If a man will begin with certainties, he shall end in doubts; but if he will be content to begin with doubts, he shall end in certainties.",
  "We cannot change the cards we are dealt, just how we play the hand.",
  "Never ruin an apology with an excuse."]
  await ctx.send(random.choice(advises))

@client.command()
async def kick(ctx, member : discord.Member, *, reason = None):
  if (not ctx.author.guild_permissions.kick_members):
    await ctx.send("Oops, you don't have permission")
    return
  await member.kick(reason=reason)
  await ctx.send (f'{member.mention} has been kicked\n>>> Reason: {reason}')

@client.command()
async def ban (ctx, member : discord.Member, *, reason = None):
  if (not ctx.author.guild_permissions.ban_members):
    await ctx.send("Oops, you don't have permission")
    return
  await member.ban(reason=reason)
  await ctx.send (f'{member.mention} has been banned\n>>> Reason: {reason}')


@client.command()
async def unban(ctx, *, member):
  if (not ctx.author.guild_permissions.ban_members):
    await ctx.send("Oops, you don't have permission")
    return

  banned_users = await ctx.guild.bans()
  print(f'here is banned users\n {banned_users}')
  member_name, member_discriminator = member.split('#')
  print(f'here is member_name\n {member_name}')
  print(f'member_discriminator\n {member_discriminator}')
  for ban_entry in banned_users :
    user = ban_entry.user

    if (user.name,user.discriminator) == (member_name,member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send (f'{user.mention} has been unbanned')
      return


@client.command()
async def join(ctx):
  """Make the bot join the channel."""

  await ctx.author.voice.channel.connect()

@client.command()
async def leave(ctx):
  """Make the bot leave rhe channel."""

  await ctx.voice_client.disconnect()

@client.command()
async def play(ctx, *, url):
  """Make the bot play a song."""
  player = music.get_player(guild_id=ctx.guild.id)
  if not player:
    player = music.create_player(ctx, ffmpeg_error_betterfix=True)
  if not ctx.voice_client.is_playing():
    await player.queue(url, search=True)
    song = await player.play()
    await ctx.send(f'Playing ... ` {song.name} `')
  else:
    song = await player.queue(url, search=True)
    await ctx.send(f'` {song.name} ` queued')



@client.command()
async def roles(ctx):
    """Lists the current roles on the server."""

    roles = ctx.message.guild.roles
    result = "**The roles on this server are: **"
    for role in roles:
        result += role.name + ", "
    await ctx.send(result)

@client.command(aliases=['user'])
async def info(ctx, user: discord.Member = None):
	
  """Gets info on a member, such as their ID."""
  if user == None:
    user = ctx.author
  embed = discord.Embed(title="User profile: " + user.name, colour=user.colour)
  embed.add_field(name="Userame:", value=user)
  embed.add_field(name="ID:", value=user.id)
  embed.add_field(name="Profile:", value=user.mention)
  embed.add_field(name="Joined:", value=user.joined_at.strftime("%b %d, %Y"))
  embed.add_field(name="Registered:", value=user.created_at.strftime("%b %d, %Y"))
  embed.add_field(name="Highest role:", value=user.top_role)
  embed.set_thumbnail(url=user.avatar_url)
  await ctx.send(embed=embed)

@client.command()
async def setplay(ctx, *args):
    """Sets the 'Playing' status."""

    if ctx.message.author.guild_permissions.administrator:
        setgame = ' '.join(args)
        await client.change_presence(activity=discord.Game(setgame))
        await ctx.send(":ballot_box_with_check: Game name set to: `" + setgame + "`")
    else:
        await ctx.send("You don't have permission")

@client.command()
async def setwatch(ctx, *args):
    """Sets the 'Watching' status."""

    if ctx.message.author.guild_permissions.administrator:
        setgame = ' '.join(args)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=setgame))
        await ctx.send(":ballot_box_with_check: Watching set to: `" + setgame + "`")
    else:
        await ctx.send("You don't have permission")

@client.command()
async def setlisten(ctx, *args):
    """Sets the 'Listening' status."""

    if ctx.message.author.guild_permissions.administrator:
        setgame = ' '.join(args)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=setgame))
        await ctx.send(":ballot_box_with_check: Listening set to: `" + setgame + "`")
    else:
        await ctx.send("You don't have permission")

@client.command()
async def setidle(ctx):
    """Change the status."""
    if ctx.message.author.guild_permissions.administrator:
        await client.change_presence(status=discord.Status.idle)
        await ctx.send(":ballot_box_with_check: Status set to: `idle`")
    else:
        await ctx.send("You don't have permission")

@client.command()
async def setdnd(ctx):
    """Change the status."""
    if ctx.message.author.guild_permissions.administrator:
        await client.change_presence(status=discord.Status.do_not_disturb)
        await ctx.send(":ballot_box_with_check: Status set to: `Do Not Disturb`")
    else:
        await ctx.send("You don't have permission")

@client.command()
async def setonline(ctx):
    """Change the status."""
    if ctx.message.author.guild_permissions.administrator:
        await client.change_presence(status=discord.Status.online)
        await ctx.send(":ballot_box_with_check: Status set to: `Online`")
    else:
        await ctx.send("You don't have permission")

@client.command()
async def setoffline(ctx):
    """Change the status."""
    if ctx.message.author.guild_permissions.administrator:
        await client.change_presence(status=discord.Status.invisible)
        await ctx.send(":ballot_box_with_check: Status set to: `Invisible`")
    else:
        await ctx.send("You don't have permission")


client.run('OTQ4Mzc5Mzc1NzI2OTA3NDIy.Yh69Hw._PtkGJRzfpK07kPGJ6MgmNEuSWU')
