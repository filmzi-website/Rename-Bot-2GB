from aiohttp import web
import asyncio
import json
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your bot components
try:
    from bot import main_bot
    BOT_AVAILABLE = True
except ImportError:
    BOT_AVAILABLE = False

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({
        "message": "JishuBotz - Running on Vercel 🚀",
        "bot_status": "active" if BOT_AVAILABLE else "not available",
        "developer": "@JishuDeveloper"
    })

@routes.post("/webhook")
async def telegram_webhook(request):
    """Handle Telegram webhook updates"""
    try:
        data = await request.json()
        
        # Process with your bot if available
        if BOT_AVAILABLE:
            # Adapt this to your bot's update processing
            # await main_bot.process_update(data)
            print(f"Received update: {data}")
        
        return web.json_response({"status": "success"})
        
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

@routes.get("/health")
async def health_check(request):
    return web.json_response({"status": "healthy", "server": "aiohttp"})

# Create app
async def create_app():
    app = web.Application(client_max_size=30000000)
    app.add_routes(routes)
    return app

# Vercel handler
app = asyncio.run(create_app())

async def main(request):
    """Vercel serverless entry point"""
    handler = app.make_handler()
    response = await handler(request)
    return response
