import json
import time
from datetime import datetime
import requests

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data=f"cb_yes"),
               InlineKeyboardButton("No", callback_data=f"cb_no"))
    return markup

from jira_connector.JiraConnector import JiraConnector
from tamtam.tamtam import TamTam

TOKEN = 'bAxyci_N4kdPqV73tpQY-LFPJgRE11BasMJQOfpeb1s'
BOT_ID = 587004630026

bot = telebot.TeleBot(TOKEN)

tt = TamTam(TOKEN)
_chatsCount = 0
chats = tt.get_chats_all()

def hello(chat_id):
    tt.send(chat_id, 'Бот Жора снова с вами!. \n'
            'Для работы мне нужна URL вашей Jira \n'
            'Команда "Жора, URL = <адрес>"')
    print('Бот Жора снова с вами!')

def help(chat_id):
    tt.send(chat_id, 'Меня зовут Жора. \n'
            'Попросить меня о действии в Jira можно через обращение "Жора, <что сделать>" \n'
            'Вот что я уже умею: \n'
            'добавь задачу \n'
            'удали задачу \n'
            'выведи все задачи из \n'
            )

def task_for_bot(chat_id, project, summary, user):
    jc = JiraConnector('https://quanoskazka.atlassian.net/')
    jc.createIssue(project, summary, user)
    tt.send(chat_id, 'Выполняю, сир...')

def print_tasks(chat_id):
    tt.send(chat_id, 'Вывожу задачи из .... :\n задач нет')

def delete_task(chat_id):
    tt.send(chat_id, 'Задача удалена')

def CheckNewChats():
    all_chats = tt.get_chats_all()
    all_count_chats = len(all_chats)
#    print(all_count_chats)
    if tt._chatsCount != all_count_chats:
        count_new_chats = all_count_chats - tt._chatsCount
        for i in range (count_new_chats):
            hello(all_chats[i]['chat_id'])
            tt._chatsCount+=1

sender = tt.sender
text_msg = tt.text_msg
user_id_msg = tt.user_id_msg
user_name_msg = tt.user_name_msg

def check_us_msg():
    user_name_msg = sender['name']
    user_id_msg = sender['user_id']
    print('"',text_msg,'"', 'Author: ', user_id_msg, ' ', user_name_msg, ' ', datetime.strftime(datetime.now(), "%H:%M  %Y.%m.%d"))

#print(len(tt.get_chats_all()))

while True:
    CheckNewChats()
    chats_upd = tt.get_chats_all()
    for chat_count in range (len (chats_upd)):
        msgs = tt.get_messages(chats_upd[chat_count]['chat_id'])
        chatID = chats_upd[chat_count]['chat_id']
        print(chatID)
        
        sender = msgs[0]['sender']
        message = msgs[0]['message']
        messaget = msgs[0]['message']
        
        text_msg = message['text']
        
        if sender['user_id'] != BOT_ID and text_msg.lower().find('жора,') != -1:
            
            if text_msg.lower().find(' добавь задачу:') != -1:
                task_for_bot(chatID, project='TestProject', summary='BotTestTask', user='TestUser')
                check_us_msg()

            if text_msg.lower().find(' удали задачу:') != -1:
                delete_task(chatID)
                check_us_msg()

            if text_msg.lower().find(' выведи все задачи из') != -1:
                print_tasks(chatID)
                check_us_msg()

            if text_msg.lower().find('привет') != -1:
                check_us_msg()
                tt.send(chats_upd[chat_count]['chat_id'], 'Привет, ' + sender['name'])
            
            if text_msg.lower().find('help') != -1:
                check_us_msg()
                help(chatID)
            if text_msg.lower().find('помощь') != -1:
                check_us_msg()
                help(chatID)
                
                reply_markup:{"ReplyKeyboardMarkup":{"keyboard":[[{"KeyboardButton":{"text":"test"}}]]}}
    
        if sender['user_id'] != BOT_ID:
            if text_msg.lower().find('help') != -1:
                check_us_msg()
                help(chatID)
    time.sleep(1)
