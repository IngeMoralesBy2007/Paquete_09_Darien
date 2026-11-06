from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
import httpx
from app.registro import registrar, dar_de_baja
from app.settings import settings

round_robin_counters = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    await registrar()
    yield
    await dar_de_baja()

app = FastAPI(
    title="PiShop Cloud - Descubridor Service (P09)",
    version="1.0.0",
    lifespan=lifespan
)

CONSUL_URL = getattr(settings, "pishop_consul_url", "http://localhost:8500")

@app.get("/health/live", status_code=status.HTTP_200_OK)
async def health_live():
    return {"status": "alive"}

@app.get("/health/ready", status_code=status.HTTP_200_OK)
async def health_ready():
    return {"status": "ready"}

@app.get("/health/startup", status_code=status.HTTP_200_OK)
async def health_startup():
    return {"status": "started"}

@app.get("/v1/servicios")
async def listar_servicios():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CONSUL_URL}/v1/agent/services")
            if response.status_code != 200:
                raise HTTPException(status_code=502, detail="Error conectando con Consul")
            
            services = response.json()
            # Devolvemos una lista limpia con los nombres de los servicios registrados
            return [service.get("Service", name) for name, service in services.items()]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno procesando servicios: {str(e)}")

@app.get("/v1/instancias/{service_name}")
async def listar_instancias(service_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CONSUL_URL}/v1/health/service/{service_name}?passing=true")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Servicio no encontrado o sin instancias")
        
        data = response.json()
        instances = [
            {
                "id": entry["Service"]["ID"],
                "address": entry["Service"]["Address"],
                "port": entry["Service"]["Port"]
            }
            for entry in data
        ]
        return instances

@app.get("/v1/resolver/{service_name}")
async def resolver_instancia(service_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CONSUL_URL}/v1/health/service/{service_name}?passing=true")
        if response.status_code != 200 or not response.json():
            raise HTTPException(status_code=404, detail="No hay instancias saludables (passing)")
        
        data = response.json()
        instances = [
            {
                "id": entry["Service"]["ID"],
                "address": entry["Service"]["Address"],
                "port": entry["Service"]["Port"]
            }
            for entry in data
        ]
        
        if service_name not in round_robin_counters:
            round_robin_counters[service_name] = 0
        
        index = round_robin_counters[service_name] % len(instances)
        round_robin_counters[service_name] = index + 1
        
        return instances[index]