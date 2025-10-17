from aiohttp import web
import json

async def handle_get(request):
    return web.json_response({
        "status": "success",
        "message": "JishuBotz - Vercel",
        "developer": "@JishuDeveloper"
    })

async def handle_webhook(request):
    try:
        # For GET requests
        if request.method == 'GET':
            return await handle_get(request)
        
        # For POST requests (Telegram webhook)
        if request.method == 'POST':
            data = await request.json()
            print("Webhook data:", data)
            
            # Add your bot logic here
            # await process_telegram_update(data)
            
            return web.json_response({"status": "success"})
            
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

# Create application
app = web.Application()

# Add routes
app.router.add_get('/', handle_get)
app.router.add_get('/webhook', handle_get)
app.router.add_post('/webhook', handle_webhook)
app.router.add_get('/health', handle_get)

# Vercel handler
async def main(request):
    return await app._handle_request(request)
