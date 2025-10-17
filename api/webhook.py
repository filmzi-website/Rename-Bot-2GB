from http.server import BaseHTTPRequestHandler
import json

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
            
            # Log the received data (for debugging)
            print(f"Received POST data: {post_data.decode('utf-8')[:200]}")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "success",
                "message": "Webhook received successfully",
                "developer": "JishuDeveloper"
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Error processing webhook: {str(e)}")
