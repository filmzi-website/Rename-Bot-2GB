from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import asyncio

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "success", 
                "message": "🤖 JishuBotz is Running on Vercel!",
                "developer": "@JishuDeveloper",
                "bot": "Rename-Bot-2GB",
                "endpoints": {
                    "root": "/",
                    "webhook": "/webhook (POST)",
                    "health": "/health"
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
    
    def do_POST(self):
        """Handle POST requests (Telegram webhook)"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
            update = json.loads(post_data)
            
            # Process Telegram update
            response = self.process_telegram_update(update)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Error processing webhook: {str(e)}")
    
    def process_telegram_update(self, update):
        """Process Telegram update with your bot logic"""
        try:
            # Basic Telegram update processing
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                text = message.get('text', '')
                
                # Your bot commands
                if text.startswith('/start'):
                    return {
                        "method": "sendMessage",
                        "chat_id": chat_id,
                        "text": "🚀 Welcome to JishuBotz!\n\nI'm successfully hosted on Vercel!\n\nDeveloper: @JishuDeveloper"
                    }
                elif text.startswith('/help'):
                    return {
                        "method": "sendMessage", 
                        "chat_id": chat_id,
                        "text": "🤖 Bot Help:\n\n/start - Start bot\n/help - This message\n\nHosted on Vercel 🚀"
                    }
                else:
                    return {
                        "method": "sendMessage",
                        "chat_id": chat_id,
                        "text": f"📨 You said: {text}\n\nBot is working on Vercel!"
                    }
            
            return {"status": "processed"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
