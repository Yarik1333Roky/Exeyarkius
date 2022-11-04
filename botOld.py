import random as rand
import asyncio
import discord
from discord.ui import Button, View
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
import aiohttp
import datetime
import time
from gtts import gTTS
from googlesearch import search

bot = commands.Bot(command_prefix = '.', intents=discord.Intents.all())
bot.remove_command("help")

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

commands_list = ["clear", "join", "leave", "play", "info", "ball8", "helper", "dog", "kick", "ban", "addadmins", "removeadmins", "listadmins", "queue", "unban", "banlist", "say", "find", "blackjack", "repeat"]
descriptions_for_commands = ["Очистка чата", "присоедини меня в голосовой канал и глазей на меня", "отключи меня из голосового канала", "можно загрузить музычку из ютуба", "все команды", "можно что-нибудь написать и получить в ответ", "помощь по командам", "рандомные картинки собачек", "кикать непослушных игроков по причине", "банить очень непослушных игроков по причине", "назначить роль админом (тоесть эта роль сможет управлять всеми командами модерации) (нужно указывать *АЙДИ РОЛИ*)", "убрать роль с админки (нужно указывать *АЙДИ РОЛИ*)", "все роли с правами модератора для моих команд", "просмотреть текущий список музыки", "эта команда наоборот, разбанивает игроков на этом сервере", "показывает всех забаненых на этом сервере, проще говоря бан лист", "я могу сказать что нибудь в голосовом канале (только если не играет музыка, я же всё-таки с одним микрофоном :))", "можно загуглить что-нибудь в гугле", "да, да, да со мной можно поиграть в блекджек :)", "повторять песню"]
admins_role = []
queues = []
can_playing = False
repeatMusic = False

async def queue_module(ctx, after:False):
    global can_playing
    
    if after == True:
        can_playing == False

    if can_playing==False:
        datas = 0
        for data in queues:
            datas = datas + 1
        
        if datas > 0:
            my_data = queues[0]
            info = my_data["info"]
            author = my_data["author"]

            voice = get(bot.voice_clients, guild = ctx.guild)
 
            url = info['formats'][0]['url']
            voice.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
            can_playing=True
        
            realDuration = str(datetime.timedelta(seconds=info["duration"]))

            embedPlay = discord.Embed(
                title=info["title"],
                url=info["url"]
            )

            embedPlay.set_thumbnail(url=info["thumbnail"])
            embedPlay.add_field(
                name=f"Поставил: {author.display_name}",
                value=f"▶ ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ (00:00:00 / {realDuration})",
                inline=True
            )

            message = await ctx.send(embed=embedPlay)

            number = 0
            while voice.is_playing():
                realNumber = str(datetime.timedelta(seconds=number))
                newembedPlay = discord.Embed(
                    title=info["title"],
                    url=info["url"]
                )

                string = ""
                mathDuration = number / info["duration"] * 10
                if mathDuration < 1:
                    string = f"▶ ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ ({realNumber} / {realDuration})"
                elif mathDuration > 1 and mathDuration < 2:
                    string = f"▶ 🟥⬜⬜⬜⬜⬜⬜⬜⬜⬜ ({realNumber} / {realDuration})"
                elif mathDuration > 2 and mathDuration < 3:
                    string = f"▶ 🟥🟥⬜⬜⬜⬜⬜⬜⬜⬜ ({realNumber} / {realDuration})"
                elif mathDuration > 3 and mathDuration < 4:
                    string = f"▶ 🟥🟥🟥⬜⬜⬜⬜⬜⬜⬜ ({realNumber} / {realDuration})"
                elif mathDuration > 4 and mathDuration < 5:
                    string = f"▶ 🟥🟥🟥🟥⬜⬜⬜⬜⬜⬜ ({realNumber} / {realDuration})"
                elif mathDuration > 5 and mathDuration < 6:
                    string = f"▶ 🟥🟥🟥🟥🟥⬜⬜⬜⬜⬜ ({realNumber} / {realDuration})"
                elif mathDuration > 6 and mathDuration < 7:
                    string = f"▶ 🟥🟥🟥🟥🟥🟥⬜⬜⬜⬜ ({realNumber} / {realDuration})"
                elif mathDuration > 7 and mathDuration < 8:
                    string = f"▶ 🟥🟥🟥🟥🟥🟥🟥⬜⬜⬜ ({realNumber} / {realDuration})"
                elif mathDuration > 8 and mathDuration < 9:
                    string = f"▶ 🟥🟥🟥🟥🟥🟥🟥🟥🟥⬜ ({realNumber} / {realDuration})"
                elif mathDuration > 9:
                    string = f"▶ 🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥 ({realNumber} / {realDuration})"

                newembedPlay.set_thumbnail(url=info["thumbnail"])
                newembedPlay.add_field(
                    name=f"Поставил: {author.display_name}",
                    value=str(string),
                    inline=True
                )

                await message.edit(embed=newembedPlay)
                number = number + 10
                await asyncio.sleep(10)

            newembed1Play = discord.Embed(
                title=info["title"],
                url=info["webpage_url"]
            )   
            newembed1Play.set_thumbnail(url=info["thumbnail"])
            newembed1Play.add_field(
                name=f"Поставил: {author.display_name}",
                value=f"{realDuration} (Прослушано)",
                inline=True
            )

            await message.edit(embed=newembed1Play)
            if repeatMusic == False:
                queues.remove(my_data)

            can_playing=False  
            await queue_module(ctx, False)          

