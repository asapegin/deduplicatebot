##
 # Copyright 2024 Dr. Andrey Sapegin
 #
 # Licensed under the "Attribution-NonCommercial-ShareAlike" Vizsage
 # Public License (the "License"). You may not use this file except
 # in compliance with the License. Roughly speaking, non-commercial
 # users may share and modify this code, but must give credit and 
 # share improvements. However, for proper details please 
 # read the full License, available at
 #  https://github.com/asapegin/licenses/blob/main/Vizsage-License-BY-NC-SA
 # and the handy reference for understanding the full license at 
 #  https://github.com/asapegin/licenses/blob/main/Vizsage-Deed-BY-NC-SA
 #
 # Please contact the author for any other kinds of use.
 #
 # Unless required by applicable law or agreed to in writing, any
 # software distributed under the License is distributed on an 
 # "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
 # either express or implied. See the License for the specific 
 # language governing permissions and limitations under the License.
 #
 ##

import telebot
import logging
import sys
import traceback
import html
import emoji
import demoji
from telegram.helpers import escape_markdown
import sqlite3
import time

conn = sqlite3.connect('/home/vampire/remdupsbot_sqlite.db',check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY,mtime INTEGER, chat_id,thread_id,user_id,message_id,message)")
cur.execute("select max(id) from messages")
result = cur.fetchone()
if result is None:
    mid=0
else:
    print(result)
    print(result[0])
    mid = result[0]

bot = telebot.TeleBot('xxx:yyy')

def sanitiser(text):
    #res = emoji.replace_emoji(text,replace="")
    #demoji.replace(res,repl="")
    res = text
    res = html.escape(res)
    res = escape_markdown(res)
    return res

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = sanitiser(message.text)
    millis = time.time_ns() // 1_000_000
    threadid = message.message_thread_id
    if threadid is None:
        threadid = ''
    print(message.chat.id,millis-15778800000,threadid,message.from_user.id,text)
    if text == "/rules":
        return
    cur.execute("select * from messages where chat_id=? and mtime > ? and thread_id=? and user_id=? and message=?",(message.chat.id,millis-15778800000,threadid,message.from_user.id,text))
    result = cur.fetchone()
    if result is not None:
        #print(result[0],result[1],result[2],result[3],result[4],result[5],result[6])
        # check if messaged saved in the DB was already deleted
        try:
            message_exists = bot.pin_chat_message(result[2],result[5],True)
        except:
            message_exists = False

        if message_exists:
            bot.unpin_chat_message(result[2],result[5])
            deleted = False
        else:
            deleted = True
            cur.execute("DELETE FROM messages WHERE chat_id=? and message_id = ?", (message.chat.id,result[5]))
            conn.commit()
    if result is not None and not deleted:
        print("it was duplicate, sending reply")
        print(message.from_user.full_name,message.from_user.id)
        bot.send_message(message.chat.id, f"Сообщение от [{message.from_user.full_name}](tg://user?id={message.from_user.id}) было автоматически удалено,\
        так как такое же сообщение уже было опубликовано ранее. \
        Правила публикации объявлений доступны по команде /rules", reply_to_message_id=message.id, parse_mode='markdown')
        print("deleting message:")
        print(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id)
    else:
        global mid
        mid = mid + 1
        cur.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?);", (mid,millis,message.chat.id,threadid,message.from_user.id,message.id,text))
        conn.commit()
        print("no duplicate found, writing message to db:")
        print(mid,millis,message.chat.id,message.message_thread_id,message.from_user.id,message.id,text)
        # delete all but last 10k messages from DB if DB gets too big (more than 20k messages)
        # check every 1000 messages
        if mid % 1000 == 0:
            cur.execute("SELECT COUNT(*) FROM messages")
            result = cur.fetchone()
            row_count = result[0]
            if row_count > 20000:
                cur.execute("delete from messages where id not in (select id from test order by id desc limit 10000)")
                conn.commit()
            #delete all messages older than half a year
            #cur.execute("delete from messages where mtime < ?",millis-15778800000)
            #conn.commit()

# Запускаем бота
while True:
    try:
	# Get information about the bot's status in the chat
	#chat_id =
        #bot_status = bot.get_chat_member(chat_id, bot.get_me().id)

        # Check if the bot has admin rights in the chat
        #if bot_status.status in ['administrator', 'creator']:
        #    print("The bot has admin rights in the group.")
        #else:
        #    print("The bot does not have admin rights in the group.")
        #    time.sleep(60)
        #    continue

        bot.infinity_polling(none_stop=True)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        error = "".join(line for line in lines)
        logging.error(error)
