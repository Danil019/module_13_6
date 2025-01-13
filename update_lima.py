from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

key_api = '7663863093:AAHBqmiFkF15GWjTPKjsmgb68wyN-Iz8QVg'
bot = Bot(token=key_api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = InlineKeyboardMarkup(resize_keyboard = True)
button_age = InlineKeyboardButton(text = 'Рассчитать', callback_data='calories')
button_info = InlineKeyboardButton(text = 'Формула', callback_data='formulas')
kb.add(button_age, button_info)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = ['start'])
async def main_menu(message):
    await message.answer("Этот бот подсчитывает калории, чтобы активировать, нажмите на кнопку 'Рассчитать'. "
                         "\nТакже, можете посмотреть формулу расчёта калорий, нажав на кнопку 'Формула'",
                         reply_markup = kb)

@dp.callback_query_handler(text = "calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(first = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(second = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(third = message.text)
    data = await state.get_data()
    bmr = 10 * float(data['third']) + 6.25 * float(data['second']) - 5 * float(data['first']) + 5
    await message.answer(f"Ваша норма калорий: {bmr}")
    await state.finish()

@dp.callback_query_handler(text = "formulas")
async def get_formulas(call):
    await call.message.answer('10 x вес(кг) + 6.25 x рост(см) - 5 * возраст + 5')
    await call.answer()

@dp.message_handler()
async def start(message):
    await message.answer("Привет! Чтобы начать, чтобы меня активировать нужна команда /start")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)