@bot.event
async def on_ready():
    print("Bot ready")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Узнай о мне - .info"))

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="Все команды",
        description="Вы можете отдельно написать команду с командой helper. Пример: .helper info"
    )

    embed.add_field(
        name="🔨 Модерация 🔨",
        value="`.clear` `.kick` `.unban` `.banlist` `.ban` `.addadmins` `.removeadmins` `.listadmins`",
        inline=False
    )
    embed.add_field(
        name="🎵 Музыка 🎵",
        value="`.join` `.leave` `.play` `.skip` `.queue` `.repeat`",
        inline=False
    )
    embed.add_field(
        name="📃 Информация 📃",
        value="`.info` `.helper`",
        inline=False
    )
    embed.add_field(
        name="😉 Прикольненькое 👍",
        value="`.ball8` `.dog` `.say` `.blackjack`",
        inline=False
    )


    await ctx.send(embed=embed)

@bot.command(pass_context = True)
async def clear(ctx, amount: int=100):
   find=False
   for role_id in admins_role:
    if role_id in [y.id for y in ctx.author.roles]:
        find=True
   
   if find==True:
    await ctx.channel.purge(limit = amount + 1)
    await ctx.send(f"Очищено {amount} сообщений!")
   else:
     await ctx.send("У вас нет не одной роли которая может управлять этой командой")

@bot.command(pass_context = True)
async def ban(ctx, member:discord.Member, *, reason=None):
   find=False
   for role_id in admins_role:
    if role_id in [y.id for y in ctx.author.roles]:
        find=True 

   if find==True:
    await member.send(f"Вы были забанены на сервере '{ctx.message.guild.name}' по причине: {reason}")
    await ctx.send(f"{member.name} был успешно забанен(а) на этом сервере по причине: {reason}") 
    await member.ban(reason=reason)
   else:
     await ctx.send("У вас нет не одной роли которая может управлять этой командой") 

@bot.command(pass_context = True)
async def unban(ctx, *, arg):
   find=False
   for role_id in admins_role:
    if role_id in [y.id for y in ctx.author.roles]:
        find=True 

   if find==True:
    banned_users = ctx.guild.bans()

    async for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.mention) == (arg):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} был(а) успешно разбанен(а)!")
            return
   else:
     await ctx.send("У вас нет не одной роли которая может управлять этой командой")  

@bot.command(pass_context = True)
async def banlist(ctx): 
   find=False
   for role_id in admins_role:
    if role_id in [y.id for y in ctx.author.roles]:
        find=True 

   if find==True:
    embed = discord.Embed(
        title="Бан лист",
        description="Список всех забаненых игроков на сервере"
    )

    banned_users = ctx.guild.bans()

    async for ban_entry in banned_users:
        user = ban_entry.user
        reason = ban_entry.reason

        embed.add_field(
            name=user.mention,
            value=f"Причина: {reason}",
            inline=False
        )

    
    await ctx.send(embed=embed)   
   else:
     await ctx.send("У вас нет не одной роли которая может управлять этой командой")          

@bot.command(pass_context = True)
async def kick(ctx, member:discord.Member, *, reason=None):
   find=False
   for role_id in admins_role:
    if role_id in [y.id for y in ctx.author.roles]:
        find=True 

   if find==True:
    await member.send(f"Вы были кикнуты с сервера '{ctx.guild.name}' по причине: {reason}")
    await ctx.send(f"{member.name} был успешно кикнут(а) с этого сервера по причине: {reason}")
    await member.kick(reason=reason)
   else:
     await ctx.send("У вас нет не одной роли которая может управлять этой командой")  

