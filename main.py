import logging
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Включим логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Список стран и их столиц
countries_and_capitals = {
    "Австрия": "Вена",
    "Албания": "Тирана",
    "Андорра": "Андорра-ла-Велья",
    "Беларусь": "Минск",
    "Бельгия": "Брюссель",
    "Болгария": "София",
    "Босния и Герцеговина": "Сараево",
    "Ватикан": "Ватикан",
    "Великобритания": "Лондон",
    "Венгрия": "Будапешт",
    "Германия": "Берлин",
    "Греция": "Афины",
    "Дания": "Копенгаген",
    "Ирландия": "Дублин",
    "Исландия": "Рейкьявик",
    "Испания": "Мадрид",
    "Италия": "Рим",
    "Кипр": "Никосия",
    "Латвия": "Рига",
    "Литва": "Вильнюс",
    "Люксембург": "Люксембург",
    "Мальта": "Валлетта",
    "Молдова": "Кишинев",
    "Монако": "Монако",
    "Нидерланды": "Амстердам",
    "Норвегия": "Осло",
    "Польша": "Варшава",
    "Португалия": "Лиссабон",
    "Румыния": "Бухарест",
    "Россия": "Москва",
    "Северная Македония": "Скопье",
    "Сербия": "Белград",
    "Словакия": "Братислава",
    "Словения": "Любляна",
    "Украина": "Киев",
    "Финляндия": "Хельсинки",
    "Франция": "Париж",
    "Хорватия": "Загреб",
    "Черногория": "Подгорица",
    "Чехия": "Прага",
    "Швейцария": "Берн",
    "Швеция": "Стокгольм",
    "Эстония": "Таллин"
}

# Функция для старта бота и приветственного сообщения
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f'Привет, {user.first_name}! Я помогу тебе выучить столицы европейских государств. Напиши /quiz, чтобы начать викторину!'
    )

# Функция для начала викторины
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    country = random.choice(list(countries_and_capitals.keys()))
    context.user_data['current_country'] = country
    await update.message.reply_text(
        f'Назови столицу страны: {country}'
    )

# Функция для проверки ответа пользователя
async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_answer = update.message.text
    correct_answer = countries_and_capitals.get(context.user_data.get('current_country'))

    if user_answer.lower() == correct_answer.lower():
        await update.message.reply_text(f'Правильно! Столица {context.user_data.get("current_country")} - {correct_answer}.')
    else:
        await update.message.reply_text(f'Неправильно. Столица {context.user_data.get("current_country")} - {correct_answer}.')
    
    # Задать следующий вопрос
    await quiz(update, context)

def main() -> None:
    # Инициализация бота с токеном
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

    application.run_polling()

if __name__ == '__main__':
    main()
