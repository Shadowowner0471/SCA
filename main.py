import asyncio
import requests
import random
import time
from faker import Faker
from aiogram import Bot
from aiogram.types import InputFile
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import live

fake = Faker()

def luhn_algorithm(card_number):
    digits = [int(d) for d in str(card_number) if d.isdigit()]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

async def send_messages():
    bot = Bot(token='7195176470:AAGYLaHq7oR7JejT1mer1WBGhpXpL4pIKLk')
    chat_id = -1002500129281

    try:
        with open('cards.txt') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("cards.txt not found.")
        return

    requests_limit = 1
    pause_duration = 1

    for i, line in enumerate(lines, start=1):
        line = line.strip()
        parts = line.split("|")
        if len(parts) < 1:
            print(f"Invalid card in position {i}: {line}")
            continue

        card_number = ''.join(filter(str.isdigit, parts[0]))
        if len(card_number) < 12 or not luhn_algorithm(card_number):
            print(f"Invalid card in position {i}: {line}")
            continue

        BIN = card_number[:6]
        try:
            req = requests.get(f"https://bins.antipublic.cc/bins/{BIN}").json()
            brand = req['brand']
            country = req['country']
            country_name = req['country_name']
            country_flag = req['country_flag']
            country_currencies = req['country_currencies']
            bank = req['bank']
            level = req['level']
            typea = req['type']
        except (KeyError, ValueError) as e:
            print(f"Error with BIN lookup: {e}")
            continue

        month = str(random.randint(1, 12)).zfill(2)
        year = str(random.randint(24, 32)).zfill(2)
        full_name = fake.name()
        address = fake.address()

        photo_path = "scrap.jpg"

        try:
            photo = InputFile(photo_path)

            button_consultas = InlineKeyboardButton("CHANNEL", url="https://t.me/+p-27K6Lw2qE2MTM1")
            keyboard = [[button_consultas]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            message = (
                "\n"
                " GALAXY CARDER Scrapper 🐍\n"
                "━━━━━━━━━━━━━━\n"
                f"<b>⌖ 𝗖𝗰 ⤳</b> <code>{line}</code>\n"
                "⌖ 𝗦𝘁𝗮𝘁𝘂𝘀 ⤳ APPROVED  ✅\n"
                f"⌖ 𝗕𝗶𝗻 ⤳ #Bin{BIN}\n"
                "━━━━━━━━━━━━━━\n"
                f"<b>⌮ 𝗜𝗻𝗳𝗼 ⤳ </b>  <code>{brand}-{typea}-{level}</code>\n"
                f"<b>⌮ Bank ⤳ </b>  <code>{bank}</code>\n"
                f"<b>⌮ Country ⤳ </b>  <code>{country_name} [{country_flag}]</code>\n"
                "━━━━━━━━━━━━━━\n"
                f"<b>⌮ 𝐄𝐱𝐭𝐫𝐚 ⤳ </b>  <code>{card_number}xxxx|{month}|{year}|rnd</code>\n"
                "⌖  MADE BY ⤳ GALAXY CARDER\n"
                "━━━━━━━━━━━━━━\n"
            )

            await bot.send_photo(
                chat_id,
                photo,
                caption=message,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Error sending message or loading image: {e}")
            continue

        if i % requests_limit == 0 and i != len(lines):
            print(f"Request limit reached. Pausing {pause_duration} seconds...")
            time.sleep(pause_duration)

    await bot.session.close()

live()

if __name__ == '__main__':
    asyncio.run(send_messages())
    
