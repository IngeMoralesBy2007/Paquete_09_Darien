import httpx
from app.settings import settings

SERVICE_ID = f"{settings.pishop_service_name}-1"

async def registrar():
    payload = {
        "ID": SERVICE_ID,
        "Name": settings.pishop_service_name,
        "Address": settings.pishop_service_name,
        "Port": settings.pishop_http_port,
        "Check": {
            "HTTP": f"http://{settings.pishop_service_name}:{settings.pishop_http_port}/health/live",
            "Interval": "10s",
            "Timeout": "3s"
        }
    }
    async with httpx.AsyncClient() as client:
        try:
            await client.put(f"{settings.pishop_consul_url}/v1/agent/service/register", json=payload)
        except Exception as e:
            print(f"Error registrando en Consul: {e}")

async def dar_de_baja():
    async with httpx.AsyncClient() as client:
        try:
            await client.put(f"{settings.pishop_consul_url}/v1/agent/service/deregister/{SERVICE_ID}")
        except Exception as e:
            print(f"Error dando de baja en Consul: {e}")