# Descubridor Service (Paquete 09)

Microservicio de descubrimiento e instanciación de servicios desarrollado con **FastAPI** e integrado con **Consul** como registro y catálogo.

## 🚀 Características Implementadas
- **Endpoints de Descubrimiento:**
  - `GET /v1/servicios`: Lista todos los servicios registrados en Consul.
  - `GET /v1/servicios/{nombre}/instancias`: Consulta las instancias activas y saludables de un servicio específico.
  - `GET /v1/servicios/{nombre}/resolver`: Resuelve y balancea una instancia activa para el consumo del servicio.
- **Sondas de Ciclo de Vida (Health Checks):**
  - `/health/live`
  - `/health/ready`
  - `/health/startup`

## 🛠️ Configuración y Ejecución Local

1. Instalar dependencias:bash
pip install fastapi uvicorn pydantic httpx pydantic-settings
2. Configurar la variable de entorno para conectar con Consul:
* En Windows (PowerShell):powershell
$env:CONSUL_HOST="127.0.0.1"
3. Ejecutar las validaciones locales:bash
python herramientas/validar_entrega.py descubridor-service
**Evidencia**
1.Comando docker compose: 
C:\Users\Usuario\Documents\fundamentos_arquitectura_politecnico-main>docker compose up -d --build descubridor-service
[+] Building 1.4s (13/13) FINISHED
 => [internal] load local bake definitions                                                                         0.0s
 => => reading from stdin 779B                                                                                     0.0s
 => [internal] load build definition from Dockerfile                                                               0.0s
 => => transferring dockerfile: 246B                                                                               0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                0.8s
 => [auth] library/python:pull token for registry-1.docker.io                                                      0.0s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [1/5] FROM docker.io/library/python:3.11-slim@sha256:65bd3d9f1d7fa268dd1909973ba7eb4bdf41f6dcf2cfbe76ba9528b1  0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:65bd3d9f1d7fa268dd1909973ba7eb4bdf41f6dcf2cfbe76ba9528b1  0.0s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 3.52kB                                                                                0.0s
 => CACHED [2/5] WORKDIR /app                                                                                      0.0s
 => CACHED [3/5] COPY requirements.txt .                                                                           0.0s
 => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt                                                0.0s
 => [5/5] COPY . .                                                                                                 0.0s
 => exporting to image                                                                                             0.2s
 => => exporting layers                                                                                            0.1s
 => => exporting manifest sha256:98c99e0c87f199e889c4d97b4e4a635435cde44657de2ace15475001eea96c54                  0.0s
 => => exporting config sha256:963f06a1da3f16814a6242e96f00bac4f845fc366c372e32228f4e213e4b4e3c                    0.0s
 => => exporting attestation manifest sha256:55c17016f4057d536e55043c8281bcdd811446b74c1e5fa4d56077ccbbe9fd56      0.0s
 => => exporting manifest list sha256:e7e5f798794c3d55dac27df9b6f7c6d91c89e9118b2d34af3cb8ba590c24d46f             0.0s
 => => naming to docker.io/library/fundamentos_arquitectura_politecnico-main-descubridor-service:latest            0.0s
 => => unpacking to docker.io/library/fundamentos_arquitectura_politecnico-main-descubridor-service:latest         0.0s
 => resolving provenance for metadata file                                                                         0.0s
[+] up 4/4
 ✔ Image fundamentos_arquitectura_politecnico-main-descubridor-service       Built                                  1.7s
 ✔ Container fundamentos_arquitectura_politecnico-main-redis-1               Healthy                                1.3s
 ✔ Container fundamentos_arquitectura_politecnico-main-consul-1              Healthy                                1.3s
 ✔ Container fundamentos_arquitectura_politecnico-main-descubridor-service-1 Started                                1.6s
---------------------------------------------
2.Endpoint servicios:C:\Users\Usuario>curl http://localhost:8090/v1/servicios
["descubridor-service"]
---------------------------------------------
3.Resolvedor o Balanceador:C:\Users\Usuario>curl http://localhost:8090/v1/resolver/descubridor-service
{"id":"descubridor-service-1","address":"descubridor-service","port":8090}
---------------------------------------------
4.contenedores de docker activos:CONTAINER ID   IMAGE                                                           COMMAND                  CREATED          STATUS                    PORTS                                         NAMES
01215e2948b3   fundamentos_arquitectura_politecnico-main-descubridor-service   "uvicorn app.main:ap…"   10 minutes ago   Up 10 minutes             0.0.0.0:8090->8090/tcp, [::]:8090->8090/tcp   fundamentos_arquitectura_politecnico-main-descubridor-service-1
74f0253a47e2   redis:8-alpine                                                  "docker-entrypoint.s…"   22 minutes ago   Up 22 minutes (healthy)   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp   fundamentos_arquitectura_politecnico-main-redis-1
622f4cbbf908   hashicorp/consul:1.21                                           "docker-entrypoint.s…"   22 minutes ago   Up 22 minutes (healthy)   0.0.0.0:8500->8500/tcp, [::]:8500->8500/tcp   fundamentos_arquitectura_politecnico-main-consul-1
---------------------------------------------
5.Pyton test:PS C:\Users\Usuario\Documents\fundamentos_arquitectura_politecnico-main> python herramientas/validar_entrega.py descubridor-service
C:\Users\Usuario\AppData\Local\Programs\Python\Python313\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
  from starlette.testclient import TestClient as TestClient  # noqa

== descubridor-service (rol P09, puerto 8090) ==
  [ok] GET    /v1/servicios
  [ok] GET    /v1/servicios/{nombre}/instancias
  [ok] GET    /v1/servicios/{nombre}/resolver
  [ok] sonda /health/live -> 200
  [ok] sonda /health/ready -> 200
  [ok] sonda /health/startup -> 200
  [ok] sin configuración embebida (0 hallazgos)

Resumen: {'descubridor-service': 'OK'}
