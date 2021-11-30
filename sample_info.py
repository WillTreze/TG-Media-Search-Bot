# Bot information
SESSION = 'Media_search'
USER_SESSION = 'User_Bot'
API_ID = 55555
API_HASH = ''
BOT_TOKEN = ''
USERBOT_STRING_SESSION = 'MyFiles'

# Bot settings
CACHE_TIME = 300
USE_CAPTION_FILTER = False

# Admins, Channels & Users
ADMINS = [55555]
CHANNELS = [-100123456, 'channelusername']
AUTH_USERS = [12345]
AUTH_CHANNEL = -10012345

# MongoDB information
DATABASE_URI = ""
DATABASE_NAME = ''
COLLECTION_NAME = 'Telegram_files'  # If you are using the same database, then use different collection name for each bot

# Messages
START_MSG = """
**Hi, I'm Media Search bot**
Here you can search files in inline mode. Just press follwing buttons and start searching.
"""

SHARE_BUTTON_TEXT = 'Checkout {username} for searching files'
INVITE_MSG = 'Please join @.... to use this bot'