@bot.command()
async def helper(ctx, *, args):
   for commands_name, description_command in zip(commands_list, descriptions_for_commands):
    if args == commands_name:
        embedHelper = discord.Embed(
            title=commands_name,
            description=description_command
        )

        await ctx.send(embed=embedHelper)

@bot.command()
async def addadmins(ctx, *, args : int):
   if str(ctx.author.id) == str(ctx.guild.owner_id):
    Role = discord.utils.get(ctx.guild.roles, id=args)
    if Role:
     if Role.id in admins_role:
        await ctx.send(f"Роль <@&{Role.id}> уже находиться в списке админ ролей")
     else:
        await ctx.send(f"Роль <@&{Role.id}> успешно добавленна к админам ролям моих команд")
        admins_role.append(Role.id)
   else:
    await ctx.send("Добавлять, удалять и просматривать роли для моих админ команд может только создатель сервера!")

@bot.command()
async def listadmins(ctx):
   if str(ctx.author.id) == str(ctx.guild.owner_id):
    embedListadmins = discord.Embed(
       title="Все админы",
    )

    for role_id in admins_role:
     embedListadmins.add_field(
         name="\u200B",
         value=(f"<@&{role_id}>"),
         inline=False
     )

    await ctx.send(embed=embedListadmins)
   else:
    await ctx.send("Добавлять, удалять и просматривать роли для моих админ команд может только создатель сервера!")  

@bot.command()
async def removeadmins(ctx, *, args : int):
   if str(ctx.author.id) == str(ctx.guild.owner_id):
    Role = discord.utils.get(ctx.guild.roles, id=args)
    if Role.id in admins_role:
        await ctx.send(f"Роль <@&{Role.id}> успешно удалена из админ ролей моих команд")
        admins_role.remove(Role.id)
    else:
        await ctx.send(f"Роль <@&{Role.id}> не находиться в списке админ ролей")
   else:
    await ctx.send("Добавлять, удалять и просматривать роли для моих админ команд может только создатель сервера!")  

@bot.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Запрыгиваю на канал {channel}')

@bot.command()
async def say(ctx, *, args):
    if (ctx.author.voice):
        tts = gTTS(text=args, lang="ru")
        voice = get(bot.voice_clients, guild = ctx.guild)
        tts.save("voice.mp3")

        voice.play(discord.FFmpegPCMAudio("voice.mp3"))
    else:
        await ctx.send('Я не заметил чтоб ты был в голосовом канале')

@bot.command()
async def repeat(ctx):
    global repeatMusic

    if repeatMusic == False:
        repeatMusic = True
        await ctx.send("✅ Повторение музыки **ВКЛЮЧЕНО** ✅")   
    elif repeatMusic == True:
        repeatMusic = False
        await ctx.send("⛔ Повторение музыки **ВЫКЛЮЧЕНО** ⛔")   

@bot.command()
async def find(ctx, *, query):
    embed = discord.Embed(
      title=f"Результаты по запросу {query}",
    )
    
    author = ctx.author.mention
    await ctx.channel.send(f"Запрос в процессе, {author} !")
    async with ctx.typing():
        for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
            embed.add_field(
                name="\u200B",
                value=j,
                inline=False
            )  
    
    await ctx.send(embed=embed)  

@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'Я покинул канал {channel}')

@bot.command()
async def skip(ctx):
    voice = get(bot.voice_clients, guild = ctx.guild)
    if voice:
        voice.stop()
        await ctx.send('Текущая музыку пропущена')
    else:
        await ctx.send('Я не заметил где играла бы какая-нибудь музыка')

@bot.command()
async def queue(ctx):
   embedQueue = discord.Embed(
       title="Лист ожидания песен",
   )

   for data in queues:
    realDuration = str(datetime.timedelta(seconds=data["info"]["duration"]))

    embedQueue.add_field(
        name=data["info"]["title"],
        value=realDuration,
        inline=False
    )

   await ctx.send(embed=embedQueue)

@bot.command()
async def play(ctx, *, arg):
    if (ctx.author.voice):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            if 'https://' in arg:
                info = ydl.extract_info(arg, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]

        data = {}
        data["info"] = info
        data["author"] = ctx.author    

        queues.append(data)

        await ctx.send("Добавлен в список песен! Ожидайте очереди и скоро ваша песня заиграет")
        await asyncio.sleep(1)
        await queue_module(ctx, False)
    else:
        await ctx.send('Я не заметил чтоб ты был в головом канале')

