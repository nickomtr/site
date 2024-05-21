import asyncpg
import asyncio
import json
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import time
import requests
import hypercorn
from hypercorn.asyncio import serve
#file = open('place.txt', 'r')
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
dsn = "postgresql://postgres:postgres@localhost:8008/postgres"
asyncio.DEFAULT_TIMEOUT = 60 
# Connect to the database using the connection string

import time
import aiohttp
servdata = 'version, lastsave, timecreated, online, tags, name, maxPlayers, password, seed, modification, id, psid, playing, playerinv, ac, currentp, ownerid, isPremium' #and id 16
col_names1 = ['version', 'lastsave', 'timecreated', 'online', 'tags', 'name', 'maxPlayers', 'password', 'seed', 'modification','id','psid', 'playing', 'playerinv', 'ac', 'currentp', 'ownerid', 'isPremium']
A = 'https://users.roblox.com/v1/users/31234143'

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, HTTPException, status, Body, Depends
from fastapi.staticfiles import StaticFiles
security = HTTPBasic()
app = FastAPI()
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.on_event("startup")
async def startup():

    app.db_pool = await asyncpg.create_pool(dsn)

@app.on_event("shutdown")
async def shutdown():
    app.db_pool.terminate()

@app.get("/spendrobux/{id}/{robux}")
async def spendrobux(request: Request, id, robux):
    async with app.db_pool.acquire() as conn:
        getter = await conn.fetchrow(f"""SELECT * FROM public.users WHERE "users"."UserId" = {id}""")
        if not getter:

            await conn.execute(f"""INSERT INTO "public"."users" ("UserId") VALUES ({id})""")
            return JSONResponse(content=jsonable_encoder({'details': "success"}))
        else:

            return JSONResponse(content=jsonable_encoder({'details': "fail"}))

@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/adduser/{id}")
async def adduser(request: Request, id):
    async with app.db_pool.acquire() as conn:
        getter = await conn.fetchrow(f"""SELECT * FROM public.users WHERE "users"."UserId" = {id}""")
        if not getter:

            await conn.execute(f"""INSERT INTO "public"."users" ("UserId") VALUES ({id})""")
            return JSONResponse(content=jsonable_encoder({'details': "success"}))
        else:

            return JSONResponse(content=jsonable_encoder({'details': "fail"}))


@app.get("/db")
async def setcode(request: Request):
    return templates.TemplateResponse("db.html", {"request": request})


