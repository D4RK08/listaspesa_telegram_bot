import telegram
import json
from telegram.ext import Updater, CommandHandler

authorized_users = [1020841691,43488628,124172379,5574808702]

def lista(update, context):
    user_id = update.message.from_user.id
    if user_id in authorized_users:
        with open("messages.json", "r") as f:
            json_data = json.load(f)
            try:
                update.message.reply_text("\n".join(json_data["spesa"]))
            except KeyError:
                update.message.reply_text("La lista degli acquisti è vuota.")

def comprato(update, context):
    user_id = update.message.from_user.id
    if user_id in authorized_users:
        message_to_delete = update.message.text.replace("/comprato ","")
        message_to_delete = message_to_delete.lower()
        with open("messages.json", "r") as f:
            json_data = json.load(f)
            try:
                for i, msg in enumerate(json_data["spesa"]):
                    if msg == message_to_delete:
                        json_data["spesa"].pop(i)
                        break
                else:
                    update.message.reply_text("Messaggio non trovato")
                    return
                with open("messages.json", "w") as f:
                    json.dump(json_data, f)
                update.message.reply_text("Elemento eliminato con successo")
            except KeyError:
                update.message.reply_text("La lista degli acquisti è vuota.")



def message_handler(update, context):
    user_id = update.message.from_user.id
    if user_id in authorized_users:
        text = update.message.text
        text = text.lower()
        with open("messages.json", "r") as f:
            json_data = json.load(f)
        if "spesa" not in json_data:
            json_data["spesa"] = []
        json_data["spesa"].append(text)
        with open("messages.json", "w") as f:
            json.dump(json_data, f)

updater = Updater(token="5579776570:AAEqSd8MEKt6muENDpeq5OEbrNgxzVeKeVc", use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("lista", lista))
dispatcher.add_handler(CommandHandler("comprato", comprato))
dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, message_handler))

updater.start_polling()
