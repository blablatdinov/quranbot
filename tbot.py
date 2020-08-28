import config, telebot, threading, json, time, schedule, cherrypy
from content import content

bot = telebot.TeleBot(config.token)


WEBHOOK_HOST = '107.173.6.211'
WEBHOOK_PORT = 88  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = '/home/quranbot/webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = '/home/quranbot/webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

print('Bot started')
print('count of content = ' + str(len(content)) + ' posts')


def read(): #Считываем словарь из файла
    with open('tada.json', 'r') as f:
        data = json.loads(str(f.read()))
    return data


data = read()
print(data)


def work(): #Делаем рассылку
    global data
    for key in data:
        try:
            bot.send_message(int(key), content[data[key] + 1])
            data[key] += 1
            with open('data.json', 'w') as f:   # Сохраняем словарь в файл
                f.write(json.dumps(data))
            print('work ok')
        except:
            data[key] = -1
            with open('data.json', 'w') as f:   # Сохраняем словарь в файл
                f.write(json.dumps(data))
            print('user ' + key + ' was deleted')


def friholiday():
    global data
    for key in data:
        try:
            bot.send_message(int(key), "Всех с благословенной пятницей, друзья!")
        except:
            print(key + 'was deleted')


def status(): #Печатаем словарь в консоль
    print(data)
    bot.send_message(358610865, "I'm working. Count of users = " + str(len(data)))


def sh():
    print('def sh started')
    schedule.every().day.at("07:00").do(work)   #Запускаем рассылку каждый день в 7 часов
    schedule.every().day.at("06:00").do(read)   #Запускаем считвание словаря каждый день в 6 часов
    schedule.every().friday.at("08:00").do(friholiday)
    schedule.every().day.at("06:30").do(status)
    # schedule.every(1).seconds.do(work)
    while True:
        schedule.run_pending()
        time.sleep(1)


sh()


@bot.message_handler(func=lambda massage: True, commands=['start', 'help', 'registration'])
def start(message):
    global data
    if message.text == '/start':
        bot.send_message(message.chat.id, content[0])
    if message.text == '/help':
        bot.send_message(message.chat.id, message.chat.id)
    if message.text == '/registration':
        data[str(message.chat.id)]= 1
        with open('data.json', 'w') as f:   # Сохраняем словарь в файл
            f.write(json.dumps(data))
        bot.send_message(message.chat.id, 'Регистрация прошла успешно')
        time.sleep(1)
        bot.send_message(message.chat.id, content[1])
        print('new user - ' + str(message.chat.id))
        bot.send_message(358610865, 'Зарегестрировался новый пользователь. Идентификатор - ' + str(message.chat.id))


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
bot.remove_webhook()

 # Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))


# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

 # Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})


# bot.polling(none_stop=True, interval=0)


