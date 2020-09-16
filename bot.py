from telegram.ext import Updater
import os
import telegram.utils

PORT = int(os.environ.get('PORT', 5000))
TOKEN = ''
#group members have to be added in manually or thru some other script
#current telegram libraries do not have feature to poll for all group members automatically
group_chat = []
alert_message = ""

def alert_user(update, context):
	try:
		context.user_data['counter'] += 1
	except:
		context.user_data['counter'] = 0
	if context.user_data['counter'] == 20:
		context.bot.send_message(chat_id=update.effective_chat.id, text=alert_message, reply_to_message_id=update.message.message_id)
		context.user_data['counter'] = 0

def produce_parsed_text(calling_user):
	acc = ""
	for e in group_chat:
		if e[0] != calling_user.id:
			acc += telegram.utils.helpers.mention_html(e[0],e[1]) + " "
	return acc

def alert_chat(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text=produce_parsed_text(update.effective_user), parse_mode='HTML')

from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import filters
def main():
	updater = Updater(token=TOKEN, use_context=True)

	dispatcher = updater.dispatcher
	user_handler = MessageHandler(filters.Filters.group & filters.Filters.user(), alert_user)
	alert_all_handler = CommandHandler('chat_alert', alert_chat)
	dispatcher.add_handler(alert_all_handler)
	dispatcher.add_handler(user_handler)
	updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
	updater.bot.setWebhook('' + TOKEN)
	#updater.idle()

if __name__ == "__main__":
	main()