import telebot
import threading
from telebot import types
from time import sleep
from gestion_pdf import createDirectoryPDF, savePDF, countPDFs, deleteAllPDF
from gestion_imagenes import verificate, createPDFtoImages, listImages, deleteAllImages



'''
REQUERIMENTS
$ pip install pyTelegramBotAPI
$ pip install pdf2image
$ pip install pypdf2
'''


msn_info = "A Bot [@HurquyPDF_Bot](https://t.me/HurquyPDF_Bot) that allow convert PDF to Images  \n\nThe Project [@HurquyPDF_Bot](https://t.me/HurquyPDF_Bot) \n__Github__: [jhonijlm](https://github.com/jhonijlm) \n__Twitter__: [jhnoijlm](https://twitter.com/jhonijlm) \nDonate: [jhonijlm](https://www.paypal.me/jhonijlm)"
msn_notice = "__RULES__ 📏\n\n ✅ Allow to make 10 images by PDF.\n\n ✅ Each PDF sent, has a waiting time of 3 minutes for convert to Images, in case it exceeds the estimated time the image is removed.\n\n ✅ Then of convert to Images , Delete all\n\n ✅ If the bot does not work, you can send /start to update the bot to the new version"


BOT_TOKEN = "1427302131:AAFLr2GEe74lPFT3n1bZyT_qyK1fobQqNlM"
BOT_INTERVAL = 3
BOT_TIMEOUT = 30

bot = telebot.TeleBot(BOT_TOKEN)

# Listen of the chatbot
def listener(mensaje_telegram):
    for mensaje in mensaje_telegram:
        chat_ID = mensaje.chat.id
        if(mensaje.content_type == "text"):
            if(mensaje.text == "PDF TO IMAGES 🖼"):
                if(verificate(chat_ID)):
                    bot.send_message(chat_ID, "Wait a moment please 🙂")
                    createPDFtoImages(chat_ID)
                    sleep(3)
                    loadImages(bot, chat_ID, listImages(chat_ID))
                    deleteAllImages(chat_ID)
                    deleteAllPDF(chat_ID)
                    bot.send_message(chat_ID, " ✅ 🙂")
                else:
                    bot.send_message(chat_ID, "You have not sent me any PDF 📄")
            elif(mensaje.text == "NOTICE 📢"):
                bot.send_message(chat_ID, msn_notice, parse_mode='MARKDOWN')
            elif(mensaje.text == "INFO ℹ"):
                bot.send_message(chat_ID, msn_info, parse_mode='MARKDOWN',disable_web_page_preview=True)
        elif(mensaje.content_type == "document"):

            if(countPDFs(chat_ID) <= 1):
                
                fileID = mensaje.document.file_id
                hilaDownload = threading.Thread(target=downloadPDF, args=(bot, fileID, chat_ID))
                hilaDownload.start()
            else:
                bot.send_message(chat_ID, "I'm Sorry, I can't process more than one PDF")

# listener
bot.set_update_listener(listener)

# bot main 
def bot_polling():
    print("EMPEZANDO BOT ...")
    while True:
        try:
            print("NEW INSTANCE OF BOT STARTED")
            # bot = telebot.TeleBot(BOT_TOKEN) #Generate new bot instance
            # If bot is used as a global variable, remove bot as an input param
            botactions(bot)
            bot.polling(none_stop=True, interval=BOT_INTERVAL,timeout=BOT_TIMEOUT)
        except Exception as ex:  # Error in polling
            print("WWARNING: SCANN BOT, RESTART ON {}sec. ERROR:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else:  # Clean exit
            bot.stop_polling()
            print("FINISHED BOT")
            break  # End loop

# bot actions
def botactions(bot):
    @bot.message_handler(commands=["start"])
    def command_start(message):
        msn = "Welcome " + message.chat.first_name + "  😊 to HurquyPDF, a convert of PDF to Images"
        chat_ID = message.chat.id
        bot.send_message(chat_ID, msn)
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        itembtn1 = types.KeyboardButton("PDF TO IMAGES 🖼")
        itembtn2 = types.KeyboardButton("NOTICE 📢")
        itembtn3 = types.KeyboardButton("INFO ℹ")
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(chat_ID, "Choose a option", reply_markup=markup)


# method for download documents
def downloadPDF(bot, file_ID, chatID):
    file_info = bot.get_file(file_ID)
    download = bot.download_file(file_info.file_path)
    namePDF = createDirectoryPDF(chatID)
    verificate = savePDF(namePDF, download)
    sleep(3)
    # if(verificate == True):
    #   bot.send_message(chatID, "pdf procesado")
    # elif (verificate == False):
    #    bot.send_message(chatID, "pdf corrupto")
    if (verificate == False):
        bot.send_message(chatID, "I'm sorry, apparently the document is corrupt 😞")


# method for send images to chatbot
def loadImages(bot ,chat_ID, listImages):
    print(listImages)
    for rutaImage in listImages:
        photo = open(rutaImage, "rb")
        bot.send_photo(chat_ID, photo)
        photo.close()


# Thread instance
polling_thread = threading.Thread(target=bot_polling)
polling_thread.daemon = True
polling_thread.start()


# Main execute Thread
if __name__ == "__main__":
    while True:
        try:
            sleep(120)
        except KeyboardInterrupt:
            break
