import logging
from decouple import config
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from repository import GroupRepository
from repository import MessageRepository
from repository import GroupMessageRepository

TOKEN = config('TOKEN')
BOT_NAME = config('BOT_NAME')

# Create logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
job_queue = updater.job_queue

# Create repositories
group_repository = GroupRepository()
message_repository = MessageRepository()
group_message_repository = GroupMessageRepository()


def new_member(update, context):
    for member in update.message.new_chat_members:
        if member.username == BOT_NAME:
            group_repository.create(
                update.message.chat.title, update.message.chat.id)


def send_scheduled_messages(context):
    scheduled_messages = group_message_repository.get_scheduled_messages_to_current_time()
    for scheduled_message in scheduled_messages:
        context.bot.send_message(chat_id=scheduled_message.group.telegram_id,
                                    text=scheduled_message.message.content, disable_web_page_preview=False)


# - Setup job queue
# Sends scheduled messages to the current time
job_queue.run_repeating(send_scheduled_messages, interval=60, first=0)

# - Setup handlers
# When the bot is added to any group, the
# group must be registered in the database
dispatcher.add_handler(MessageHandler(
    Filters.status_update.new_chat_members, new_member))

# - Watch telegram updates
updater.start_polling()
updater.idle()
