import discord
import aiopg
import json
from discord.ext import commands
import asyncio
from discord import app_commands
import requests
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
bot = commands.Bot(command_prefix=':',intents = discord.Intents.all())

ALLOWED_ROLE_IDS = ['1056622070374600807', '981685248913973348']
DATABASE_URL = 'postgresql://postgres:postgres@localhost:8008/postgres'
group_holder_cookie = '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_7E1510D294986B99485A727C9E924AB0F3DCE1E88C4110624F0C7752AF97AE390912A4017D2A9B3A8CB95E9A04C6A216ED574C6C60CBB20838A0390820A944AD0C5A07A4BEF959EDDF255EC3E86E4E5E42B7C91F0D83ED73B27B24DD03F5634E736285BB592A8AD465D2D76B78CAEB1311A8D6C1F26157B946C40A4D23260667E7B167F5920A19FD49C3E2F12EC9A673CED5D29885052A61E667B09512EDB1CE447BB002C67C8B6656D0113AEE3F770D1CA380C9905378E20A8190DDAE5537A2255A1BF8311EEF8BCF22496BED484CEAEBBF9C579C4250E660B8699954082CE464B05FA77F443305AA7867FE3BE11AA07BD6868F37933788BF9A7A92415FB48331197AA7894235BFE224B283139046F8B9A4CA76C6226A2F20D5709AEB1A77B932418D5AAE305701B95B658E0834A24636B90B8C60D6C06742F821C88F30C9ECF699D03F08C6BC592AA6A82974D2C7B7D67AFF9FBE1D03C579BAD72CD912A045265C0DFE4A8897DE30F52F713CE56B379626DF0FC186ED123356EF2D712B86507F5B498D0E387697CA6FE3178115B732C9F1C52A49120F5B26769131242181F1FB7FB35EE3C36F5D171A3709AD22E22AF2F08F672BFD877E147D3E64752AB1FB5081D5E9B466594EBF3C092402A58CFEF043132D483CEA9E4F5F0A57D789391B45440C7120E8D78D1D40908CB0AF1F6CFDDE0A1EF623049C3633618BF80E17F28BD7DC56132C3ABF6156E570439DD8750562EAAC1A819C1DE7A38CEBE2DCADA6B772E295FE6AE8C988B2CE6033F50548467DDA74D3A246A9F4A63B971633C89587EB60AABCB798C31D210E72970B6435C2046C05837A8CDA4F6E7104AAB630D5A7E806B907C86FA2615DCAB6F0AD9208195CD27A1C718D9F8A1290CEE9BEF915918EA461C46EF5E0D6F2C8F310224C7E970C6C7EBB208E9A5FEF0AD2D2D1CA1A629C01D3AB1DAD56F580878A9CB4485AC5630E9756314ECA7972107A05A27ADF0BBCA1479C9A4099645E62FB3E89CAF6EC29322055C93800A25A6D9ABCDD9E5ABD71E52C'
products = {
    "products": [
        {
            "name": "Diamond",
            "price": 21
        },
        {
            "name": "Diamond Axe",
            "price": 44
        },
        {
            "name": "Diamond Boots",
            "price": 50
        },
        {
            "name": "Diamond Chestplate",
            "price": 100
        },
        {
            "name": "Diamond Helmet",
            "price": 63
        },
        {
            "name": "Diamond Leggings",
            "price": 88
        },
        {
            "name": "Diamond Pickaxe",
            "price": 44
        },
        {
            "name": "Diamond Sword",
            "price": 36
        },
        {
            "name": "Gold Ingot",
            "price": 10
        },
        {
            "name": "Golden Sword",
            "price": 27
        },
        {
            "name": "Steel Axe",
            "price": 21
        },
        {
            "name": "Steel Boots",
            "price": 28
        },
        {
            "name": "Steel Chestplate",
            "price": 56
        },
        {
            "name": "Steel Helmet",
            "price": 34
        },
        {
            "name": "Steel Ingot",
            "price": 10
        },
        {
            "name": "Steel Leggings",
            "price": 48
        },
        {
            "name": "Steel Pickaxe",
            "price": 21
        },
        {
            "name": "Steel Sword",
            "price": 18
        },
        {
            "name": "Ruby Axe",
            "price": 56
        },
        {
            "name": "Ruby Boots",
            "price": 64
        },
        {
            "name": "Ruby Chestplate",
            "price": 128
        },
        {
            "name": "Ruby Ingot",
            "price": 27
        },
        {
            "name": "Ruby Helmet",
            "price": 80
        },
        {
            "name": "Ruby Leggings",
            "price": 99
        },
        {
            "name": "Ruby Pickaxe",
            "price": 56
        },
        {
            "name": "Ruby Sword",
            "price": 38
        },
        {
            "name": "Sapphire Ingot",
            "price": 66
        },
        {
            "name": "Sapphire Sword",
            "price": 99

        },
        {
            "name": "Sapphire Pickaxe",
            "price": 92

        },
        {
            "name": "Ruby Sword",
            "price": 62

        },
        {
            "name": "x32 torches",
            "price": 14
        },
        {
            "name": "x64 brick",
            "price": 18

        },
        {
            "name": "x64 glass",
            "price": 18

        },
        {
            "name": "x64 oak planks",
            "price": 18

        }
    ]
}


