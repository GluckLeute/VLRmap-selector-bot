import discord
from discord.ext import commands
import random
from config import TOKEN

ALL_MAPS = ["ASCENT","BIND","SPLIT","HAVEN","ICEBOX","BREEZE","FRACTURE","PEARL","LOTUS"]
MAP_DICT =  {
         "1": "ASCENT",
        "2": "SPLIT",
        "3": "HAVEN",
        "4": "BIND",
        "5": "ICEBOX",
        "6": "BREEZE",
        "7": "FRACTURE",
        "8": "PEARL",
        "9": "LOTUS"
        }
maplist = ALL_MAPS[:]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# BOT起動成功
@bot.event
async def on_ready():
    print('success')

@bot.event
async def on_message(message):
    await bot.process_commands(message)

# pingコマンド
@bot.command()
async def ping(ctx):
    await ctx.send("PONG!")

@bot.command()
async def init(ctx):
    global maplist
    maplist = ALL_MAPS[:]
    await ctx.send("maplistを初期化しました")

@bot.command()
async def m_list(ctx):
    maps_str = "\n".join(maplist)
    await ctx.send(f"現在のマップ一覧:\n{maps_str}")

@bot.command()
async def m_num(ctx):
    msg = "マップナンバー一覧:\n"
    for number, name in MAP_DICT.items():
        msg += f"{number}: {name}\n"
    await ctx.send(msg)

@bot.command()
async def m_ban(ctx, *maps):
    try:
        banlist = []
        for item in maps:
            if item in MAP_DICT:
                banlist.append(MAP_DICT[item])
            else:
                if item.upper() in MAP_DICT.values():
                    banlist.append(item.upper())
                else:
                    await ctx.send(f"不正な入力です: {item}")
                    return

        global maplist
        maplist = [map_name for map_name in maplist if map_name not in banlist]

        await ctx.send("以下のMAPはBANされました.\n" + str(banlist).replace('\'', ''))

    except Exception as e:
        await ctx.send(f'エラーが発生しました: {str(e)}')

@bot.command()
async def map(ctx, n:int):
    if n <= 0:
        await ctx.send("1以上の数を指定してください")
    elif len(maplist) >= n:
        randommap = random.sample(maplist, n)
        await ctx.send(str(n)+"つのMAPが選ばれました.\n"+ str(randommap).replace('\'',''))
    elif len(maplist) < n:
        await ctx.send("MAP数より多い値が指定されました.")

bot.run(TOKEN)
