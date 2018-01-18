import discord
import asyncio
import datetime
from time import sleep
import random
#import sys
import sympy
import tweepy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("discordkey")
parser.add_argument("twitterkey")
parser.add_argument("twittersecret")
args = parser.parse_args()


last_purge = datetime.date.today()
ONE_DAY = datetime.timedelta(days=1)
GMT_SUMMER = 22
GMT_WINTER = 23
i = 0

CHANNEL_ID = "359843358346313730" #My channel
TEMP = "368389272153096192" #temp
PICS = "362757563739144192"
PICS2 = "368767279824896000"
MIMIC = "369199932026126337"
PINK = "348537189350506496"
MATH = "352112797212999687"
MYMATH = "369447607052795904"
IMAGE_EXT = "jpg jpeg png bmp gif".split(" ")
KEY = args.discordkey
TWITKEY = args.twitterkey
TWITSECRET = args.twittersecret



client = discord.Client()

async def evaluate_pic(message):
    if has_image(message) and message.content == "":
        print("This is a good pic!")
    else:
        stuff = message.content
        print("This is a bad pic.")
        await client.delete_message(message)
        print(stuff.replace(u"\u2018", "'").replace(u"\u2019", "'"))

#Takes a string and returns a list of urls
#Returns empty list if no urls
def to_urls(s):
    words = s.split(' ')
    for word in words:
        if not is_url(word):
            words.remove(word)
    return words

def sans_urls(s):
    words = s.split(' ')
    for word in words:
        if is_url(word):
            words.remove(word)
    return words

def has_image(message):
    global IMAGE_EXT
    out = False
    #for embed in message.embeds:
    #    #print("There's an {} embed!".format(type(embed)))
    #    if embed['type'] == 'image':
    #        out = True
    #    #if embed.image != Empty:
    #    #    return True
    for att in message.attachments:
        #print(type(att))
        #print(att)
        if att['filename'].split('.')[-1] in IMAGE_EXT:
            out = True
    return out

def is_url(s):
    if s.startswith('http'):
        return True
    else:
        return False

def has_urls(s):
    urls = to_urls(s)
    if len(urls) > 0:
        return True
    else:
        return False

def has_text(s):
    if s == "":
        return False
    else:
        text = sans_urls(s)
        if len(text) != 0:
            return True
        else:
            return False

def only_urls(s):
    urls = to_urls(s)
    if urls == s:
        return True
    else:
        return False

def getTweet(process=False):
    auth = tweepy.OAuthHandler(TWITKEY, TWITSECRET)
    api = tweepy.API(auth)
    tweets = api.user_timeline('metaprophet')
    quote = random.choice(tweets).text
    if process:
        quote = quote.lower()
        if quote.endswith('.') and not quote.endswith('..'):
            quote = quote.strip('.')
    return quote




async def process_matlab(message):
    print('matlab time!')
    code = message.content
    preamble = "\\documentclass{report}[12pt]\\thispagestyle{empty}\\usepackage{xcolor}\\begin{document}"
    #sympy.interactive.init_printing(fontsize='20pt',backcolor='Black')
    code = '\huge \definecolor{bg}{HTML}{36393e} \definecolor{fg}{HTML}{c0c1c2} \pagecolor{bg} \\textcolor{fg}{'+code+'}'
    #code = '\huge '+code
    print(code)
    try:
        sympy.preview(code, output='png', filename='latex.png', euler=False, viewer='file', preamble=preamble)
        await client.send_file(message.channel, 'latex.png')
    except RuntimeError as e:
        print(e)
        await client.add_reaction(message, '❌')
        #s = str(e)
        #await client.send_message(message.channel, s)



async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed:
        await consider_purge()
        #print("Running background task")
        await asyncio.sleep(10) # task runs every 10 seconds

async def updateChan():
    number = int(tempchan.name.strip('temp'))+1
    name = 'temp'+str(number)
    topic = getTweet()
    print(tempchan.name+' -> '+name)
    print('Topic: '+topic)
    await client.edit_channel(tempchan, name=name, topic=topic)

async def purge():
    #to do: make it not crash when quoting something unprintable
    #to do: make it handle >1000 messages
    #to do: put logic outside this function and make it only and definitively purge
    global last_purge
    global GMT_WINTER

    today = datetime.date.today()
    yesterday = today - ONE_DAY
    midnight = datetime.time(GMT_WINTER, 0, 0)
    purge_before = datetime.datetime.combine(yesterday, midnight)

    last_purge = today
    
    print("time to delete i guess")
    deleted = await client.purge_from(tempchan, limit=10000, before=purge_before, after=purge_before-ONE_DAY*14)
    if len(deleted) != 0:
        print('Deleted {} messages'.format(len(deleted)))
        quote = ''
        #while quote == '': 
        quote = random.choice(deleted).content
        await updateChan()
        
        if quote != '':
            await client.send_message(tempchan, quote)
            print('Quote: '+quote)
    else:
        await client.send_message(tempchan, 'not yet!')

async def pretend_purge():
    global last_purge
    last_purge = datetime.datetime.today()
    await client.send_message(tempchan, 'I wanna purge!')

async def consider_purge():
    #print('Should i purge!?')
    if datetime.date.today() > last_purge:
        await purge()

@client.event
async def on_ready():
    global tempchan
    global picschan
    global mychan
    global mimic
    global pinkserver
    global mymath
    global mathchan
    tempchan = client.get_channel(TEMP)
    picschan = client.get_channel(PICS)
    mychan = client.get_channel(CHANNEL_ID)
    mimic = client.get_channel(MIMIC)
    pinkserver = client.get_server(PINK)
    mymath = client.get_channel(MYMATH)
    mathchan = client.get_channel(MATH)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await client.delete_message(client.get_message(client.get_channel('362757563739144192'),'368798975068864515'))
    #await client.send_message(tempchan, 'you fools, this server is now mine')

#@client.event
#async def on_error(event, *args, **kwargs):
#    err = sys.exc_info()
#    for thing in err:
#        await client.send_message(mychan, thing)
    


@client.event
async def on_message(message):
    if message.author != client.user:
        global last_purge
        #print("Last purge was {}".format(last_purge))
        #print(datetime.datetime.today())
        #consider_purge()
        if message.content.startswith('bot, get ready'):            
            last_purge = last_purge - ONE_DAY
        if message.content.startswith('!forceupdate'):
            await updateChan()
        #if message.content.startswith('!forcerename'):
            #await client.edit_channel(tempchan, name="temp65", topic="Now put the gun down.")
        if message.content.startswith('!acat'):
            await client.send_message(tempchan, '(=^・^=)')
        if (message.channel == mathchan or message.channel == mymath) and message.content.startswith('$') and message.content.endswith('$'):
            await process_matlab(message)
        if message.channel == picschan:
            await evaluate_pic(message)
        if client.user in message.mentions:
            await asyncio.sleep(1)
            await client.send_message(message.channel, '?')
        if message.channel == mimic:
            await client.send_message(mimic, message.content)
            print("time to mimic this: "+message.content)            
    else:
        print("Woah that message was by me!")



client.loop.create_task(my_background_task())
client.run(KEY)
print("Hey it's THIS line! What does it mean?")