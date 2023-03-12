from flask import Flask, request
import os
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from main import start,til,tulov,mains,pay,yubor,check,admin,admin_command,up_admin,data as d


TOKEN = os.environ["Token"]

bot = Bot(TOKEN)

app = Flask(__name__)

@app.route('/webhook', methods=["POST", "GET"])
def hello():
    if request.method == 'GET':
        return 'hi from Python2022I'
    elif request.method == "POST":
        data = request.get_json(force = True)
        
        dispacher: Dispatcher = Dispatcher(bot, None, workers=0)
        update:Update = Update.de_json(data, bot)
    
        #update 
        dispacher.add_handler(CommandHandler('start',start))
        dispacher.add_handler(CallbackQueryHandler(til,pattern='til'))
        dispacher.add_handler(MessageHandler((Filters.text('💰Оплата') | Filters.text('💰To\'lov')),tulov))
        dispacher.add_handler(MessageHandler((Filters.text('📓Информация') | Filters.text('📓Malumot')),d))
        dispacher.add_handler(MessageHandler((Filters.text('👤Панель администратора') | Filters.text('👤Admin panel')),admin))
        dispacher.add_handler(CallbackQueryHandler(admin_command,pattern='admin'))
        dispacher.add_handler(CallbackQueryHandler(pay,pattern='tas'))
        dispacher.add_handler(CallbackQueryHandler(up_admin,pattern='tur'))
        dispacher.add_handler(MessageHandler(Filters.all,mains))
        dispacher.add_handler(CallbackQueryHandler(yubor,pattern='y'))
        dispacher.add_handler(CallbackQueryHandler(check,pattern='k'))

        
        dispacher.process_update(update)
        return 'ok'