@app.get("/uidtoname/{id}")
async def setcode(request: Request, id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://users.roblox.com/v1/users/{id}") as response:
            async with session.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={id}&size=352x352&format=Png&isCircular=false") as response2:
                resp = await response.json()
                resp2 = await response2.json()
                final =[resp,resp2]
                return JSONResponse(content=jsonable_encoder(final))



@app.get("/deleteuser/{userid}")
async def deleteuser(request: Request, userid):

    async with app.db_pool.acquire() as conn:
        await conn.execute(f"""DELETE FROM public.users WHERE "users"."UserId" = {userid}""")
    return JSONResponse(content=jsonable_encoder({'details': "success"}))



##
@app.get("/getplayerdata/{userid}")

async def getplayerdata(request: Request, userid):
    async with app.db_pool.acquire() as conn:
        getter = await conn.fetchrow(f"""SELECT * FROM public.users WHERE "users"."UserId" = {userid}""")
    if not getter:
        print('Player not found 404 GET')
        return JSONResponse(content=jsonable_encoder({'error': 'player not found'}))
    print(userid, ' got his data GET!')
    res = dict(getter)
    res['playerInventories'] = json.loads(res['playerInventories'])
    return JSONResponse(content=res)


@app.post("/setplayerdata")
async def setplayerdata(request: Request):
    playerid = request.headers.get('playerid')
    main_data = await request.body()
    print(playerid, ' got his data SET!')
    async with app.db_pool.acquire() as conn:
        getter = await conn.fetchrow(f"""SELECT * FROM public.users WHERE "users"."UserId" = {playerid}""")
        if not getter:
            await conn.execute(f"""INSERT INTO "public"."users" ("UserId","playerInventories", "playerGamepasses", "currentGame", "isBanned") VALUES ({playerid}, NULL,NULL, 1, FALSE)""")
        for k, v in json.loads(main_data).items():
            await conn.execute(f"""UPDATE "public"."users" SET "{k}" = '{v}' WHERE "users"."UserId" = {playerid};""")
    return JSONResponse(content=jsonable_encoder({'success': 'true'}))

@app.get("/games")
async def games(request: Request):
    async with app.db_pool.acquire() as conn:
            getter = await conn.fetch(f"""SELECT * FROM public.games""")
    getter = list(getter)
    res = []
    for id in getter:
        res.append(id[0])
    op = {index + 1: item for index, item in enumerate(res)}    
    print('Player got active games GET!')
    return JSONResponse(content=jsonable_encoder(op))



@app.post("/setserverdata")
async def SetServerData(request: Request):
    async with app.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            sid = request.headers.get('sid')
            main_data = await request.body()
            print(sid, ' -  serverID got data SET!')
            for k, v in json.loads(main_data).items():
                await cur.execute(f"""UPDATE "public"."worlds" SET "{k}" = '{v}' WHERE "worlds"."id" = {sid};""")
            
            return JSONResponse(content=jsonable_encoder({'success': 'true'}))                    



@app.post("/setserverdatapsid")
async def SetServerData(request: Request):
    async with app.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                psid = request.headers.get('psid')
                main_data = await request.body()
                print(psid, ' -  serverID_PSID got data SET!')

                for k, v in json.loads(main_data).items():
                    await cur.execute(f"""UPDATE "public"."worlds" SET "{k}" = '{v}' WHERE "worlds"."psid" = '{psid}';""")
                
                return JSONResponse(content=jsonable_encoder({'success': 'true'}))                    

            except:
                return JSONResponse(content=jsonable_encoder({'success': 'false'}))

@app.post("/CreateServer")
async def SetServerData(request: Request):
    ownerid = request.headers.get('ownerid')
    isPremium = request.headers.get('isPremium')
    async with app.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""SELECT * FROM public.worlds WHERE "worlds"."ownerid" = {ownerid} AND "worlds"."isPremium" = true;""")
            getter = await cur.fetchall()
            if getter:
                return JSONResponse(content=jsonable_encoder({'error': 'player'}))
            await cur.execute(f"""INSERT INTO "public"."worlds" ({servdata}) VALUES (NULL, NULL,NULL, NULL,NULL,'new server', NULL,NULL, NULL,NULL, DEFAULT,NULL,NULL, DEFAULT, NULL, 0, {int(ownerid)}, {isPremium}) RETURNING id""")
    id_of_new_row = await cur.fetchone()
    id_of_new_row = id_of_new_row[0]
    return JSONResponse(content=jsonable_encoder({'id': id_of_new_row}))

# @app.post("/DropServer")
# async def SetServerData(request: Request):
#     async with app.db_pool.acquire() as conn:
#         async with conn.cursor() as cur:
#             await cur.execute(f"""INSERT INTO "public"."worlds" ({servdata}) VALUES (NULL, NULL,NULL, NULL,NULL,'new server', NULL,NULL, NULL,NULL, NULL,NULL) RETURNING id""")
#             id_of_new_row = await cur.fetchone()
#             id_of_new_row = id_of_new_row[0]
#             await conn.close()
#             return JSONResponse(content=jsonable_encoder({'id': id_of_new_row}))

@app.get("/getserverlist/{desyatok}")
async def getserverlist(desyatok: int, name: str = False, sid: int = False, tags: str = False, psid: str = False):
    async with app.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            desyatok = int(desyatok)
            ert = desyatok * 10
            if tags:

                pass #to be added
            elif name:
                name_data = name
                await cur.execute(f"""SELECT * FROM public.worlds WHERE "worlds"."name" SIMILAR TO '%{name_data}%' ORDER BY "worlds"."playing" DESC LIMIT 10 OFFSET {ert-10}""")
                getter = await cur.fetchall()
                result = {}
                for i in range(0, len(getter)):
                    result[i] = {}
                    
                for j in range(0, len(getter)):
                    for i in range(0, len(col_names1)):
                        if getter[j][i] == None:
                            c = 'nil'
                            result[j][col_names1[i]] = c
                        else:
                            c = getter[j][i]
                            result[j][col_names1[i]] = c

                return JSONResponse(content=jsonable_encoder(result))
            elif sid:
                await cur.execute(f"""SELECT * FROM public.worlds WHERE "worlds"."id" = {sid}""")
                getter = await cur.fetchall()
                print(getter)
                result = {}
                for i in range(0, len(getter)):
                    result[i] = {}
                    
                for j in range(0, len(getter)):
                    for i in range(0, len(col_names1)):
                        if getter[j][i] == None:
                            c = 'nil'
                            result[j][col_names1[i]] = c
                        else:
                            c = getter[j][i]
                            result[j][col_names1[i]] = c

                return JSONResponse(content=jsonable_encoder(result))
            elif psid:
                await cur.execute(f"""SELECT * FROM public.worlds WHERE "worlds"."psid" = '{psid}' """)
                getter = await cur.fetchall()
                print(getter)
                result = {}
                for i in range(0, len(getter)):
                    result[i] = {}
                    
                for j in range(0, len(getter)):
                    for i in range(0, len(col_names1)):
                        if getter[j][i] == None:
                            c = 'nil'
                            result[j][col_names1[i]] = c
                        else:
                            c = getter[j][i]
                            result[j][col_names1[i]] = c

                return JSONResponse(content=jsonable_encoder(result))
            else:
                await cur.execute(f"""SELECT * FROM public.worlds ORDER BY "worlds"."playing" DESC OFFSET {ert-10} LIMIT 10""")
                getter = await cur.fetchall()
                print(getter)
                result = {}
                for i in range(0, len(getter)):
                    result[i] = {}
                    
                for j in range(0, len(getter)):
                    for i in range(0, len(col_names1)):
                        if getter[j][i] == None:
                            c = 'nil'
                            result[j][col_names1[i]] = c
                        else:
                            c = getter[j][i]
                            result[j][col_names1[i]] = c
                await conn.close()
                return JSONResponse(content=jsonable_encoder(result))


config = hypercorn.Config()
config.bind = ["192.168.1.77:443", "192.168.1.77:80"] #192.168.1.254:8009 - 192.168.1.77:8009

config.workers = 5
asyncio.run(serve(app, config))