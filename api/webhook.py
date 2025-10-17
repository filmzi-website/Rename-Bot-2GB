from aiohttp import web
import asyncio
import json

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({
        "message": "JishuBotz - Running on Vercel 🚀",
        "status": "active",
        "developer": "@JishuDeveloper"
    })

@routes.post("/webhook")
async def telegram_webhook(request):
    """Handle Telegram webhook updates"""
    try:
        data = await request.json()
        print(f"Received update: {data}")
        
        # Add your bot processing logic here
        # await process_telegram_update(data)
        
        return web.json_response({"status": "success"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

@routes.get("/health")
async def health_check(request):
    return web.json_response({"status": "healthy"})

# Create app
app = web.Application()
app.add_routes(routes)

# Vercel handler
async def main(request):
    """Vercel serverless entry point"""
    return await app._handle_request(request)
