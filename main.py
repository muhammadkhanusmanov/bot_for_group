from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler
from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ChatAdministratorRights,ChatPermissions
from db import DB
import datetime


def start(update:Update,context:CallbackContext):
    bot=context.bot
    user_id=update.message.from_user.id
    chat_id=update.message.chat_id
    first_name=update.message.from_user.first_name
    text=f'Assalomu Alaykum {first_name}'
    db=DB('db.json')
    db.starting(user_id)
    db.save()
    bot.send_message(chat_id=chat_id,text=text)
    text=f'Tilni tanlang'
    uz=InlineKeyboardButton('Uz🇺🇿',callback_data='til uz')
    ru=InlineKeyboardButton('ru🇷🇺',callback_data='til ru')
    btn=InlineKeyboardMarkup([[uz,ru]])
    bot.send_message(chat_id=chat_id,text=text,reply_markup=btn)

def til(update:Update,context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_iid=query.message.message_id
    bot=context.bot
    q,til=query.data.split()
    user_id=query.from_user.id
    print(user_id)
    db=DB('db.json')
    db.add_til(user_id,til)
    user=db.get_user(user_id)
    lang=user['til']
    group=db.get_statistic()
    spr_admin=group['superadmins']
    if str(user_id) in spr_admin:
        if lang=='uz':
            text='Admin nazorati'
            admin=KeyboardButton('👤Admin panel')
            btn=ReplyKeyboardMarkup([[admin]],resize_keyboard=True)       
            bot.sendMessage(user_id,text,reply_markup=btn)
        else:
            text='Административный контроль'
            admin=KeyboardButton('👤Панель администратора')
            btn=ReplyKeyboardMarkup([[admin]],resize_keyboard=True)
            bot.sendMessage(chat_id=user_id,text=text,reply_markup=btn)
    else:
        if str(user_id) in group['admins']:
            if lang=='uz':
                text='Siz bu botda adminsiz sizda cheklovlar yo\'q'
                bot.sendMessage(user_id,text)
            else:
                text='Вы не являетесь админом этого бота, у вас нет ограничений'
                bot.sendMessage(user_id,text)
        else:
            if lang=='uz':
                text=f'Bu bot {group["group"]} da cheklovlarni oluvchi bot.\n Bu bot orqali tulov qilasiz va guruh cheklovlaridan ozod bo\'lasiz.'
                tulov=KeyboardButton('💰To\'lov',resize=True)
                data=KeyboardButton('📓Malumot',resize=True)
                btn=ReplyKeyboardMarkup([[data,tulov]],resize_keyboard=True)
                bot.sendMessage(user_id, text,reply_markup=btn)
            else:
                text=f'С помощью этого бота вы можете получить информацию о своем статусе в {group["group"]}.'
                tulov=KeyboardButton('💰Оплата',resize=True)
                data=KeyboardButton('📓Информация',resize=True)
                btn=ReplyKeyboardMarkup([[data,tulov]],resize_keyboard=True)
                bot.sendMessage(user_id, text,reply_markup=btn)
        
    db.save()

def tulov(update:Update,context:CallbackContext):
    bot=context.bot
    user_id=update.message.from_user.id
    chat_id=update.message.chat_id
    message_iid=update.message.message_id
    db=DB('db.json')
    user=db.get_user(user_id)
    lang=user['til']
    stc=db.get_statistic()
    typ=update.message.chat.type
    group=stc['group']
    if typ=='private':
        if str(user_id) in stc['actives'].keys():
            date=stc['actives'][str(user_id)]['date']
            if lang=='uz':
                text=f"Hozirda siz guruhda faolsiz {date} dan keyin tulov amalga oshirishingiz mumkin"
                bot.send_message(user_id,text)
            else:
                text=f"В настоящее время вы неактивны в группе и можете внести платеж после {date}"
                bot.send_message(chat_id=user_id,text=text)
        else:
            if lang=='uz':
                text=f"To'lov qilasiz va {stc['group']} da {stc['date']}ga cheklovlardan ozod bo'lasiz.\n\nTo'lov qilish:\nKarta raqami: {stc['cart']}\nKarta egasi:{stc['cart_name']}\n\nTo'lov qilib so'ng tasdiqlash tugmasini bosing"
                tasdiq=InlineKeyboardButton('Tasdiqlash✅',callback_data='tas tulov')
                btn=InlineKeyboardMarkup([[tasdiq]])
                bot.sendMessage(user_id,text,reply_markup=btn)
            else:
                text=f"Вы оплатите и освободитесь от ограничений по {stc['group']} до {stc['date']}.\n\nОплата:\nНомер карты: {stc['cart']}\ nВладелец карты:{stc[ 'cart_name']}\n\nПосле оплаты нажмите подтвердить"
                tasdiq=InlineKeyboardButton('Подтверждение✅',callback_data='tas tulov')
                btn=InlineKeyboardMarkup([[tasdiq]])
                bot.sendMessage(chat_id,text,reply_markup=btn)
    else:
        bot.delete_message(group,message_id=message_iid)
    db.save()

def pay(update:Update,context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id=query.message.message_id
    bot=context.bot
    user_id=query.from_user.id
    db=DB('db.json')
    user=db.get_user(user_id)
    lang=user['til']
    db.add_current(user_id)
    if lang=='uz':
        text="To'lovni tasdiqlatish uchun to'lov qilingan karta egasining kartada ko'rsatilgan ism familyasini quyidagi ko'rinishda <Ism:Karta egasi ismi familyasi> yuboring."
        bot.edit_message_text(chat_id=user_id,message_id=message_id,text=text)
    else:
        text="Для подтверждения платежа отправьте имя и фамилию платного держателя карты, как указано на карте в форме ниже <Имя:Карта владелец имя фамилия>."
        bot.edit_message_text(chat_id=user_id,message_id=message_id,text=text)
    db.save()

def admin(update:Update,context:CallbackContext):
    message_id=update.message.message_id
    bot=context.bot
    user_id=update.message.from_user.id
    db=DB('db.json')
    spr_user=db.get_statistic()['superadmins']
    lang=db.get_user(user_id)['til']
    if str(user_id) in spr_user:
        if lang=='uz':
            text="Tanlang"
            stc=InlineKeyboardButton('Statistika',callback_data='admin stc')
            upd_chan=InlineKeyboardButton('Guruhni almashtirish',callback_data='admin upd')
            upd_admin=InlineKeyboardButton('Admin qo\'shish',callback_data='admin add')
            del_admin=InlineKeyboardButton('Adminni o\'chirish',callback_data='admin del')
            upd_cart=InlineKeyboardButton("To'lov sozlamalari",callback_data='admin cart')
            btn=InlineKeyboardMarkup([[stc,upd_chan],[upd_admin,del_admin],[upd_cart]])
            bot.sendMessage(user_id,text,reply_markup=btn)
        else:
            text='Выбирать'
            stc=InlineKeyboardButton('Статистика',callback_data='admin stc')
            upd_chan=InlineKeyboardButton('Изменить группу',callback_data='admin upd')
            upd_admin=InlineKeyboardButton('Добавить администратор',callback_data='admin add')
            upd_cart=InlineKeyboardButton("Настройки оплаты",callback_data='admin cart')
            del_admin=InlineKeyboardButton('Удалить администратор',callback_data='admin del')
            btn=InlineKeyboardMarkup([[stc,upd_chan],[upd_admin,del_admin],[upd_cart]])
            bot.sendMessage(chat_id=user_id,text=text,reply_markup=btn)
    db.save()

def admin_command(update:Update,context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id=query.message.message_id
    bot=context.bot
    user_id=query.from_user.id
    db=DB('db.json')
    stc=db.get_statistic()
    lang=db.get_user(user_id)['til']
    q,data=query.data.split()
    if lang=='uz':
        if data=='stc':
            text=f"Bot super adminlari: {len(stc['superadmins'])} ta \n______\nDoimiy ruxsatlar:{len(stc['admins'])}\n________\nVaqtincha ruxsatlar:{len(stc['actives'].keys())}"
            bot.edit_message_text(chat_id=user_id,message_id=message_id,text=text)
        elif data=='cart':
            textf=f"Karta qo'shish: <Karta:Karta_raqami>\nKarta egasini almashtirish: <Cart name:Karta egasi ismi>\nFaollik vaqti (kunda): <Day:kun_raqamda>"
            bot.sendMessage(user_id,textf)
        elif data=='upd':
            text=f"Joriy guruh:{stc['group']}Guruhni yangilash uchun avval botga guruhga to'liq adminlik huquqini bering va undan so'ng <add group:@groupusername> shaklida yuboring"
            bot.edit_message_text(chat_id=user_id,message_id=message_id,text=text)
        elif data=='add':
            text=f"Admin turini tanlang"
            spr_admin=InlineKeyboardButton('Super Admin qo\'shish',callback_data='tur spra')
            pr_admin=InlineKeyboardButton('Admin qo\'shish',callback_data='tur pra')
            btn=InlineKeyboardMarkup([[spr_admin,pr_admin]])
            bot.edit_message_text(chat_id=user_id,text=text,message_id=message_id,reply_markup=btn)
        else:
            text=f"Admin turini tanlang"
            spr_admin=InlineKeyboardButton('Super Adminni olib tashlsh',callback_data='tur sprd')
            pr_admin=InlineKeyboardButton('Adminni olib tashlsh',callback_data='tur prd')
            btn=InlineKeyboardMarkup([[spr_admin,pr_admin]])
            bot.edit_message_text(chat_id=user_id,message_id=message_id,text=text,reply_markup=btn)
    else:
        if data=='stc':
            text=f"Суперадминистраторы ботов: {len(stc['superadmins'])} ta \n______\nПостоянные разрешения:{len(stc['admins'])}\n________\nВременные разрешения:{len( stc['actives'].keys())}"
            bot.edit_message_text(chat_id=user_id,message_id=message_id,text=text)
        elif data=='upd':
            text=f"Текущая группа:{stc['group']}Чтобы обновить группу, сначала предоставьте боту полные права администратора группы, а затем отправьте его как <add group:@groupusername>"
            bot.edit_message_text(chat_id=user_id,message_id=message_id,text=text)
        elif data=='add':
            text=f"Выберите тип администратора"
            spr_admin=InlineKeyboardButton('Добавить супер администратора',callback_data='tur spra')
            pr_admin=InlineKeyboardButton('Добавить администратора',callback_data='tur pra')
            btn=InlineKeyboardMarkup([[spr_admin,pr_admin]])
            bot.edit_message_text(chat_id=user_id,text=text,message_id=message_id,reply_markup=btn)
        elif data=='cart':
            textf="Добавить карту: <Karta:Card_>\nИзменить владельца карты: <Cart name:Card>\nВремя действия (день): <Day:day_number>"
            bot.sendMessage(user_id,textf)
        else:
            text=f"Выберите тип администратора"
            spr_admin=InlineKeyboardButton('Удалить суперадминистратора',callback_data='tur sprd')
            pr_admin=InlineKeyboardButton('Удалить администратора',callback_data='tur prd')
            btn=InlineKeyboardMarkup([[spr_admin,pr_admin]])
            bot.edit_message_text(chat_id=user_id,message_id=message_id,text=text,reply_markup=btn) 
    db.save() 


def data(update:Update,context:CallbackContext):
    bot=context.bot
    user_id=update.message.from_user.id
    chat_id=update.message.chat_id
    message_iid=update.message.message_id
    db=DB('db.json')
    user=db.get_user(user_id)
    lang=user['til']
    stc=db.get_statistic()
    actives=stc['actives'].keys()
    if lang=='uz':
        if str(user_id) in actives:
            date=stc['actives'][str(user_id)]['date']    
            text=f"Siz guruhda {date} gacha faolsiz"
            bot.sendMessage(user_id, text)
        else:
            text=f"Guruhda faollik uchun bot orqali to'lov qiling"
            bot.sendMessage(user_id, text)
    else:
        if str(user_id) in actives:
            date=stc['actives'][str(user_id)]['date'] 
            text=f"Вы активны в группе до {date}"
            bot.sendMessage(user_id,text)
        else:
            text="Платный бот за групповую активность"
            bot.sendMessage(user_id,text)
    db.save()

def up_admin(update:Update,context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id=query.message.message_id
    bot=context.bot
    user_id=query.from_user.id
    q,data=query.data.split()
    db=DB('db.json')
    user=db.get_user(user_id)
    lang=user['til']
    stc=db.get_statistic()
    if lang=='uz':
        if data=='spra':
            text="Super admin qo'shish <add superadmin:user_id> ko'rinishida yuboring."
            bot.sendMessage(user_id,text)
        elif data=='pra':
            text="Admin qo'shish <add admin:user_id> ko'rinishida yuboring."
            bot.sendMessage(user_id,text)
        elif data=='sprd':
            text="Super adminni olib tashlsh <del superadmin:user_id> ko'rinishida yuboring."
            bot.sendMessage(user_id,text)
        else:
            text="Adminni olib tashlsh <del admin:user_id> ko'rinishida yuboring."
            bot.sendMessage(user_id,text)
    else:
        if data=='spra':
            text='Отправить как Добавить суперадминистратора <add superadmin:user_id>.'
            bot.sendMessage(chat_id,text)
        elif data=='pra':
            text='Отправить как Добавить администратора <add admin:user_id>.'
            bot.sendMessage(chat_id,text)
        elif data=='sprd':
            text='Отправить как Удалить суперадминистратора <del superadmin:user_id>.'
            bot.sendMessage(chat_id,text)
        else:
            text='Отправить как Удалить администратора <del admin:user_id>.'
            bot.sendMessage(chat_id,text)
    db.save()
            

def mains(update:Update,context:CallbackContext):
    bot=context.bot
    user_id=update.message.from_user.id
    chat_id=update.message.chat_id
    message_iid=update.message.message_id
    db=DB('db.json')
    stc=db.get_statistic()
    date=str(update.message.date)
    date=datetime.datetime.strptime(date[:-9], "%Y-%m-%d %H:%M")
    actives=stc['actives'].keys()
    typ=update.message.chat.type
    if typ=='private':
        user=db.get_user(user_id)
        lang=user['til']
        if lang=='uz':
            try:
                d,text=update.message.text.split(':')
            except:
                pass
            else:
                print(d)
                if d=='add group' and str(user_id) in stc['superadmins']:
                    try:
                        chan1=bot.getChatMember(f'{text}',str(chat_id))['status']
                    except:
                        bot.sendMessage(chat_id,'Guruhni o\'zgashtirishda xatolik tekshirib qayta urinib ko\'ring') 
                    else:
                        db.add_group(text)
                        send_text="Guruh muvaffaqiyatli qo'shildi."
                        bot.sendMessage(user_id,send_text)
                elif (d.upper()=='ISM' or d=='Имя') and str(user_id) in stc['current_active']:
                    send_text=f"To'lov qilingan karta egasi : {text}\nMalumot to'g'ri bo'lsa tasdiqlash tugmasini bosing"
                    tas=InlineKeyboardButton('✅Tasdiqlash',callback_data=f'y tas/{text}')
                    bek=InlineKeyboardButton('❌Bekor qilish',callback_data='y bek/{text}')
                    btn=InlineKeyboardMarkup([[tas,bek]])
                    bot.sendMessage(chat_id,send_text,reply_markup=btn)
                elif d.upper()=='KARTA' and str(user_id) in stc['superadmins']: 
                    db.add_cart(text)
                    bot.sendMessage(user_id,"Muvaffaqiyatli qo'shildi")
                elif d.upper()=="CART NAME" and str(user_id) in stc['superadmins']:
                    db.add_name(text)
                    bot.sendMessage(user_id,"Muvaffaqiyatli qo'shildi")
                elif d.upper()=="DAY" and str(user_id) in stc['superadmins']:
                    db.add_date(text)
                    bot.sendMessage(user_id,"Muvaffaqiyatli qo'shildi")
                elif d=='add superadmin' and str(user_id) in stc['superadmins']:
                    send_text = f"Qo'shilgan superadmin IDisi:{text}"
                    bot.sendMessage(user_id,send_text)
                    db.add_superadmin(text)
                elif d=='add admin' and (str(user_id) in stc['superadmins']):
                    send_text = f"Qo'shilgan admin IDisi:{text}"
                    bot.sendMessage(user_id,send_text)
                    db.add_admin(text)
                elif d.lower()=='del superadmin' and str(user_id) in stc['superadmins']:
                    x=db.del_superadmin(text)
                    if x:
                        send_text=f"O'chirilgan super admin IDsi:{text}"
                        bot.send_message(user_id,send_text)
                    else:
                        send_text=f"{text} IDli super admin yo'q"
                        bot.send_message(user_id,send_text)
                elif d.lower()=='del admin' and str(user_id) in stc['superadmins']:
                    x=db.del_admin(text)
                    if x:
                        send_text=f"O'chirilgan admin IDsi:{text}"
                        bot.send_message(user_id,send_text)
                    else:
                        send_text=f"{text} IDli admin yo'q"
                        bot.send_message(user_id,send_text)
        else:
            try:
                d,text=update.message.text.split(':')
            except:
                pass
            else:
                if d=='add group' and str(user_id) in stc['superadmins']:
                    try:
                        chan1=bot.getChatMember(f'{text}',str(chat_id))['status']
                    except:
                        bot.sendMessage(user_id,'Проверьте наличие ошибок при изменении группы и повторите попытку.')
                    else:
                        db.add_group(text)
                        send_text="Группа успешно добавлена."
                        bot.sendMessage(user_id,send_text)
                elif (d.upper()=='NAME' or d.upper()=='ИМЯ') and str(user_id) in stc['current_active']:
                    send_text=f"Владелец платной карты: {text}\nЕсли информация верна, нажмите кнопку подтверждения."
                    tas=InlineKeyboardButton('✅Подтверждение',callback_data=f'y tas/{text}')
                    bek=InlineKeyboardButton('❌Отмена',callback_data='y bek/{text}')
                    btn=InlineKeyboardMarkup([[tas,bek]])
                    bot.sendMessage(chat_id,send_text,reply_markup=btn)
                elif d=='add superadmin' and str(user_id) in stc['superadmins']:
                    send_text=f"Добавлен идентификатор суперадминистратора: {text}"
                    bot.sendMessage(user_id,send_text)
                elif d.upper()=='KARTA' and str(user_id) in stc['superadmins']:
                    db.add_cart(text)
                    bot.sendMessage(user_id,"Добавлено успешно")
                elif d.upper()=="CART NAME" and str(user_id) in stc['superadmins']:
                    db.add_name(text)
                    bot.sendMessage(user_id,"Добавлено успешно")
                elif d.upper()=="DAY" and str(user_id) in stc['superadmins']:
                    db.add_date(text)
                    bot.sendMessage(user_id,"Добавлено успешно")
                elif d=='add admin' and str(user_id) in stc['superadmins']:
                    send_text=f"Добавлен идентификатор администратора: {text}"
                    bot.sendMessage(user_id,send_text)
                elif d.lower()=='del superadmin' and str(user_id) in stc['superadmins']:
                    x=db.del_superadmin(text)
                    if x:
                        send_text=f"Удален идентификатор суперадминистратора: {text}"
                        bot.sendMessage(user_id,send_text)
                    else:
                        send_text=f"Нет суперадминистратора с идентификатором {text}"
                        bot.sendMessage(user_id,send_text)
                elif d.lower()=='del admin' and str(user_id) in stc['superadmins']:
                    x=db.del_admin(text)
                    if x:
                        send_text=f"Удален идентификатор администратора: {text}"
                        bot.sendMessage(user_id,send_text)
                    else:
                        send_text=f"Нет администратора с идентификатором {text}"
                        bot.sendMessage(user_id,send_text)
    else:
        spr_admin=stc['superadmins']
        admin=stc['admins']
        actives=stc['actives']
        group=stc['group']
        if str(user_id) in actives.keys():
            datee=actives[str(user_id)]['date']
            muddat=datetime.datetime.strptime(datee,'%Y-%m-%d %H:%M')
            if date>muddat:
                bot.delete_message(chat_id=group,message_id=message_iid)
                try:
                    name=update.message.from_user.username
                except:
                    name=update.message.from_user.first_name
                    bot.send_message(group,f"Kechirasiz {name} guruhda yozish uchun @clikc_paymentbot orqali to'lov qiling va guruhda yana yoza olasiz.")
                    db.del_activ(user_id)
                else:
                    db.del_activ(user_id)
                    send_text=f"Kechirasiz @{name} guruhda yozish uchun @clikc_paymentbot orqali to'lov qiling va guruhda yana yoza olasiz."
                    bot.sendMessage(group,send_text)
            else:
                pass
        elif (str(user_id) in spr_admin or str(user_id) in admin):
            pass
        else:
            try:
                name=update.message.from_user.username
            except:
                name=update.message.from_user.first_name
                bot.send_message(group,f"{name} guruhda yozish uchun @clikc_paymentbot orqali to'lov qiling va guruhda yana yozaolasiz.")
            bot.delete_message(chat_id=group,message_id=message_iid)
            send_text=f"@{name} guruhda yozish uchun @clikc_paymentbot orqali to'lov qiling va guruhda yana yozaolasiz."
            bot.sendMessage(group,send_text)
            pr=ChatPermissions(can_send_media_messages=False)
            bot.restrict_chat_member(group,user_id,permissions=pr,until_date=date)

    db.save()

def yubor(update:Update,context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id=query.message.message_id
    bot=context.bot
    user_id=query.from_user.id
    try:
        name=query.from_user.username
    except:
        name=query.from_user.first_name
    q,data=query.data.split()
    data,namee=data.split('/')
    db=DB('db.json')
    user=db.get_user(user_id)
    spr=db.get_statistic()
    spr=spr['superadmins']
    lang=user['til']
    if lang=='uz':
        if data=='tas':
            text="Tasdiqlash uchun xabar adminga yuborildi. Tez orada xabaringiz ko'rib chiqiladi va tasdiqdan o'tsangiz guruhdagi cheklovlar sizdan olinadi."
            bot.edit_message_text(text=text, message_id=message_id,chat_id=user_id)
            db.del_current(str(user_id))
            text=f"Xabar yuboruvchi {name}\n___________\nTo'lov qilingan karta egasi ismi familyasi: {namee}\n\n"
            tas=InlineKeyboardButton('✅Tasdiqlash',callback_data=f'k tas/{user_id}')
            bek=InlineKeyboardButton('❌Bekor qilish',callback_data=f'k bek/{user_id}')
            btn=InlineKeyboardMarkup([[tas,bek]])
            for i in spr:
                try:
                    bot.sendMessage(i,text,reply_markup=btn)
                except:
                    pass
        else:
            text="To'lovni tasdiqlatish uchun to'lov qilingan karta egasining kartada ko'rsatilgan ism familyasini quyidagi ko'rinishda <Ism:Karta egasi ismi familyasi> yuboring."
            bot.edit_message_text(text=text, message_id=message_id,chat_id=user_id)
    else:
        if data=='tas':
            text="Сообщение отправлено администратору на утверждение. Ваше сообщение будет рассмотрено в ближайшее время, и после одобрения вы будете удалены из групповых ограничений."
            bot.edit_message_text(text=text, message_id=message_id,chat_id=user_id)
            db.del_current(str(user_id))
            text=f"Xabar yuboruvchi {name}\n___________\nTo'lov qilingan karta egasi ismi familyasi: {namee}\n\n"
            tas=InlineKeyboardButton('✅Tasdiqlash',callback_data=f'k tas/{user_id}')
            bek=InlineKeyboardButton('❌Bekor qilish',callback_data=f'k bek/{user_id}')
            btn=InlineKeyboardMarkup([[tas,bek]])
            for i in spr:
                try:
                    bot.sendMessage(i,text,reply_markup=btn)
                except:
                    pass
        else:
            text="Для подтверждения платежа отправьте имя и фамилию владельца платной карты, как указано на карте, в следующем формате <Имя: Имя владельца карты Фамилия>."
            bot.edit_message_text(text=text, message_id=message_id,chat_id=user_id)
    db.save()


def check(update:Update,context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id=query.message.message_id
    bot=context.bot
    user_id=query.from_user.id
    date=query.message.date
    date=str(date+datetime.timedelta(minutes=1.0))
    date=date[:-9]
    q,data=query.data.split()
    data,namee=data.split('/')
    db=DB('db.json')
    spr=db.get_statistic()
    spr=spr['superadmins']
    user=db.get_user(namee)
    lang=user['til']
    if lang=='uz':
        if data=='tas':
            text="✅"
            bot.edit_message_text(text=text, message_id=message_id,chat_id=user_id)
            text=f"To'lov tasdiqlandi endi siz faolsiz"
            bot.send_message(chat_id=namee,text=text)
            db.add_actives(chat_id=namee,date=date)
            pr=ChatPermissions(can_send_media_messages=True)
            bot.restrict_chat_member('@gpa123321',namee,permissions=pr,until_date=date)
        else:
            text="✅"
            bot.edit_message_text(text=text, message_id=message_id,chat_id=user_id)
            text="To'lov tasdiqlanmadi. Xatolik uchun admin bilan bog'lanish: @mol"
            bot.send_message(chat_id=namee,text=str(text))
    else:
        if data=='tas':
            text="✅"
            bot.edit_message_text(text=text, message_id=message_id,chat_id=user_id)
            text=f"Платеж подтвержден, теперь вы активны"
            bot.send_message(chat_id=namee,text=text)
            db.add_actives(chat_id=namee,date=date)
            pr=ChatPermissions(can_send_media_messages=True)
            bot.restrict_chat_member('@gpa123321',namee,permissions=pr,until_date=date)
        else:
            text="✅"
            bot.edit_message_text(text=text, message_id=message_id,chat_id=user_id)
            text="Платеж не подтвержден. Свяжитесь с администратором для ошибки: @mol"
            bot.send_message(chat_id=namee,text=text)
    db.save()

    


                   

                
                

        
        





updater=Updater('6239971522:AAESEFq1C7p4Q29ric5xqRneNNBqK3OyhHo')

dp=updater.dispatcher

dp.add_handler(CommandHandler('start',start))
dp.add_handler(CallbackQueryHandler(til,pattern='til'))
dp.add_handler(MessageHandler((Filters.text('💰Оплата') | Filters.text('💰To\'lov')),tulov))
dp.add_handler(MessageHandler((Filters.text('📓Информация') | Filters.text('📓Malumot')),data))
dp.add_handler(MessageHandler((Filters.text('👤Панель администратора') | Filters.text('👤Admin panel')),admin))
dp.add_handler(CallbackQueryHandler(admin_command,pattern='admin'))
dp.add_handler(CallbackQueryHandler(pay,pattern='tas'))
dp.add_handler(CallbackQueryHandler(up_admin,pattern='tur'))
dp.add_handler(MessageHandler(Filters.all,mains))
dp.add_handler(CallbackQueryHandler(yubor,pattern='y'))
dp.add_handler(CallbackQueryHandler(check,pattern='k'))


updater.start_polling()
updater.idle()