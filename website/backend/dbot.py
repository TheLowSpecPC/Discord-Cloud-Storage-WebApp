import website.backend.FileConverter as FileConverter
from website.backend.secrets import Your_Token
import website.backend.json_update as json_update
import nextcord, os, shutil
from nextcord.ext import commands
from time import sleep
import sys, re

token = Your_Token
intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix='!',intents=intents)
path_cwd = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()

def Upload(fileName, fileDir):
    FileConverter.split(fileName,fileDir)
    os.remove(path_cwd + f"\\upload\\{fileName}")

    file = os.listdir(path_cwd + f"\\out\\{fileName}\\")
    json_update.fileUpdate(fileName, str(len(file)), 'uptodis', 5)

    @bot.event
    async def on_ready():
        flag = 5
        channel = bot.get_channel(1116747276275155024)

        for i in range(len(file)):
            file[i] = path_cwd + f"\\out\\{fileName}\\" + file[i]

        print(f'{bot.user} has connected to Discord!')

        for i in range(len(file)):
            sleep(1)
            await channel.send(file=nextcord.File(file[i]), content=fileName + str(i + 1))
            print(file[i])
            if os.path.exists(file[i]):
                os.remove(file[i])

            flag += 96 / len(file)
            json_update.fileUpdate(fileName, str(len(file)), 'uptodis', flag)

            if i + 1 == len(file):
                os.rmdir(path_cwd + f"\\out\\{fileName}\\")
                print('Done!!!!!!!!!!!')
                json_update.fileUpdate(fileName, str(len(file)), 'uptodis', 100)

        json_update.fileUpdate(fileName, str(len(file)), 'inDiscord', 0)

        await bot.close()

    bot.run(token)

def Download(fileName, chunks):
    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
        channel = bot.get_channel(1116747276275155024)
        contents = []
        names = []
        flag = 5

        json_update.fileUpdate(fileName, chunks, 'downfromdis', flag)

        totalpart = int(chunks)
        for i in range(totalpart):
            names.append(fileName + str(i + 1))
        print(names)

        a = 1
        os.mkdir(path_cwd + f"\\out\\{fileName}\\")
        async for message in channel.history(limit=None):
            content = message.content
            contents.append(content)

            if a <= len(names):
                if content in names:
                    for attachment in message.attachments:
                        print(attachment.filename)
                        await attachment.save(attachment.filename)
                        shutil.move(cwd + "\\" + attachment.filename, path_cwd + f"\\out\\{fileName}\\" + attachment.filename)

                        flag += 95/len(names)
                        json_update.fileUpdate(fileName, chunks, 'downfromdis', flag)
                        if a == len(names):
                            FileConverter.join(fileName)
                            print("done")

                            folder = os.listdir(path_cwd + f"\\out\\{fileName}\\")
                            for i in range(len(folder)):
                                folder[i] = path_cwd + f"\\out\\{fileName}\\" + folder[i]
                            for i in range(len(folder)):
                                if os.path.exists(folder[i]):
                                    os.remove(folder[i])
                            if os.path.exists(path_cwd + f"\\out\\{fileName}\\"):
                                os.rmdir(path_cwd + f"\\out\\{fileName}\\")

                            json_update.fileUpdate(fileName, chunks, 'inServer', 0)
                        a += 1
            else:
                break

        await bot.close()

    bot.run(token)

def Delete(fileName, chunks):
    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
        channel = bot.get_channel(1116747276275155024)
        contents = []
        names = []
        flag = 5

        json_update.fileUpdate(fileName, chunks, 'deleting', flag)

        totalpart = int(chunks)
        for i in range(totalpart):
            names.append(fileName + str(i + 1))
        print(names)

        a = 0
        async for message in channel.history(limit=None):
            content = message.content
            contents.append(content)

            if a <= len(names):
                if content in names:
                    await message.delete()

                    flag += 95 / len(names)
                    json_update.fileUpdate(fileName, chunks, 'deleting', flag)
                    a += 1
            else:
                break
        json_update.fileDelete(fileName)

        await  bot.close()

    bot.run(token)

if sys.argv[1] == "send":
    Upload(sys.argv[2], sys.argv[3])
elif sys.argv[1] == "download":
    Download(sys.argv[2], sys.argv[3])
elif sys.argv[1] == "delete":
    Delete(sys.argv[2], sys.argv[3])