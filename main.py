import discord
import credits
from discord.ext import commands
from random import randint
from os import remove 
from time import sleep
from model.model import get_class
from imageai.Detection import ObjectDetection

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command('photo')
async def photo(ctx):
   if ctx.message.attachments:
       for attachment in ctx.message.attachments:
           file_name = attachment.filename
           if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png') or file_name.endswith('.avif'): 
                await attachment.save(f'./images/{file_name}')
                msg = await ctx.send('ведем подсчеты...')
                class_name, confidence = get_class(model_path='model/keras_model.h5', labels_path='model/labels.txt', image_path=f'./images/{file_name}')
                await msg.delete()
                await ctx.send(f'С вероятностью {confidence}% это {class_name.lower()}')
                remove(f'./images/{file_name}')
           else:
               await ctx.send('Неправильный формат файлов!')
               return
   else:
       await ctx.send("Кажется, ты забыл прикрепить фото")         

bot.run("YOUR TOKEN")     
