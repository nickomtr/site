from discord import *
import discord

from discord.ext import commands
import requests
import asyncio
import json

import sqlite3

from bit import PrivateKey, wif_to_key, PrivateKeyTestnet

from bit.network import NetworkAPI, satoshi_to_currency, currency_to_satoshi

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from discord.ext import tasks
import time
import qrcode
from PIL import Image
import io
import numpy as np
from datetime import datetime
def format_float(num):
    return np.format_float_positional(num, trim='-')

#listen to transactions

EmbedClose = discord.Embed(title='Close Deal', description='*Requires confirmation from both parties.\n`Sender:` ❌\n`Receiver:` ❌*', color=discord.Color.red())
EmbedClose1 = discord.Embed(title='Close Deal', description='*Requires confirmation from both parties.\n`Sender:` ✅\n`Receiver:` ❌*', color=discord.Color.red())
EmbedClose2 = discord.Embed(title='Close Deal', description='*Requires confirmation from both parties.\n`Sender:` ❌\n`Receiver:` ✅*', color=discord.Color.red())
serverr = 1059857006158168115
categg = 1079121613573865504
 
con = sqlite3.connect("fastdb.db")


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None
        self.value = None
    @discord.ui.button(style=ButtonStyle.primary,custom_id="menu",label="Use Service.",emoji='<:Bitcoin:1060605946017103923>')
    async def main(self, interaction: discord.Interaction, button: discord.ui.Button,):
        
        await interaction.response.send_message('Creating inquiry...', ephemeral=True)
        
        category = discord.utils.get(interaction.guild.categories, id=categg)
        cur = con.cursor()
        


        overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True),
        }
        
        havealreadyinquires = cur.execute(f"select * from inquires where sender = {interaction.user.id} and closed = 0")
        havealreadyinquires = havealreadyinquires.fetchone()
        print(havealreadyinquires)
        if havealreadyinquires:
            await interaction.edit_original_response(content='Inquiry was not created as you have one already.')
        else:
            await interaction.edit_original_response(content='Inquiry created.')
            res = cur.execute(f"INSERT INTO inquires (sender, receiver, type, barter, paymenttype, receiverpayinfo, senderpayinfo,closed, usd, agree, pk, pubkey, transmes, crypto_price, confirm, confsent) VALUES ({interaction.user.id}, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, 0, NULL, NULL, NULL, NULL, 0, 0) RETURNING id;")
            res = res.fetchone()[0]
            con.commit()
            ##cur.close()
            await interaction.guild.create_text_channel(f'Inquiry-{res}', category=category, overwrites=overwrites)

