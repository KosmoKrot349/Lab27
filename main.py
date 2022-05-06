import telebot
import psycopg2
from datetime import datetime, timedelta
from telebot import types

token='5333911459:AAFKGAcEf9umVUApXDIV1hlpJgaa4q9tyoQ'
bot = telebot.TeleBot(token)
keyboard = types.ReplyKeyboardMarkup()
conn = psycopg2.connect(database="Lab7",user="postgres", password="1111", host="localhost", port="5432")
cursor = conn.cursor()

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Хочу", "/help", "расписание")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МАУП?', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я умею выводить расписание по дням, и по неделям')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда –https://maup.com.ua/')

    else:
        if message.text.lower()=="расписание":
            keyboard = types.ReplyKeyboardMarkup()
            keyboard.row("Пн","Вт","Ср","Чт","Пт","На эту неделю", "На следующую неделю","Назад")
            bot.send_message(message.chat.id, 'Выберите, какое расписание вас интересует', reply_markup=keyboard)

        else:
            if message.text.lower()=="на эту неделю":
                bot.send_message(message.chat.id, getScheduleWeek(datetime.now()))
            else:
                if message.text.lower()=="на следующую неделю":
                    bot.send_message(message.chat.id, getScheduleWeek(datetime.now()+timedelta(days=7)))
                else:
                    if message.text.lower() == "пн" or message.text.lower() == "вт" or message.text.lower() == "ср" or message.text.lower() == "чт" or message.text.lower() == "пт":
                        bot.send_message(message.chat.id,getScheduleDay(message.text.lower()))
                    else:
                        if message.text.lower()=="назад":
                            keyboard = types.ReplyKeyboardMarkup()
                            keyboard.row("Хочу", "/help", "расписание")
                            bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МАУП?', reply_markup=keyboard)
                        else:
                            bot.send_message(message.chat.id, 'Ивините, я Вас не понял')



def getScheduleWeek(date):

    sqldate=GetMondayDate(date).date()
    sql=f"select  tt.\"day\",tt.\"startTime\",tt.\"roomNumber\",s.\"name\",tea.\"fullName\" from timetable as tt join subjects as s on s.\"Id\"=tt.\"subjectId\" join teachers as tea on s.\"Id\"=tea.\"subjectId\" where tt.\"startTime\">='{sqldate.strftime('%Y-%m-%d %H:%M:%S')}' and tt.\"startTime\"<=date '{sqldate.strftime('%Y-%m-%d %H:%M:%S')}'+interval '7 day' order by tt.\"startTime\",tt.\"subjectId\""
    cursor.execute(sql)
    records = list(cursor.fetchall())
    return GenerateSchedule(records)

def getScheduleDay(day):
    monday=GetMondayDate(datetime.now())
    delata = 0

    if day == 'пн':
        delata = 0
    if day == 'вт':
        delata = 1
    if day == 'ср':
        delata = 2
    if day == 'чт':
        delata = 3
    if day == 'пт':
        delata = 4

    sqldate = (monday+ timedelta(days=delata)).date()
    sql = f"select  tt.\"day\",tt.\"startTime\",tt.\"roomNumber\",s.\"name\",tea.\"fullName\" from timetable as tt join subjects as s on s.\"Id\"=tt.\"subjectId\" join teachers as tea on s.\"Id\"=tea.\"subjectId\" where tt.\"startTime\">='{sqldate.strftime('%Y-%m-%d %H:%M:%S')}' and tt.\"startTime\"<=date '{sqldate.strftime('%Y-%m-%d %H:%M:%S')}'+interval '1 day' order by tt.\"startTime\",tt.\"subjectId\""
    cursor.execute(sql)
    records = list(cursor.fetchall())
    str = GenerateSchedule(records)
    return str






def GetMondayDate(date):
    nameOfDay = date.strftime("%A")
    delata = 0

    if nameOfDay == 'Monday':
        delata = 0
    if nameOfDay == 'Tuesday':
        delata = 1
    if nameOfDay == 'Wednesday':
        delata = 2
    if nameOfDay == 'Thursday':
        delata = 3
    if nameOfDay == 'Friday':
        delata = 4
    if nameOfDay == 'Saturday':
        delata = 5
    if nameOfDay == 'Sunday':
        delata = 6
    return date - timedelta(days=delata)

def GenerateSchedule(records):
    sheduleString=''
    day=''
    for record in records:
        if(day!=record[0]):
            sheduleString+='\n'+str(record[0])+'\n_________________________\n'
            day=str(record[0])
        sheduleString+=str(record[3])+' '+str(record[2])+' '+str(record[1])+' '+str(record[4])+'\n'
    return sheduleString



bot.polling(none_stop=True, interval=0)



