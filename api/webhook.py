from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import asyncio
import logging

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from pyrogram import Client, filters
    from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
    from config import Config
    PYRAGRAM_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Pyrogram import failed: {e}")
    PYRAGRAM_AVAILABLE = False

# Global bot instance (reused across invocations)
bot_instance = None

async def get_bot():
    """Get or create bot instance"""
    global bot_instance
    if bot_instance is None:
        bot_instance = Client(
            "renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins={"root": "plugins"},
            sleep_threshold=15,
            in_memory=True
        )
        await bot_instance.start()
    return bot_instance

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Health check endpoint"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "status": "running",
            "bot": "JishuBotz - Rename Bot",
            "pyrogram": PYRAGRAM_AVAILABLE,
            "developer": "@JishuDeveloper",
            "features": "File Renaming | Thumbnail | MongoDB"
        }
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle Telegram webhook with Pyrogram"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data)
            
            # Process update asynchronously
            asyncio.run(self.process_pyrogram_update(update))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "processed"}).encode())
            
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            self.send_error(500, f"Error: {str(e)}")
    
    async def process_pyrogram_update(self, update):
        """Process update using Pyrogram"""
        try:
            bot = await get_bot()
            
            # Handle different update types
            if 'message' in update:
                await self.handle_message(bot, update['message'])
            elif 'callback_query' in update:
                await self.handle_callback(bot, update['callback_query'])
                
        except Exception as e:
            logger.error(f"Process update error: {e}")
    
    async def handle_message(self, bot, message):
        """Handle incoming messages"""
        try:
            chat_id = message['chat']['id']
            text = message.get('text', '')
            
            if text.startswith('/start'):
                await self.send_telegram_message(
                    chat_id,
                    f"🚀 **Welcome to Rename Bot!** \n\n"
                    f"I can rename files and more! \n\n"
                    f"**Developer:** @JishuDeveloper \n"
                    f"**Host:** Vercel \n\n"
                    f"Send me a file to rename it! 📁"
                )
            
            elif text.startswith('/help'):
                await self.send_telegram_message(
                    chat_id,
                    "🤖 **Available Commands:** \n\n"
                    "📁 **File Operations:**\n"
                    "/rename - Rename files\n"
                    "/thumbnail - Set custom thumbnail\n"
                    "/viewthumb - View current thumbnail\n"
                    "/delthumb - Delete thumbnail\n\n"
                    "🔧 **Bot Settings:**\n"
                    "/settings - Configure bot\n"
                    "/mode - Change upload mode\n\n"
                    "📊 **Info:**\n"
                    "/status - Bot status\n"
                    "/about - About this bot\n\n"
                    "**Powered by @JishuDeveloper** 🚀"
                )
            
            elif text.startswith('/about'):
                await self.send_telegram_message(
                    chat_id,
                    "🤖 **About Rename Bot:** \n\n"
                    "✨ **Features:**\n"
                    "• Rename files with custom names\n"
                    "• Custom thumbnail support\n"
                    "• Multiple upload modes\n"
                    "• MongoDB database\n"
                    "• Vercel hosting\n\n"
                    "👨‍💻 **Developer:** @JishuDeveloper\n"
                    "📢 **Channel:** @MadflixBotz\n"
                    "🔧 **Support:** @MadflixSupport\n\n"
                    "**Thanks for using!** ❤️"
                )
            
            # Check if message contains a file
            elif any(key in message for key in ['document', 'video', 'audio', 'photo']):
                await self.handle_file_message(bot, message)
            
            else:
                await self.send_telegram_message(
                    chat_id,
                    f"📨 **Message Received** \n\n"
                    f"You said: `{text}` \n\n"
                    f"Send me a file to rename it, or use /help for commands."
                )
                
        except Exception as e:
            logger.error(f"Handle message error: {e}")
    
    async def handle_file_message(self, bot, message):
        """Handle file messages - integrate your rename logic here"""
        try:
            chat_id = message['chat']['id']
            
            # Get file information
            file_info = self.extract_file_info(message)
            
            await self.send_telegram_message(
                chat_id,
                f"📁 **File Received** \n\n"
                f"**File Name:** `{file_info['name']}`\n"
                f"**File Size:** {file_info['size']}\n"
                f"**File Type:** {file_info['type']}\n\n"
                f"Please send the new name for this file...\n\n"
                f"Example: `MyRenamedFile.mp4`"
            )
            
            # Here you would integrate your actual rename logic
            # from plugins.rename import process_rename_request
            # await process_rename_request(bot, message)
            
        except Exception as e:
            logger.error(f"Handle file error: {e}")
            await self.send_telegram_message(chat_id, "❌ Error processing file. Please try again.")
    
    def extract_file_info(self, message):
        """Extract file information from message"""
        file_info = {'name': 'Unknown', 'size': 'Unknown', 'type': 'Unknown'}
        
        try:
            if 'document' in message:
                doc = message['document']
                file_info['name'] = doc.get('file_name', 'Document')
                file_info['size'] = self.format_size(doc.get('file_size', 0))
                file_info['type'] = 'Document'
            elif 'video' in message:
                video = message['video']
                file_info['name'] = 'Video File'
                file_info['size'] = self.format_size(video.get('file_size', 0))
                file_info['type'] = 'Video'
            elif 'audio' in message:
                audio = message['audio']
                file_info['name'] = audio.get('file_name', 'Audio File')
                file_info['size'] = self.format_size(audio.get('file_size', 0))
                file_info['type'] = 'Audio'
            elif 'photo' in message:
                file_info['name'] = 'Photo'
                file_info['size'] = 'Unknown'
                file_info['type'] = 'Photo'
                
        except Exception as e:
            logger.error(f"Extract file info error: {e}")
            
        return file_info
    
    def format_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names)-1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.2f} {size_names[i]}"
    
    async def send_telegram_message(self, chat_id, text, reply_markup=None):
        """Send message via Telegram API"""
        try:
            url = f"https://api.telegram.org/bot{Config.BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'Markdown',
                'reply_markup': reply_markup
            }
            
            import requests
            response = requests.post(url, json=payload, timeout=10)
            return response.json()
            
        except Exception as e:
            logger.error(f"Send message error: {e}")
    
    async def handle_callback(self, bot, callback_query):
        """Handle callback queries"""
        try:
            chat_id = callback_query['message']['chat']['id']
            data = callback_query['data']
            
            # Handle different callback actions
            if data == 'help':
                await self.handle_message(bot, {
                    'chat': {'id': chat_id},
                    'text': '/help'
                })
                
        except Exception as e:
            logger.error(f"Handle callback error: {e}")
