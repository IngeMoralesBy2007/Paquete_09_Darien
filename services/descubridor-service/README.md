# 🔍 Paquete 09: Servicio de Registro y Descubrimiento (descubridor-service)

Microservicio perteneciente a la plataforma **PiShop Cloud**, encargado de gestionar el autorregistro de servicios en la red y resolver peticiones de descubrimiento dinámico mediante la integración con HashiCorp Consul.

---

## 🛠️ Tecnologías Utilizadas

* **Python / FastAPI:** Framework principal para los endpoints de descubrimiento y salud.
* **Pydantic-Settings:** Gestión centralizada de variables de entorno y configuración.
* **HTTPX:** Cliente HTTP asíncrono para la comunicación con la API del agente Consul.
* **HashiCorp Consul (v1.21):** Service Registry y Health Checking.
* **Docker / Docker Compose:** Entorno de contenerización y orquestación local.

---

## 🏗️ Arquitectura y Funcionamiento

1. **Autorregistro en Consul (`lifespan`):** Al levantar la aplicación FastAPI, el servicio registra automáticamente sus metadatos (nombre, IP, puerto y chequeo de salud) en el agente de Consul. Al apagarse de forma limpia (`graceful shutdown`), remueve su registro de Consul.
2. **Chequeo de Salud (`/health/live`):** Consul consulta periódicamente este endpoint para validar que el servicio siga operativo.
3. **Listado de Servicios (`/v1/servicios`):** Consulta a Consul los servicios activos y devuelve un arreglo JSON con las instancias disponibles.
4. **Resolución y Balanceo (`/v1/resolver/{service_name}`):** Devuelve la IP y puerto del servicio solicitado utilizando un algoritmo de selección balanceada (Round-Robin).

---

## ⚙️ Configuración de Variables de Entorno

El servicio utiliza las siguientes variables (definidas en `settings.py` con prefijo `PISHOP_` o leídas desde `.env`):

| Variable | Valor por defecto | Descripción |
| :--- | :--- | :--- |
| `PISHOP_APP_ENV` | `dev` | Entorno de ejecución. |
| `PISHOP_SERVICE_NAME` | `descubridor-service` | Nombre asignado al microservicio. |
| `PISHOP_HTTP_PORT` | `8090` | Puerto en el que escucha FastAPI. |
| `PISHOP_CONSUL_URL` | `http://consul:8500` | URL interna de red de Consul en Docker. |

---

## 🚀 Despliegue Local con Docker Compose

1. **Asegurar variables globales:** Verificar la presencia del archivo `.env` en la raíz del repositorio con las variables base (ej. `PISHOP_API_KEY`, `POSTGRES_PASSWORD`).
2. **Levantar los servicios:** Ejecutar desde la raíz del proyecto:
   ```cmd
   docker compose up -d --build consul descubridor-service