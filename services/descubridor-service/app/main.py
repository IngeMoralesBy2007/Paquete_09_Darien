from fastapi import FastAPI, HTTPException
import httpx
import os

app = FastAPI(title="Descubridor Service", version="1.0.0")

CONSUL_HOST = os.getenv("CONSUL_HOST", "consul")
CONSUL_PORT = os.getenv("CONSUL_PORT", "8500")
CONSUL_URL = f"http://{CONSUL_HOST}:{CONSUL_PORT}"

SERVICE_NAME = os.getenv("PISHOP_SERVICE_NAME", "descubridor-service")
SERVICE_PORT = int(os.getenv("PISHOP_HTTP_PORT", "8090"))
SERVICE_HOST = os.getenv("SERVICE_HOST", "descubridor-service")

@app.on_event("startup")
def registrar_en_consul():
    """Registra automáticamente este servicio en Consul al arrancar"""
    payload = {
        "ID": f"{SERVICE_NAME}-1",
        "Name": SERVICE_NAME,
        "Address": SERVICE_HOST,
        "Port": SERVICE_PORT
    }
    try:
        url = f"{CONSUL_URL}/v1/agent/service/register"
        response = httpx.put(url, json=payload)
        if response.status_code == 200:
            print(f"✅ Servicio {SERVICE_NAME} registrado exitosamente en Consul.")
        else:
            print(f"⚠️ Error al registrar en Consul: {response.text}")
    except Exception as e:
        print(f"❌ No se pudo conectar a Consul: {e}")

@app.get("/v1/servicios")
def listar_servicios():
    """Obtiene la lista completa de servicios registrados en Consul"""
    try:
        url = f"{CONSUL_URL}/v1/catalog/services"
        response = httpx.get(url)
        if response.status_code != 200:
            return {}
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.get("/v1/servicios/{nombre}/instancias")
def listar_instancias(nombre: str):
    """Consulta todas las instancias activas de un servicio registrado en Consul"""
    try:
        url = f"{CONSUL_URL}/v1/health/service/{nombre}?passing=true"
        response = httpx.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Servicio no encontrado en Consul")
        
        data = response.json()
        instancias = [
            {
                "id": item["Service"]["ID"],
                "nombre": item["Service"]["Service"],
                "direccion": item["Service"]["Address"],
                "puerto": item["Service"]["Port"]
            }
            for item in data
        ]
        return {"servicio": nombre, "instancias": instancias}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/servicios/{nombre}/resolver")
def resolver_servicio(nombre: str):
    """Resuelve y balancea una instancia activa para el servicio consultado"""
    try:
        url = f"{CONSUL_URL}/v1/health/service/{nombre}?passing=true"
        response = httpx.get(url)
        if response.status_code != 200 or not response.json():
            raise HTTPException(status_code=404, detail="No hay instancias disponibles para este servicio")
        
        instancia = response.json()[0]["Service"]
        return {
            "nombre": instancia["Service"],
            "direccion": instancia["Address"],
            "puerto": instancia["Port"],
            "url": f"http://{instancia['Address']}:{instancia['Port']}"
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health/live")
def health_live():
    """Verifica si el contenedor está vivo"""
    return {"status": "ok"}

@app.get("/health/ready")
def health_ready():
    """Verifica si el microservicio está listo para recibir tráfico"""
    return {"status": "ok"}

@app.get("/health/startup")
def health_startup():
    """Verifica si el servicio ha completado su arranque"""
    return {"status": "ok"}