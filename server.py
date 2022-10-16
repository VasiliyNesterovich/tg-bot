"""Сервер Telegram бота, запускаемый непосредственно"""
from email import message
import logging
import os
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

import exceptions
import expenses
from categories import Categories
from middlewares import AccessMiddleware
from inline_keyboard import TODAY, MONTH, EXPENSES, CATEGORIES, ALL
import buffer



logging.basicConfig(level=logging.INFO)

# API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
API_TOKEN = "5739568300:AAEfr1V8gMIgVR0MHCb3TIHK7U3TGwTXdyQ"
# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
# ACCESS_ID = 357607331

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# dp.middleware.setup(AccessMiddleware(ACCESS_ID))



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    
    buffer.user_id = message.from_user.id
    await message.answer(
        "Бот для учёта финансов\n\n"
        "Добавить расход: 5 такси\n"
        "Сегодняшняя статистика: /today\n"
        "За текущий месяц: /month\n"
        "Последние внесённые расходы: /expenses\n"
        "Категории трат: /categories", reply_markup=ALL)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    
    buffer.user_id = message.from_user.id
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Удалил"
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Отправляет список категорий расходов"""
    
    buffer.user_id = message.from_user.id
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " +\
            ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories]))
    await message.answer(answer_message, reply_markup=CATEGORIES)

@dp.callback_query_handler(text='categories')
async def callback_categories_list(callback_query):
    """Отправляет список категорий расходов"""
    
    buffer.user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " +\
            ("\n* ".join([c.name+' ('+", ".join(c.aliases)+')' for c in categories]))
    await bot.send_message(callback_query.from_user.id, text=answer_message, reply_markup=CATEGORIES)

@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    
    buffer.user_id = message.from_user.id
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message, reply_markup=TODAY)

@dp.callback_query_handler(text='today')
async def callback_today_statistics(callback_query):
    """Отправляет сегодняшнюю статистику трат"""
    
    buffer.user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    answer_message = expenses.get_today_statistics()
    await bot.send_message(callback_query.from_user.id, text=answer_message, reply_markup=TODAY)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    
    buffer.user_id = message.from_user.id
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message, reply_markup=MONTH)

@dp.callback_query_handler(text='month')
async def callback_month_statistics(callback_query):
    """Отправляет статистику трат текущего месяца"""
    
    buffer.user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    answer_message = expenses.get_month_statistics()
    await bot.send_message(callback_query.from_user.id, text=answer_message, reply_markup=MONTH)


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    
    buffer.user_id = message.from_user.id
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Нет ни одной суммы.")
        return
    
    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние внесенные суммы:\n\n* " + "\n\n* "\
            .join(last_expenses_rows)
    await message.answer(answer_message, reply_markup=EXPENSES)

@dp.callback_query_handler(text='expenses')
async def callback_list_expenses(callback_query):
    """Отправляет последние несколько записей о расходах"""
    
    buffer.user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    last_expenses = expenses.last()
    if not last_expenses:
        await bot.send_message(callback_query.from_user.id, text="Нет ни одной суммы.")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние внесенные суммы:\n\n* " + "\n\n* "\
            .join(last_expenses_rows)
    await bot.send_message(callback_query.from_user.id, text=answer_message, reply_markup=EXPENSES)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новый расход"""
    
    buffer.user_id = message.from_user.id
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлена сумма {expense.amount} руб на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message, reply_markup=ALL)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