@bot.event
async def on_ready():

    print("Ready!")

import time

@bot.command()
async def hello(ctx):   
    await ctx.send('hi !')

@bot.command(name='add_item', description = "[REDACTED]")
@commands.has_role(1056622070374600807)
async def add_item(ctx, player_id: int, item:str, quantity:int, durability: int=None):
    print(ctx)
    async with aiopg.create_pool(DATABASE_URL) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""SELECT * FROM public.users WHERE "users"."UserId" = {player_id}""")
                result = await cur.fetchone()
                if result is not None:
                    inventory = result[1]
                    output = inventory
                    for slot, val in inventory.items():
                        val = json.loads(val)
                        if val["name"] == "":
                            await ctx.channel.send(f'Player {player_id} backpack was checked and found free slot.')
                            toc = json.loads(output[slot])
                            toc["name"] = item
                            toc["count"] = int(quantity)
                            if durability:
                                toc["durability"] = durability
                            else:
                                toc["durability"] = False
                            ans = json.dumps(toc)
                            output[slot] = ans
                            output = json.dumps(output)
                            rsp = await cur.execute(f"""UPDATE "public"."users" SET "playerInventories" = '{output}' WHERE "users"."UserId" = {player_id};""")
                            print(output)
                            embed = discord.Embed(title='ZetaSystem Server System', description='SUCCESS', color=discord.Color.green())
                            await ctx.send(embed=embed)
                            break
                else:
                    embed = discord.Embed(title='ZetaSystem Server System', description='FAILURE', color=discord.Color.red())
                    await ctx.send(embed=embed)
                    await ctx.channel.send(f'Player {player_id} not found in the database')
                await conn.close()
                pool.terminate()
                await pool.wait_closed()

@bot.command(name='add_place', description = "[REDACTED]")
@commands.has_role(1056622070374600807)
async def add_place(ctx, id: int):
    async with aiopg.create_pool(DATABASE_URL) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""SELECT * FROM "public"."games" WHERE "games"."id" = {id}""")
                result = await cur.fetchone()
                if result:
                    embedfail = discord.Embed(title='ZetaSystem Server System', description='Game Exists.', color=discord.Color.red())
                    await ctx.send(embed=embedfail)
                else:
                    await cur.execute(f"""INSERT INTO "public"."games" ("id") VALUES ({id})""")
                    embeds = discord.Embed(title='ZetaSystem Server System', description=f'Place with id - {id} is created.', color=discord.Color.green())
                    await ctx.send(embed=embeds)
@bot.command(name='delete_place', description = "[REDACTED]")
@commands.has_role(1056622070374600807)
async def delete_place(ctx, id: int):
    async with aiopg.create_pool(DATABASE_URL) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""SELECT * FROM "public"."games" WHERE "games"."id" = {id}""")
                result = await cur.fetchone()
                if result:
                    await cur.execute(f"""DELETE FROM "public"."games" WHERE "games"."id" = {id}""")
                    embedfail = discord.Embed(title='ZetaSystem Server System', description='Place deleted.', color=discord.Color.green())
                    await ctx.send(embed=embedfail)
                else:
                    embeds = discord.Embed(title='ZetaSystem Server System', description=f'Place - {id} is not found.', color=discord.Color.red())
                    await ctx.send(embed=embeds)
@bot.command(name = "list_places", description = "[REDACTED]")
@commands.has_role(1056622070374600807)
async def list_places(ctx):
    async with aiopg.create_pool(DATABASE_URL) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""SELECT * FROM "public"."games" """)
                result = await cur.fetchall()
                embeds = discord.Embed(title='ZetaSystem Server System', description=f'Available palces - {result}', color=discord.Color.light_grey())
                await ctx.send(embed=embeds)
