import os
import time
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import START_MSG, CHANNELS, ADMINS, INVITE_MSG
from utils import Media

logger = logging.getLogger(__name__)


@Client.on_message(filters.command('start'))
async def start(bot, message):
    """Start command handler"""
    if len(message.command) > 1 and message.command[1] == 'subscribe':
        tmp_msg = await message.reply(INVITE_MSG)
                
        time.sleep(5)
        await tmp_msg.delete()
    else:
        buttons = [[
            InlineKeyboardButton('Search Here', switch_inline_query_current_chat=''),
            InlineKeyboardButton('Go Inline', switch_inline_query=''),
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        tmp_msg = await message.reply(START_MSG, reply_markup=reply_markup)
                
        time.sleep(5)
        await tmp_msg.delete()


@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        tmp_msg = await message.reply(text)
        
        time.sleep(5)
        await tmp_msg.delete()
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        tmp_msg = await message.reply_document(file)
        os.remove(file)
        
        time.sleep(5)
        await tmp_msg.delete()


@Client.on_message(filters.command('total') & filters.user(ADMINS))
async def total(bot, message):
    """Show total files in database"""
    msg = await message.reply("Processing...⏳", quote=True)
    try:
        total = await Media.count_documents()
        tmp_msg = await msg.edit(f'📁 Saved files: {total}')
        
        time.sleep(5)
        await tmp_msg.delete()
    except Exception as e:
        logger.exception('Failed to check total files')
        tmp_msg = await msg.edit(f'Error: {e}')
                
        time.sleep(5)
        await tmp_msg.delete()


@Client.on_message(filters.command('logger') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))


@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type,
        'caption': reply.caption.html if reply.caption else None
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        await msg.edit('File not found in database')
