import requests
from config import tg_token, token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=("start"))
async def start_command(message: types.Message):

    Markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    moscow = types.KeyboardButton('Москва', callback_data='moscow')
    piter = types.KeyboardButton('Санкт Петербург', callback_data='piter')
    Markup.add(moscow, piter)



    await message.answer_sticker(r"CAACAgIAAxkBAAEBe8Zg1HN5L0qxJFe6yy_2yTgYK7BGSAAC2wADUomRI5rH22s7rj__HwQ")

    await message.reply("***Доброго времени суток, напишите мне название города "
                        "и я отправлю вам сведения о погоде в нём!***\n***Если хотите узнать "
                        "больше информации о боте, пропишите команду '/info' !***", reply_markup=Markup)

@dp.message_handler(commands=("info"))
async def info_command(message: types.Message):


    await message.reply("Спасибо что заинтересовались дополнительной информацией о боте!\n"
                        "Данный бот умеет определять погодные условия во всех городах мира, "
                        "определять среднюю температуру в любой стране.\nНаписал данного "
                        "ботa: Гapницкий Aлекcaндp, студент РТУ МИРЭА, группы БСБО-07-19.\n"
                        "Проект подготовил для предмета: Интерпретируемый язык "
                        "программирования высокого уровня. "
                        "Преподаватель: Тарланов Арслан Арсланович")


@dp.message_handler()
async def get_weather(message: types.Message):

    site = types.InlineKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    gesmet = types.InlineKeyboardButton(text='Бот берёт погоду с этого сайта'
                                        ,url='https://openweathermap.org')
    site.add(gesmet)

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token}&units=metric"
        )

        data = r.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]


        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "На улице происходит что-то, чего нет " \
                 "в моей базе знаний, посмотри в окно!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        d = "{0:.2f}".format(round(pressure / 1.3322, 1))

        if cur_weather > 30:
            await message.answer_sticker(r"CAACAgIAAxkBAAEBe7Jg1G8usE5nEpRREPnTcEYIR19RSQAC2AADUomRI2V0cN023Kl6HwQ")
        elif cur_weather > 20:
            await message.answer_sticker(r"CAACAgIAAxkBAAEBe7dg1G-U2Ibkt59FgSI2T1rZz2kybgACxAADUomRI-xxLnj5ti4GHwQ")
        elif cur_weather > 10:
            await message.answer_sticker(r"CAACAgIAAxkBAAEBe7pg1HASBQR6vfGx5kbDfdkinq5EhgACwgADUomRI3_cQZkoHaRNHwQ")
        elif cur_weather > 0:
            await message.answer_sticker(r"CAACAgIAAxkBAAEBe71g1HByFzNNncdV81qmL5HdOKG5lAACxgADUomRIzmUbbF6xf1YHwQ")
        elif cur_weather < 0:
            await message.answer_sticker(r"CAACAgIAAxkBAAEBe8Bg1HCcqjVKWm9yfPNOnXNiEVtyOwACyQADUomRI2QzL5Ov-ocxHwQ")
        elif cur_weather < 10:
            await message.answer_sticker(r"CAACAgIAAxkBAAEBe8Ng1HC7cc4NkX69hOgMvEVZF2QlxgACygADUomRIz3-U_49GT0EHwQ")
        elif cur_weather < 20:
            await message.answer_sticker(r"CAACAgIAAxkBAAEBfWZg1gja8aZ7IbNIhE8nPGS2vRxhDAACygADUomRIz3-U_49GT0EIAQ")

        await message.reply(f"\U0001F30F\U0001F30D\U0001F30E Город: {city}\U0001F30E\U0001F30D\U0001F30F"
                            f"\nТемпература: {cur_weather}C°  {wd}\nВлажность: {humidity}%\n"
                            f"Давление: {d} мм.рт.ст\nСкорость ветра: {wind} м/c", reply_markup=site)


    except:
        await message.reply("\U0001F622 К сожалению такого города в моей базе нет \U0001F622")

if __name__ == '__main__':
    executor.start_polling(dp)