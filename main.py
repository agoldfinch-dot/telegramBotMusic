import os
import requests

from aiogram import Bot, Dispatcher, executor, types
from pytube import YouTube, Search

API_TOKEN = ...

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['ищи','search'])
async def search(message: types.Message):
    try:
        text = message.text
        text = text.split(' ')
        text.pop(0)
        searchText = ' '.join(text)
        s = Search(searchText)
        endUrl = s.results[0].watch_url
        await download(endUrl, message)
    except Exception as e:
        print(e)
        await message.reply('ничего нет')

@dp.message_handler(commands=['it','это'])
async def direct_url(message: types.Message):
    try:
        url = message.text.split(' ')[1]
        await download(url, message)
    except Exception as e:
        print(e)
        await message.reply('сломалось')

async def download(url, message):
    yt = YouTube(url) 
    if yt.length//60 >= 30:
        await message.answer(f'Видео слишком длинное (более 30 минут)!\nОтмена!\n{yt.watch_url}')
        return;
    video = yt.streams.filter(abr='160kbps').last()
    ss = video.download()
    thumb = requests.get(yt.thumbnail_url).content
    os.rename(ss, f"{message.from_user.id}.mp3")

    await bot.send_audio(message.chat.id, open(str(message.from_user.id) + ".mp3", 'rb'),  title = yt.title, performer=yt.author, thumb=thumb)
    os.remove(f'{os.getcwd()}/{message.from_user.id}.mp3')

executor.start_polling(dp, skip_updates=True)