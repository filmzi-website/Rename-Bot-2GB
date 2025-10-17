from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import asyncio

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    # Import your existing bot
    from bot import main_bot
    from config import *
except ImportError as e:
    print(f"Import error: {e}")

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests (health check)"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'🤖 Bot is running on Vercel!')
    
    def do_POST(self):
        """Handle Telegram webhook updates"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data)
            
            # Process the update
            asyncio.run(self.process_telegram_update(update))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({"status": "success"})
            self.wfile.write(response.encode())
            
        except Exception as e:
            print(f"Error processing update: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = json.dumps({"status": "error", "message": str(e)})
            self.wfile.write(error_response.encode())
    
    async def process_telegram_update(self, update):
        """Process Telegram update using your existing bot"""
        try:
            # If your main_bot can handle updates directly
            if 'main_bot' in globals():
                await main_bot.process_update(update)
            else:
                # Alternative: Use your existing route.py logic
                from route import app
                # Adapt based on your route.py structure
                print(f"Processing update: {update}")
        except Exception as e:
            print(f"Error in process_telegram_update: {e}")