@bot.command()
async def dog(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://random.dog/woof.json") as r:
                
            data = await r.json()
            embed = discord.Embed(                    
                title="Dog",
                color = ctx.author.color
            )

            embed.set_image(url=data['url'])
            await ctx.send(embed=embed)

@bot.command()
async def ball8(ctx, *, args):

    text = ""
    nmbr = rand.randint(1, 10)
    if nmbr == 1:
        text = "Определённо да 👍"
        
    if nmbr == 2:
        text = "Определённо нет 👎"

    if nmbr == 3:
        text = "Да ✅"

    if nmbr == 4:
        text = "Нет ❌"

    if nmbr == 5:
        text = "Если постараешься то это случиться 😉"

    if nmbr == 6:
        text = "На глупый вопрос глупый ответ 🙄"

    if nmbr == 7:
        text = "Спроси в другой раз 😶"

    if nmbr == 8:
        text = "Я не знаю ¯(О_О)¯"

    if nmbr == 9:
        text = "Сосредоточься и спроси ещё раз ⌛"

    if nmbr == 10:
        text = "50 на 50 😶"

    embed = discord.Embed(                    
        title=f"Вопрос: {args}",
        color = ctx.author.color,
        description=f"Ответ: {text}"
    )    

    await ctx.send(embed=embed)
    await ctx.message.add_reaction('❌')
    await ctx.message.add_reaction('✅')

@bot.command()
async def blackjack(ctx):
    myPlayerID = ctx.author.id

    embed = discord.Embed(                    
        title=f"Блек джек",
        color = ctx.author.color,
        description=f"Сейчас играет: {ctx.author.mention}"
    )

    playerNumbers = []
    randomCart1 = rand.randint(1, 10)
    playerNumbers.append(randomCart1)
    randomCart2 = rand.randint(1, 10)
    playerNumbers.append(randomCart2)
    playerString = ""
    playerNumber = 0
    for number in playerNumbers:
        text = ""
        if number == 1:
            text = "1️⃣"

        if number == 2:
            text = "2️⃣"

        if number == 3:
            text = "3️⃣"

        if number == 4:
            text = "4️⃣"

        if number == 5:
            text = "5️⃣"

        if number == 6:
            text = "6️⃣"

        if number == 7:
            text = "7️⃣"

        if number == 8:
            text = "8️⃣"

        if number == 9:
            text = "9️⃣"

        if number == 10:
            text = "🔟"  

        playerString = playerString + text
        playerNumber = playerNumber + number    

    embed.add_field(
        name="Ваши карты",
        value=f"{playerString} ({playerNumber})",
    )

    MyNumbers = []
    MyrandomCart = rand.randint(1, 10)
    MyNumbers.append(MyrandomCart)
    MyString = ""
    MyNumber = 0
    for number in MyNumbers:
        text = ""
        if number == 1:
            text = "1️⃣"

        if number == 2:
            text = "2️⃣"

        if number == 3:
            text = "3️⃣"

        if number == 4:
            text = "4️⃣"

        if number == 5:
            text = "5️⃣"

        if number == 6:
            text = "6️⃣"

        if number == 7:
            text = "7️⃣"

        if number == 8:
            text = "8️⃣"

        if number == 9:
            text = "9️⃣"

        if number == 10:
            text = "🔟"  

        MyString = MyString + text
        MyNumber = MyNumber + number    

    embed.add_field(
        name="Мои карты",
        value=f"{MyString}⬜ ({MyNumber})",
    )

    buttonPlus = Button(label="Взять карту", style=discord.ButtonStyle.primary, emoji="➕")
    buttonStop = Button(label="Остановиться", style=discord.ButtonStyle.primary, emoji="✖")
    myView = View()

    async def callback_Plus(interaction):
        if interaction.user.id == myPlayerID:
            
            AnotherRandomCart = rand.randint(1, 10)
            playerNumbers.append(AnotherRandomCart)
            playerString = ""
            playerNumber = 0
            for number in playerNumbers:
                text = ""
                if number == 1:
                    text = "1️⃣"

                if number == 2:
                    text = "2️⃣"

                if number == 3:
                    text = "3️⃣"

                if number == 4:
                    text = "4️⃣"

                if number == 5:
                    text = "5️⃣"

                if number == 6:
                    text = "6️⃣"

                if number == 7:
                    text = "7️⃣"

                if number == 8:
                    text = "8️⃣"

                if number == 9:
                    text = "9️⃣"

                if number == 10:
                    text = "🔟"  

                playerString = playerString + text
                playerNumber = playerNumber + number
            

            if playerNumber > 21:
                embed = discord.Embed(                    
                    title=f"Блек джек",
                    color = ctx.author.color,
                    description=f"Играл: {ctx.author.mention}"
                )

                embed.add_field(
                    name=f"Ваши карты: {playerString} ({playerNumber})",
                    value=f"Мои карты: {MyString}⬜ ({MyNumber})",
                )

                embed.add_field(
                    name="🔴 Вы проиграли! 🔴",
                    value="🟩 Я выиграл! 🟩",
                )

                await interaction.response.edit_message(embed=embed, view=None)
            else:
                embed = discord.Embed(                    
                    title=f"Блек джек",
                    color = ctx.author.color,
                    description=f"Сейчас играет: {ctx.author.mention}"
                )

                embed.add_field(
                    name="Ваши карты",
                    value=f"{playerString} ({playerNumber})",
                )

                embed.add_field(
                    name="Мои карты",
                    value=f"{MyString}⬜ ({MyNumber})",
                )  

                await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message("Это не ваша партия! Создайте свою если вам так хочеться :/", ephemeral=True)

        
    async def callback_Stop(interaction):
        if interaction.user.id == myPlayerID:  
            playerString = ""
            playerNumber = 0
            for number in playerNumbers:
                text = ""
                if number == 1:
                    text = "1️⃣"

                if number == 2:
                    text = "2️⃣"

                if number == 3:
                    text = "3️⃣"

                if number == 4:
                    text = "4️⃣"

                if number == 5:
                    text = "5️⃣"

                if number == 6:
                    text = "6️⃣"

                if number == 7:
                    text = "7️⃣"

                if number == 8:
                    text = "8️⃣"

                if number == 9:
                    text = "9️⃣"

                if number == 10:
                    text = "🔟"  

                playerString = playerString + text
                playerNumber = playerNumber + number    

            MyrandomCart = rand.randint(1, 10)
            MyNumbers.append(MyrandomCart)

            MyNumber = 0
            for number in MyNumbers:
                MyNumber = MyNumber + number

            if MyNumber < 18:
                MyrandomCart = rand.randint(1, 10)
                MyNumbers.append(MyrandomCart)

            MyNumber = 0
            for number in MyNumbers:
                MyNumber = MyNumber + number    

            if MyNumber < 18:
                MyrandomCart = rand.randint(1, 10)
                MyNumbers.append(MyrandomCart)

            MyNumber = 0
            for number in MyNumbers:
                MyNumber = MyNumber + number    

            if MyNumber < 18:
                MyrandomCart = rand.randint(1, 10)
                MyNumbers.append(MyrandomCart)        

            MyString = ""
            MyNumber = 0
            for number in MyNumbers:
                text = ""
                if number == 1:
                    text = "1️⃣"

                if number == 2:
                    text = "2️⃣"

                if number == 3:
                    text = "3️⃣"

                if number == 4:
                    text = "4️⃣"

                if number == 5:
                    text = "5️⃣"

                if number == 6:
                    text = "6️⃣"

                if number == 7:
                    text = "7️⃣"

                if number == 8:
                    text = "8️⃣"

                if number == 9:
                    text = "9️⃣"

                if number == 10:
                    text = "🔟"  

                MyString = MyString + text
                MyNumber = MyNumber + number       


            embed = discord.Embed(                    
                title=f"Блек джек",
                color = ctx.author.color,
                description=f"Играл: {ctx.author.mention}"
            )

            embed.add_field(
                name=f"Ваши карты: {playerString} ({playerNumber})",
                value=f"Мои карты: {MyString} ({MyNumber})",
            )
            if MyNumber > 21:
                embed.add_field(
                    name="🟩 Вы Выиграли! 🟩",
                    value="🔴 Я проиграл! 🔴",
                )
            else:
                if MyNumber > playerNumber:
                    embed.add_field(
                        name="🔴 Вы проиграли! 🔴",
                        value="🟩 Я выиграл! 🟩",
                    )
                elif MyNumber < playerNumber:
                    embed.add_field(
                        name="🟩 Вы Выиграли! 🟩",
                        value="🔴 Я проиграл! 🔴",
                    )
                elif MyNumber == playerNumber:
                    embed.add_field(
                        name="🟡 Ничья! 🟨",
                        value="🟨 Ничья! 🟡",
                    )


            await interaction.response.edit_message(embed=embed, view=None)   
        else:
            await interaction.response.send_message("Это не ваша партия! Создайте свою если вам так хочеться :/", ephemeral=True)


    buttonPlus.callback = callback_Plus
    buttonStop.callback = callback_Stop
    myView.add_item(buttonPlus)
    myView.add_item(buttonStop)

    await ctx.send(embed=embed, view=myView)


bot.run('ODYxMzAxODYwNjMwOTIxMjE2.GSvTik.LkJt4KvgvCQCdtAZS_LJlgG8Rbk5dY13SvplS8')
