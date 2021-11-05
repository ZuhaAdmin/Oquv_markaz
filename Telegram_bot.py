import telebot

from telebot import types
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text, update, delete
engine = create_engine('sqlite:///all_users.db', echo = True)
meta = MetaData()

tag_users = Table(
    'tag_users', meta,
    Column('id_tag', Integer, primary_key = True),
    Column('name', String),
    Column('lastname', String),
    Column('username', String),
    Column('user_id', Integer),
)

user = Table(
    'user', meta,
    Column('id', Integer, primary_key = True),
    Column('User_id', Integer),
    Column('Ism', String),
    Column('Familya', String),
    Column('Yosh', Integer),
    Column('Oqish_yoki_ish_manzili', String),
    Column('Shaxsiy_kompyuterga_egalik', String),
)

bot = telebot.TeleBot("2038119379:AAFAk_mMLsw0gZf5USqPxk7-sd3zEztKbm4", parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    ismi = message.from_user.first_name
    familya = message.from_user.last_name
    user_id = message.from_user.id
    username = message.from_user.username

    meta.create_all(engine)

    ins = tag_users.insert()
    ins = tag_users.insert().values(name = ismi, lastname = familya, username = username, user_id = user_id)
    conn = engine.connect()
    result = conn.execute(ins)


    # markup = types.InlineKeyboardMarkup()
    # itembtna = types.InlineKeyboardButton('Python dasturlash tili kursi', callback_data = "message")
    # itembtnv = types.InlineKeyboardButton('Java dasturlash tili kursi', callback_data = "message")
    # itembtnb = types.InlineKeyboardButton('C# dasturlash tili kursi', callback_data = "message")
    # itembtnd = types.InlineKeyboardButton('Biz bilan bog\'lanish', callback_data = "message")
    # markup.row (itembtna, itembtnv, itembtnb,itembtnd)
    markup = types.ReplyKeyboardMarkup()
    markup.add('Python dasturlash tili kursi', 'Java dasturlash tili kursi','C# dasturlash tili kursi', 'Biz bilan bog\'lanish', 'delete')
    reply_text = f"Assalomu alaykum {ismi}.\nO\'quv markazimizning rasmiy Botiga hush kelibsiz. \n Iltimos o\'zingiz hohlagan kursni tanlang"
    bot.send_message(user_id, reply_text, reply_markup=markup)
    
# @bot.callback_query_handler (func = lambda call: True)
# def callback_query(call):
#     if call.data == "message":
#         bot.answer_callback_query(call.id, "Xush kelibsiz")
#         bot.register_next_step_handler(call.message, handle_docs_audio)


@bot.message_handler(content_types=['text'])
def handle_docs_audio(message):
    if message.text == 'Python dasturlash tili kursi':
        markup = types.InlineKeyboardMarkup()
        itembtna = types.InlineKeyboardButton('Ro\'yhatdan o\'tish', callback_data = "register")
        itembtnv = types.InlineKeyboardButton('Ortga qaytish', callback_data = "back")
        markup.row (itembtna, itembtnv)
        m_text = "O\'quv kursi davomiyligi: 6 oy,\nNarxi: 700 ming so\'m,\nDars vaqti: toq kunlari 18:30 - 20:30.\n"
        m_text += "\nRo\'yhatdan o\'tishni hohlaysizmi?"
        
        bot.send_message(message.from_user.id, m_text, reply_markup = markup)

    elif message.text == "delete":
        stmt = (
            delete(tag_users).
            where(tag_users.c.user_id == message.from_user.id)
        )

        conn = engine.connect()
        result = conn.execute(stmt)
        bot.send_message(message.from_user.id, "del")        

    if message.text == 'Java dasturlash tili kursi':
        markup = types.InlineKeyboardMarkup()
        itembtna = types.InlineKeyboardButton('Ro\'yhatdan o\'tish', callback_data = "register")
        itembtnv = types.InlineKeyboardButton('Ortga qaytish', callback_data = "back")
        markup.row (itembtna, itembtnv)
        m_text = "O\'quv kursi davomiyligi: 6 oy,\nNarxi: 700 ming so\'m,\nDars vaqti: juft kunlari 19:00 - 21:00.\n"
        m_text += "\nRo\'yhatdan o\'tishni hohlaysizmi?"
       
        bot.send_message(message.from_user.id, m_text, reply_markup = markup)

    if message.text == 'C# dasturlash tili kursi':
        markup = types.InlineKeyboardMarkup()
        itembtna = types.InlineKeyboardButton('Ro\'yhatdan o\'tish', callback_data = "register")
        itembtnv = types.InlineKeyboardButton('Ortga qaytish', callback_data = "back")
        markup.row (itembtna, itembtnv)
        m_text = "O\'quv kursi davomiyligi: 6 oy,\nNarxi: 700 ming so\'m,\nDars vaqti: juft kunlari 18:30 - 20:30.\n"
        m_text += "\nRo\'yhatdan o\'tishni hohlaysizmi?"
        
        bot.send_message(message.from_user.id, m_text, reply_markup = markup)

@bot.callback_query_handler (func = lambda call: True)
def callback_query(call):
    if call.data == "register":
        bot.answer_callback_query(call.id, "Xush kelibsiz")
        bot.send_message(call.message.chat.id,"Iltimos Ismingizni kiriting:")
        bot.register_next_step_handler(call.message, set_name)
    elif call.data == "back":
        bot.answer_callback_query(call.id, "Xush kelibsiz")

    # if message.text == 'Ro\'yhatdan o\'tish':
    #     familya = "Iltimos Familyangizni va Ismingizni kiriting"
    #     bot.reply_to(message, familya)

    # else:
    #     ismFamilya = message.text
    #     m_text = "Yoshingizni kiriting"
    #     bot.reply_to (message, m_text)
def set_name(mess):
    familya = mess.from_user.first_name
    yosh = mess.from_user.id
    meta.create_all(engine)

    ins = user.insert()
    ins = user.insert().values(Ism = mess.text, User_id = yosh, Familya = familya, Yosh = yosh, Oqish_yoki_ish_manzili = familya, Shaxsiy_kompyuterga_egalik = familya)
    conn = engine.connect()
    result = conn.execute(ins)

    m_text = "Familyangizni kiriting"
    bot.send_message(mess.from_user.id, m_text)
    bot.register_next_step_handler(mess, set_surname)

def set_surname(mes):
    son = mes.from_user.id
    m = mes.text
    stmt = (update(user).where(user.c.User_id == son).values(Familya = m))
    conn = engine.connect()
    result = conn.execute(stmt)


    m_text = "Yoshingizni kiriting"
    bot.send_message(mes.from_user.id, m_text)
    bot.register_next_step_handler(mes, set_old)

def set_old(xat):
    son = xat.from_user.id
    m = xat.text
    stmt = (update(user).where(user.c.User_id == son).values(Yosh = m))
    conn = engine.connect()
    result = conn.execute(stmt)

    m_text = "O\'qish yoki ishingizni manzilini kiriting"
    bot.send_message(xat.from_user.id, m_text)
    bot.register_next_step_handler(xat, set_adress)

def set_adress(sms):
    son = sms.from_user.id
    m = sms.text
    stmt = (update(user).where(user.c.User_id == son).values(Oqish_yoki_ish_manzili = m))
    conn = engine.connect()
    result = conn.execute(stmt)

    m_text = "Shaxsiy kompyuteringiz mavjutmi"
    bot.send_message(sms.from_user.id, m_text)
    bot.register_next_step_handler(sms, kompyuter)

def kompyuter(ms):
    son = ms.from_user.id
    m = ms.text
    stmt = (update(user).where(user.c.User_id == son).values(Shaxsiy_kompyuterga_egalik = m))
    conn = engine.connect()
    result = conn.execute(stmt)


    

# def set_surname(mes):
#     m_text = "Yoshingizni kiriting"
#     bot.send_message(mes.from_user.id, m_text)
#     bot.register_next_step_handler(mes, set_surname)

# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
    # ismFamilya = message
    
    
bot.infinity_polling()