class Dropdown(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None
    options = [
            discord.SelectOption(label='Bitcoin', description='One of the most popular crypto.', emoji='🟡'),
            #discord.SelectOption(label='USDT', description='Nice stable coin.', emoji='🟢💲'),
            #discord.SelectOption(label='Ethernium', description='Crypto Currency.', emoji='🔵💎'),
    ]

        
    @discord.ui.select(placeholder='Choose...', min_values=1, max_values=1, options=options,custom_id='select')
    async def callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        crypto = select.values[0]
        #if interaction.user.id != 
        await interaction.message.delete()
        await interaction.channel.send(f'Crypto was chosen - {crypto}.', delete_after=5)
        if crypto == "Bitcoin":
            cur = con.cursor()
            cur.execute(f"UPDATE inquires SET paymenttype = 'Bitcoin' WHERE id = {interaction.channel.name.split('-')[1]}")
            con.commit()
            #cur.close()
            embed = discord.Embed(title='*Escrow* System | Bitcoin 🟡', description=f'Welcome both parties into our Escrow System, please **sender** specify the ammount of **United States Dollars** that the item will be sold for. (simply type the number of USD, without anything else).\n\n💰 USD will be converted in BTC with the latest exchange course.', color=discord.Color.gold())
            await interaction.channel.send(embed=embed)
class DealType(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None
        self.value = None
    @discord.ui.button(style=ButtonStyle.primary,custom_id="dealtypebarter",label="Barter.",emoji='🛍')
    async def barter(self, interaction: discord.Interaction, button: discord.ui.Button):
        cur = con.cursor()
        res = cur.execute(f"Select * from inquires where id = {interaction.channel.name.split('-')[1]};")
        res = int(res.fetchone()[0])
        if res == interaction.user.id:
            await interaction.message.delete()
            await interaction.channel.send('Deal type barter was selected, staff will be required for it for futher proccessing, bot will not interfere with this inquiry from so on, you can only !close.')
            cur.execute(f"Update inquires set barter = 1 where id = {interaction.channel.name.split('-')[1]};")
            con.commit()
        else:
            await interaction.response.send_message('Only sender is authorized to select it.', ephemeral=True)
        #cur.close()
    @discord.ui.button(style=ButtonStyle.primary,custom_id="dealtypecrypto",label="Crypto Sale.",emoji='🛒')
    async def crypto(self, interaction: discord.Interaction, button: discord.ui.Button):
        cur = con.cursor()
        res = cur.execute(f"Select * from inquires where id = {interaction.channel.name.split('-')[1]};")
        res = int(res.fetchone()[0])
        if res == interaction.user.id:
            await interaction.message.delete()
            await interaction.channel.send('Deal type crypto was selected, staff will be required for only during conflict situation.', delete_after=5)
            embed = discord.Embed(title='*Escrow* System', description=f'Select your payment type.| Inq. ID - *#{id}* | !close', color=discord.Color.blurple())
            await interaction.channel.send(embed=embed, view=Dropdown())
            cur.execute(f"Update inquires set barter = 0 where id = {interaction.channel.name.split('-')[1]};")
            con.commit()
        else:
            await interaction.response.send_message('Only sender is authorized to select it.', ephemeral=True)
        #cur.close()
class Bitcoin(discord.Embed):

    def qrcallback(self):
        return self.qr_file

    def __init__(self, channel: discord.TextChannel):
        id = channel.name.split('-')[1]
        key = PrivateKey()
        cur = con.cursor()
        res = cur.execute(f"Select * from inquires where id = {id};")
        res = res.fetchone()
        cur.execute(f"Update inquires set pubkey = '{key.address}' where id = {id}")
        cur.execute(f"Update inquires set pk = '{key.to_wif()}' where id = {id}")
        bitcoin_amount = float(currency_to_satoshi(int(res[8]), 'usd') / 100000000)
        c = format_float(bitcoin_amount)

        cur.execute(f"Update inquires set crypto_price = '{c}' where id = {id}")
        con.commit()
        #cur.close()






        qr = qrcode.QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(f'bitcoin:{key.address}?amount={c}')
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image = qr_image.resize((300, 300))
        buffer = io.BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)
        self.qr_file = File(buffer,filename='img.png')

        self.set_image(url='attachment://img.png')
    
        super().__init__(title='*Escrow* System | Crypto Module | Bitcoin 🟡', description=f"Please, send BTC to this address - **{key.address}**, exactly **`{c} BTC`**.\n If you sent less it is OK, you must send enough so it reaches {c}. If you send more, the crypto will simply be deleted and it cannot be refunded.", color=discord.Color.gold(), url = "")     
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None
        self.value = None
    @discord.ui.button(style=ButtonStyle.green,custom_id="Agree",label="Agree.",emoji='✅')
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        cur = con.cursor()
        res = cur.execute(f"Select * from inquires where id = {interaction.channel.name.split('-')[1]};")
        res = res.fetchone()
        if int(res[1]) == interaction.user.id or interaction.user.id == 737381104935370793:
            await interaction.message.delete()
            cur.execute(f"Update inquires set agree = 1 where id = {interaction.channel.name.split('-')[1]};")
            
            embed = discord.Embed(title=f'Escrow System | General Deal Confirmation', description=f'Receiver Agreed ✅. Sender you will now be required to send Bitcoin. \n\n Note: Always make sure you are sending the bitcoin in **our** secured automated wallet.', color=discord.Color.green())
            await interaction.channel.send(embed=embed)
            prompt = Bitcoin(interaction.channel)
            await interaction.channel.send(embed=prompt, file=prompt.qrcallback())
            Bank = discord.Embed(title=f'Escrow System | Deposit', description='Will be updated in ~5 seconds.', color=discord.Color.orange())
            msg = await interaction.channel.send(embed=Bank)
            await msg.pin()

            cur.execute(f"Update inquires set transmes = {msg.id} where id = {interaction.channel.name.split('-')[1]};")


            con.commit()
            #cur.close()
        else:
            await interaction.response.send_message('Unauthorized.', ephemeral=True)
        con.commit()
class PayoutForm(discord.ui.Modal,title="Payout"):
    def __init__(self):
        super().__init__(timeout=None)

        self.name = discord.ui.TextInput(
                label="Your public key of crypto wallet.",
                min_length=2,
                max_length=50,
                custom_id='payoutformtextinput'
        )
        self.add_item(self.name)
    async def on_submit(self, interaction: discord.Interaction):
        cur = con.cursor()
        res = cur.execute(f"Select * from inquires where id = {interaction.channel.name.split('-')[1]};")
        res = res.fetchone()
        if int(res[0]) == interaction.user.id:
            tx = PrivateKey(res[10]).send([], leftover=self.name.value)
            
            embed1 = discord.Embed(title='*Escrow* System | Payout 🌐', description=f'Sent. Transaction hash **{tx}**. Ticket Closed.', color=discord.Color.green())

            embed2 = discord.Embed(title='*Escrow* System | 👋', description=f'Thank you for using our service.', color=discord.Color.green())
            cur.execute(f"Update inquires set closed = 1 where id = {interaction.channel.name.split('-')[1]};")
            con.commit()
            await interaction.channel.send(embed=embed1)
            await interaction.channel.send(embed=embed2)
        else:
            await interaction.response.send_message('Unauthorized.', ephemeral=True)
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Most likely crypto address is invalid.', ephemeral=True)

    
class SendCrypto(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None
        self.value = None
    @discord.ui.button(style=ButtonStyle.blurple,custom_id="addr",label="Select Address.",emoji='🌐')
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        cur = con.cursor()
        res = cur.execute(f"Select * from inquires where id = {interaction.channel.name.split('-')[1]};")
        res = res.fetchone()
        if int(res[1]) == interaction.user.id or interaction.user.id == 737381104935370793:
            await interaction.response.send_modal(PayoutForm())
        else:
            await interaction.response.send_message('Unauthorized.', ephemeral=True)
        con.commit()
        #cur.close()
class Payout(discord.Embed):
    def __init__(self):
        super().__init__(title='*Escrow* System | Payout 🌐', description=f"Please, receiver send your BTC address.", color=discord.Color.blue())
class ConfirmDeal(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None
        self.value = None
    @discord.ui.button(style=ButtonStyle.green,custom_id="confirmdeal",label="Confirm.",emoji='✅')
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        cur = con.cursor()
        res = cur.execute(f"Select * from inquires where id = {interaction.channel.name.split('-')[1]};")
        res = res.fetchone()
        if int(res[0]) == interaction.user.id or interaction.user.id == 737381104935370793:
            print(interaction.channel.id)
            await interaction.channel.send(embed=Payout(), view=SendCrypto())
            await interaction.message.delete()
            cur.execute(f"Update inquires set confirm = 1 where id = {interaction.channel.name.split('-')[1]};")
        else:
            await interaction.response.send_message('Unauthorized.', ephemeral=True)
        con.commit()
        #cur.close()
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()


        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)

    async def setup_hook(self) -> None:

        self.add_view(Menu())
        self.add_view(DealType())
        self.add_view(Dropdown())
        self.add_view(Confirm())
        self.add_view(ConfirmDeal())
        self.add_view(SendCrypto())
        self.add_view(PayoutForm())
        self.add_view(Close())
class Close(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None
        self.value = None
    @discord.ui.button(style=ButtonStyle.green,custom_id="close",label="Agree.",emoji='✔')
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        cur = con.cursor()
        res = cur.execute(f"Select * from inquires where id = {interaction.channel.name.split('-')[1]};")
        res = res.fetchone()

        if int(res[1]) == interaction.user.id:
            if interaction.message.embeds[0] == EmbedClose1:
                await interaction.message.delete()
                await interaction.channel.send('Ticket Closed!')
                cur.execute(f"Update inquires set closed = 1 where id = {interaction.channel.name.split('-')[1]};")
            await interaction.message.edit(embed=EmbedClose2)
        else:
            if interaction.message.embeds[0] == EmbedClose2:
                await interaction.message.delete()
                await interaction.channel.send('Ticket Closed!')
                cur.execute(f"Update inquires set closed = 1 where id = {interaction.channel.name.split('-')[1]};")
                
            await interaction.message.edit(embed=EmbedClose1)
        con.commit()
        #cur.close()
bot = Bot()






@tasks.loop(seconds = 10)
async def UpdateBTC():

    cur = con.cursor()
    start = cur.execute(f"SELECT * FROM inquires WHERE confsent = 0 AND closed = 0 AND crypto_price IS NOT NULL")
    start = list(start.fetchall())
    for inq in start:

        msg_id = inq[12]
        crypto = inq[13]
        unspents1 = PrivateKey(inq[10]).get_unspents()
        min_conf = 1
        unspents = [u.txid for u in unspents1]
        confirmed_unspents = [u for u in unspents1 if u.confirmations >= min_conf]
        balance = sum(u.amount for u in confirmed_unspents)
        channel = discord.utils.get(bot.get_guild(serverr).channels, name=f'inquiry-{inq[16]}')

        if msg_id is None or channel is None:
            return

        msg = await channel.fetch_message(msg_id)
        if float(balance) >= crypto:
            embed = discord.Embed(title=f'Escrow System | Deposit', description=f'{format_float(float(balance/100000000))}/{format_float(float(crypto))} BTC. Enough sent, 1 confirmation received.', color=discord.Color.green())
            await msg.edit(embed=embed)
            cur.execute(f"Update inquires set transmes = NULL where id = {inq[16]};")
            embed = discord.Embed(title=f'Escrow System | GENERAL CONFIRMATION', description=f'The cryptocurrency was received. Now, sender must confirm item receival.\n*NOTE: This action is final.*', color=discord.Color.red())
            await channel.send(embed=embed, view=ConfirmDeal())
            cur.execute(f"Update inquires set confsent = 1 where id = {inq[16]};")
        else:
            embed = discord.Embed(title=f'Escrow System | Deposit', description=f'{format_float(float(balance))}/{format_float(float(crypto))} BTC.\nTransaction(s) Detected: {", ".join(unspents)}', color=discord.Color.orange(), timestamp=datetime.now())
            await msg.edit(embed=embed)
    con.commit()
    #cur.close()





@bot.command()
async def hello(ctx):   
    
    await ctx.send('hi')

@bot.listen()
async def on_ready():
    UpdateBTC.start()

@bot.command()
async def g(ctx):   
    embed = discord.Embed(title='Automated Middleman Service', description='The service currently supports: bitcoin. If you want to use the service, click the "Use Service." button bellow.', color=discord.Color.blurple())
    await ctx.send(embed=embed, view=Menu())

@bot.command()
async def close(ctx):
    category_tickets = discord.utils.get(ctx.guild.categories, id=categg)
    if ctx.channel.category == category_tickets:
        await ctx.send(embed=EmbedClose, view=Close())
@bot.command()
async def force_close(ctx, arg):
    cur = con.cursor()
    cur.execute(f"Update inquires set closed = 1 where id = {arg}")


@bot.event
async def on_guild_channel_create(channel):
    category_tickets = discord.utils.get(channel.guild.categories, id=categg)
    if channel.category == category_tickets:
        cur = con.cursor()
        start = cur.execute(f"SELECT * FROM inquires WHERE id = {channel.name.split('-')[1]}")
        start = start.fetchone()
        #cur.close()
        id = channel.name.split('-')[1]
        embed = discord.Embed(title='Escrow Service', description=f'Welcome to our escrow service, please submit the Discord ID of the user you will be trading with.\n\nAux. Information: Inquiry creator role in the trade is sender. | Inquiry creator role user id is - {start[0]}. | Inq. ID - *#{id}* | !close', color=discord.Color.blurple())
        await channel.send(embed=embed)




@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    category_tickets = discord.utils.get(msg.guild.categories, id=categg)
    if msg.channel.category == category_tickets:
        inquiry_id = msg.channel.name.split('-')[1]
        cur = con.cursor()
        start = cur.execute(f"SELECT * FROM inquires WHERE id = {inquiry_id}")
        start = start.fetchone()
        content = msg.content
        if start[1] is None and msg.author.id == int(start[0]):
            try:
                content = int(content)
            except:
                await msg.channel.send('Error! Wrong format, put only *pure discord ID!*', delete_after=5)
                return
            receiver = msg.channel.guild.get_member(content)
            if receiver is not None:
                cur.execute(f"UPDATE inquires SET receiver = {content} WHERE id = {inquiry_id}")
                con.commit()
                await msg.channel.set_permissions(receiver, read_messages=True,send_messages=True)
                await msg.channel.send(f'Welcome, {receiver.mention}! You were added to this inquiry, currently you can only spectate actions the sender is doing, you cannot interact with bot as for now, you will be required to confirm deal details later.')
                embed = discord.Embed(title='*Escrow* System', description=f'Please, {msg.author.mention}, select deal type.', color=discord.Color.blurple())
                await msg.channel.send(embed=embed, view=DealType())
            else:
                await msg.channel.send('User was not found, try again!', delete_after=5)
                return
        elif start[1] is not None and start[3] is not None and start[4] is not None and start[9] == 0 and int(start[0]) == msg.author.id and start[8] is None:
            try:
                int(content)
            except:
                await msg.channel.send('Put in integer number of USD.', delete_after=5)
                return
            cur.execute(f"UPDATE inquires SET usd = {int(content)} WHERE id = {inquiry_id}")
            embed = discord.Embed(title='Escrow System | Bitcoin 🟡', description=f'💰 USD is selected to be {content}$.', color=discord.Color.gold())
            await msg.channel.send(embed=embed)
            embed = discord.Embed(title=f'Escrow System | General Deal Confirmation❗', description=f'Receiver, please make sure.\nIt is a sale (not barter)\nDeal type is Bitcoin 🟡\n💰 USD price {content}$.\nNote: if you disagree with terms, **!close** the ticket.', color=discord.Color.red())
            await msg.channel.send(embed=embed, view=Confirm())
        con.commit()
        #cur.close()
    await bot.process_commands(msg)





bot.run('')
