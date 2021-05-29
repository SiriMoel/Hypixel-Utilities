#COPYRIGHT 2021 AIDAN CROSBY
import discord
import random
import requests
import math
import datetime
TOKEN = "ODQ4MDIwODYyMzA4OTc0NjAy.YLGi-Q.N4a1Us-YLVBPDake6E8Vb575djI"
API = "4700f0a7-cae9-417a-a6ce-01f2592875c7"

#FUNCTIONS


#FINDING THE MOST RECENT PROFILE
def getRecentProfile(name, debug=False):
    data = requests.get(
        url = f"https://sky.shiiyu.moe/api/v2/profile/{name}").json()

    timestamp = -1
    profile = None
    if debug: print(f"searching through {len(data['profiles'])} profiles")
    for name, value in data['profiles'].items():
        if value['last_save'] > timestamp:
            timestamp = value['last_save']
            profile = value
    return profile



#FIND THERE CURRENT ARMOUR
def getArmourString(profile):
    armour = profile['items'].get('armor',0)
    if not armour: return "API OFF"

    names = [a['display_name'] for a in armour][::-1]
    if not names: return "NONE"
    return "\n".join(names)


#FIND THEIR CURRENT WEAPONS
def getWeaponsString(profile):
    w = profile['items'].get('weapons',0)
    if not w: return "API OFF"

    names = [a['display_name'] for a in w if a['rarity'] in ['mythic','legendary']]
    if not names: return "NO legendary or above"
    return "\n".join(names)

#FIND THERE LEVEL 100 PETS
def getPetString(profile):
    pets = profile['raw'].get ('pets', 0)
    if not pets: return "API OFF"
    names = [a['display_name'] for a in pets if a['level']['level']>=100]
    if not names: return "NONE>=100"
    pets = "\n".join(names)
    
    return pets


#FIND THERE CURRENT BANK AND BURSE COINS
def getBankCoins(name, profile):
    data = requests.get(
        url = f"https://sky.shiiyu.moe/api/v2/coins/{name}/{profile['cute_name']}"
    ).json()
    
    bank =  data.get('bank','API OFF')
    purse = data['purse']
    return str(bank), str(purse)

#FIND THERE MOST RECENT AUCTIONS(USING GETRECENTPROFILE FUNCTION AND HPYIXEL API)
def getCurrentAuctions(name):
    profile = getRecentProfile(name)
    result = ""
    UUID = profile["profile_id"]
    data = requests.get(
        url = f"https://api.hypixel.net/skyblock/auction?key=4700f0a7-cae9-417a-a6ce-01f2592875c7&profile={UUID}"
    ).json()
    auction = data["auctions"][-3:]
    for a in auction:
       date = datetime.datetime.fromtimestamp(a["end"] /1000.0)
       date_str = date.strftime("%Y-%m-%d %H:%M:%S")
       a = a["item_name"] + f" {date_str}" + f" for ${a['highest_bid_amount']:n}" + " \n"
       result = result + a
    return result
    print(UUID)


#EVENTS



#CLIENT EVENT, DETECTED WHEN STARTED UP
client = discord.Client()
@client.event
async def on_ready():
     print('We have logged in as {0.user}'.format(client))

#CLIENT EVENT OF MESSAGE
@client.event
async def on_message(message):
    

    #THE STATUS OF BOT(INGAME)
    await client.change_presence(activity=discord.Game('/help'))
    
    
    
    username = str(message.author).split('#')[0] 
    user_message =str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')
    if message.author == client.user:
        return
    if message.channel.name =='bot-commands':
        args = user_message.lower().split()
        print(args)
        
        if user_message.lower() == 'hello':
            await message.channel.send(f'Hello @{username.display_name}!')
            return
        elif user_message.lower() == 'bye':
            await message.channel.send(f'See you later @{username}!')
            return
        elif user_message.lower() == '/random':
            response =  f'This is your random number: {random.randrange(10000)}'
            await message.channel.send(response)
            return
        elif args[0] == '/armour':
            print("armour")
            name = args[1]
            await message.channel.send(f'giving armour to {name}')
            return
    if user_message.lower() == '/credits':
        await message.channel.send(f'This bot was made by PlutosNotRed#1169 or Pluto_Red in game.')
        return
    if user_message.lower() == '/help':
        embed=discord.Embed(title="Hypixel Utilities by #PlutosNotRed#1169")
        embed.set_author(name="Commands")
        embed.add_field(name="/random", value="Gets a random value", inline=False)
        embed.add_field(name="/overview [IGN]", value="Use this command to get an overview of your skyblock profile", inline=False)
        embed.add_field(name="bye", value=" Says goodbye to you", inline=False)
        embed.add_field(name="/help", value="What you are seeing right now", inline=False)
        embed.add_field(name="/credits", value="Shows you who made the bot", inline=False)
        embed.set_footer(text="Bot by PlutosNotRed#1169")
        await message.channel.send(embed = embed)

        return
    #/OVERVIEW
    if args[0] == '/overview':
        name = args[1]

        profile = getRecentProfile(name)
        bank,coin = getBankCoins(name,profile)
        armour = getArmourString(profile)
        pets = getPetString(profile)
        w = getWeaponsString(profile)
        auctions = getCurrentAuctions(name)
        print('======')
        print(type(pets),pets)
        print(armour)
        print(bank,coin)
        print(profile['cute_name'])
        embed=discord.Embed(title=f"on profile {profile['cute_name']}", color=0xe01700)
        embed.set_author(name=f"{name}", url=f"https://sky.shiiyu.moe/{name}", icon_url=f"https://cravatar.eu/helmavatar/{name}/190.png")
        embed.set_thumbnail(url=f"https://cravatar.eu/helmhead/{name}/190.png")
        embed.add_field(name="Armor <:superior_helmet:848070223268675625>", value=f"{armour}", inline=False)
        embed.add_field(name="Pet <:megaladon_pet:848074601262743563>", value=f"{pets}", inline=False)
        embed.add_field(name="Bank <:gold_ingot:848070289085956127>", value=f"{bank}", inline=False)
        embed.add_field(name="Purse <:piggy_bank:848070350323712010>", value=f"{coin}", inline=False)
        embed.add_field(name="Weapons <:iron_sword:848075149970374706>", value=f"{w}", inline=False)
        embed.add_field(name="Auctions <:iron_sword:848075149970374706>", value=f"{auctions}", inline=False)
        embed.set_footer(text="by PlutosNotRed#1169")
        await message.channel.send(embed = embed)
    


#SCRIPT TO RUN BOT


client.run(TOKEN)