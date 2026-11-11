import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
from instagrapi import Client

# ================= ВСТАВЬ СВОИ ДАННЫЕ =================
TELEGRAM_BOT_TOKEN = "СЮДА_ТОКЕН_ОТ_BOTFATHER"
TELEGRAM_MY_ID = "СЮДА_ТВОЙ_ЦИФРОВОЙ_ID"

INSTA_USER = "твой_логин_в_инсте"
INSTA_PASS = "твой_пароль_в_инсте"
# =====================================================

# Это заглушка-сервер, чтобы Koyeb видел, что сервис живой
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# --- Сам бот ---
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
cl = Client()

print("Подключаемся к Instagram...")
try:
    cl.login(INSTA_USER, INSTA_PASS)
    print("✅ Успешный вход в Instagram!")
    bot.send_message(TELEGRAM_MY_ID, "🚀 Бот на Koyeb успешно запущен и подключен к Инсте!")
except Exception as e:
    err_text = f"❌ Ошибка входа в Инсту: {e}"
    print(err_text)
    bot.send_message(TELEGRAM_MY_ID, err_text)

# Цикл проверки сообщений
last_msg_id = None
while True:
    try:
        threads = cl.direct_threads(amount=1)
        if threads:
            last_thread = threads[0]
            latest_msg = last_thread.messages[0]

            if latest_msg.id != last_msg_id:
                if str(latest_msg.user_id) != str(cl.user_id):
                    sender = last_thread.thread_title or "Собеседник"
                    text = latest_msg.text or "[Вложение / Рилс]"
                    
                    bot.send_message(TELEGRAM_MY_ID, f"📩 *Новое сообщение в Инсте!*\nОт: *{sender}*\n\n{text}", parse_mode="Markdown")

                last_msg_id = latest_msg.id
        time.sleep(5)
    except Exception as e:
        time.sleep(5)
