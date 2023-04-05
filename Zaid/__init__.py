from pyrogram import Client
from config import API_ID, API_HASH, SUDO_USERS, OWNER_ID, BOT_TOKEN, STRING_SESSION1, STRING_SESSION2, STRING_SESSION3, STRING_SESSION4, STRING_SESSION5, STRING_SESSION6, STRING_SESSION7, STRING_SESSION8, STRING_SESSION9, STRING_SESSION10
from datetime import datetime
import time
from aiohttp import ClientSession

StartTime = time.time()
START_TIME = datetime.now()
CMD_HELP = {}
SUDO_USER = SUDO_USERS
clients = []
ids = []

SUDO_USERS.append(OWNER_ID)
aiosession = ClientSession()

if API_ID:
   API_ID = API_ID
else:
   print("ئاگادارکردنەوە: API ID بە بەکارهێنانی ZAID API نەدۆزراوەتەوە ⚡")
   API_ID = "6435225"

if API_HASH:
   API_HASH = API_HASH
else:
   print("ئاگادارکردنەوە: API HASH بە بەکارهێنانی ZAID API نەدۆزراوەتەوە ⚡")   
   API_HASH = "4e984ea35f854762dcde906dce426c2d"

if not BOT_TOKEN:
   print("ئاگاداری: BOT TOKEN نەدۆزراوەتەوە PLZ ADD ⚡")   

app = Client(
    name="app",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Zaid/modules/bot"),
    in_memory=True,
)

if STRING_SESSION1:
   print("client1: دۆزرایەوە.. دەست پێدەکات.. 📳")
   client1 = Client(name="one", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION1, plugins=dict(root="Zaid/modules"))
   clients.append(client1)

if STRING_SESSION2:
   print("Client2: دۆزرایەوە.. دەست پێدەکات.. 📳")
   client2 = Client(name="two", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION2, plugins=dict(root="Zaid/modules"))
   clients.append(client2)

if STRING_SESSION3:
   print("Client3: دۆزرایەوە.. دەست پێدەکات.. 📳")
   client3 = Client(name="three", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION3, plugins=dict(root="Zaid/modules"))
   clients.append(client3)

if STRING_SESSION4:
   print("Client4: دۆزرایەوە.. دەست پێدەکات.. 📳")
   client4 = Client(name="four", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION4, plugins=dict(root="Zaid/modules"))
   clients.append(client4)

if STRING_SESSION5:
   print("Client5: دۆزرایەوە.. دەست پێدەکات.. 📳")
   client5 = Client(name="five", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION5, plugins=dict(root="Zaid/modules"))
   clients.append(client5)

if STRING_SESSION6:
   print("Client6: دۆزرایەوە.. دەست پێدەکات.. 📳")
   client6 = Client(name="six", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION6, plugins=dict(root="Zaid/modules"))
   clients.append(client6)

if STRING_SESSION7:
   print("Client7: دۆزرایەوە.. دەست پێدەکات.. 📳")
   client7 = Client(name="seven", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION7, plugins=dict(root="Zaid/modules"))
   clients.append(client7)

if STRING_SESSION8:
   print("Client8: دۆزرایەوە.. دەست پێدەکات.. 📳")
   client8 = Client(name="eight", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION8, plugins=dict(root="Zaid/modules"))
   clients.append(client8)

if STRING_SESSION9:
   print("Client9: دۆزرایەوە.. دەست پێدەکات.. 📳")
   client9 = Client(name="nine", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION9, plugins=dict(root="Zaid/modules"))
   clients.append(client9)

if STRING_SESSION10:
   print("Client10: دۆزرایەوە.. دەست پێدەکات.. 📳")
   client10 = Client(name="ten", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION10, plugins=dict(root="Zaid/modules")) 
   clients.append(client10)
