from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

BTN_TODAY = InlineKeyboardButton('Сегодня', callback_data='today')
BTN_MONTH = InlineKeyboardButton('Месяц', callback_data='month')
BTN_EXPENSES = InlineKeyboardButton('Последнее', callback_data='expenses')
BTN_CATEGORIES = InlineKeyboardButton('Категории', callback_data='categories')

# START = ReplyKeyboardMarkup().add(BTN_START)

TODAY = InlineKeyboardMarkup().add(BTN_MONTH, BTN_EXPENSES, BTN_CATEGORIES)
MONTH = InlineKeyboardMarkup().add(BTN_TODAY, BTN_EXPENSES, BTN_CATEGORIES)
EXPENSES = InlineKeyboardMarkup().add(BTN_TODAY, BTN_MONTH, BTN_CATEGORIES)
CATEGORIES = InlineKeyboardMarkup().add(BTN_TODAY, BTN_MONTH, BTN_EXPENSES)
ALL = InlineKeyboardMarkup().add(BTN_TODAY, BTN_MONTH, BTN_EXPENSES, BTN_CATEGORIES)