@bot.command(name = "ban", description = "Use to ban player from ZetaSystem.")
@commands.has_role(1056622070374600807)
async def ban(ctx, id: int):
    async with aiopg.create_pool(DATABASE_URL) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""SELECT * FROM "public"."users" WHERE "users"."UserId" = {id}""")
                result = await cur.fetchone()
                if not result:
                    embedfail = discord.Embed(title='ZetaSystem Server System', description='Player does not exist. Pre-banning is to be added.', color=discord.Color.red())
                    await ctx.send(embed=embedfail)
                else:
                    rsp = await cur.execute(f"""UPDATE "public"."users" SET "isBanned" = TRUE WHERE "users"."UserId" = {id};""")
                    embeds = discord.Embed(title='ZetaSystem Server System', description=f'Player was banned!', color=discord.Color.red())
                    await ctx.send(embed=embeds)

# @app_commands.command(name = "Delete DB entry", description = "Use to fully delete player object from DB", guild=discord.Object(id=977180123876966491))
# @commands.has_role(1056622070374600807)
# async def clear(ctx, id):
#     async with aiopg.create_pool(DATABASE_URL) as pool:
#         async with pool.acquire() as conn:
#             async with conn.cursor() as cur:
#                 await cur.execute(f"""SELECT * FROM "public"."users" WHERE "users"."UserId" = {id}""")
#                 result = await cur.fetchone()
#                 if not result:
#                     embedfail = discord.Embed(title='ZetaSystem Server System', description='Player does not exist.', color=discord.Color.red())
#                     await ctx.send(embed=embedfail)
#                 else:
#                     rsp = await cur.execute(f"""UPDATE "public"."users" SET "playerInventories" = NULL WHERE "users"."UserId" = {id};""")
#                     embeds = discord.Embed(title='ZetaSystem Server System', description=f'Player was inventory removed!', color=discord.Color.red())
#                     await ctx.send(embed=embeds)

@bot.command(name = "delete_entry_db", description = "Use to fully delete player object from DB, player inventory.")
@commands.has_role(1056622070374600807)
async def delete_entry_db(ctx, id: int):
    async with aiopg.create_pool(DATABASE_URL) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""SELECT * FROM "public"."users" WHERE "users"."UserId" = {id}""")
                result = await cur.fetchone()
                if not result:
                    embedfail = discord.Embed(title='ZetaSystem Server System', description='Player does not exist.', color=discord.Color.red())
                    await ctx.send(embed=embedfail)
                else:
                    rsp = await cur.execute(f"""DELETE FROM "public"."users" WHERE "users"."UserId" = {id}""")
                    embeds = discord.Embed(title='ZetaSystem Server System', description=f'Player entry was deleted from DB!', color=discord.Color.red())
                    await ctx.send(embed=embeds)



@bot.command(name = "unban", description = "Use to unban player from ZetaSystem.")
@commands.has_role(1056622070374600807)
async def unban(ctx, id: int):
    async with aiopg.create_pool(DATABASE_URL) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""SELECT * FROM "public"."users" WHERE "users"."UserId" = {id}""")
                result = await cur.fetchone()
                if not result:
                    embedfail = discord.Embed(title='ZetaSystem Server System', description='Player does not exist.', color=discord.Color.red())
                    await ctx.send(embed=embedfail)
                else:
                    rsp = await cur.execute(f"""UPDATE "public"."users" SET "isBanned" = FALSE WHERE "users"."UserId" = {id};""")
                    embeds = discord.Embed(title='ZetaSystem Server System', description=f'Player was unbanned!', color=discord.Color.green())
                    await ctx.send(embed=embeds)
@bot.command(name = "create_products", description = "Use to auto-create dev products for game.")
@commands.has_role(1056622070374600807)
async def create_products(ctx, id: int):
    embeds = discord.Embed(title='ZetaSystem Server System', description='Called-Step1-INIT', color=discord.Color.light_grey())
    await ctx.send(embed=embeds)

    session = requests.session()
    session.cookies[".ROBLOSECURITY"] = group_holder_cookie
    request1 = session.post(url="https://auth.roblox.com/")
    if "X-CSRF-Token" in request1.headers: 
        session.headers["X-CSRF-Token"] = request1.headers["X-CSRF-Token"]
    request2 = session.post(url="https://auth.roblox.com/")
    embeds = discord.Embed(title='ZetaSystem Server System', description='Called-Step2-XCRSF', color=discord.Color.light_grey())
    await ctx.send(embed=embeds)
    unid = session.get(f'https://apis.roblox.com/universes/v1/places/{id}/universe').json()['universeId']
    embeds = discord.Embed(title='ZetaSystem Server System', description='Called-Step3-UID', color=discord.Color.light_grey())
    await ctx.send(embed=embeds)
    for item in products["products"]:
        name = item['name']
        price = item['price']
        created = False
        count = 3
        while created == False:
            ans = session.post(f'https://apis.roblox.com/developer-products/v1/universes/{unid}/developerproducts?name={name}&description=null&priceInRobux={price}')
            print(ans.content)
            if ans.status_code == 403:
                created = False
                count -= 1
            else:
                created = True
            if count == 0:
                embeds = discord.Embed(title='ZetaSystem Server System', description='Contact bot dev, error.', color=discord.Color.red())
                await ctx.send(embed=embeds)
                raise 'ErrorWithAPIRequestContactDrmmrk'
    embeds = discord.Embed(title='ZetaSystem Server System', description='Called-Step4-AuthLVL4-FINISH', color=discord.Color.green())
    await ctx.send(embed=embeds)
    session.close()






bot.run('')