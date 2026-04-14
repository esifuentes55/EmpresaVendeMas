# Prueba Técnica Full-Stack — Caso C

Implementación del **Directorio de Proveedores Inteligente (CRUD)** con:
- **Frontend:** Vue 3 + Vite
- **Backend:** FastAPI
- **Base de datos:** PostgreSQL (vía SQLAlchemy)
- **IA:** OpenAI API para categorización automática de proveedores

---

## 1) Arquitectura

```text
[Vue App]
   |
   | HTTP (REST)
   v
[FastAPI]
   |--- CRUD de proveedores
   |--- búsqueda inteligente (texto + categoría IA)
   |--- categorización automática (OpenAI / fallback local)
   v
[PostgreSQL]
```

### Modelo de datos (relacional)
Se eligió un modelo **relacional** porque el dominio CRUD requiere:
- integridad de datos (email único),
- filtros por columnas (nombre, ciudad, categoría),
- actualización/transaccionalidad clara.

Tabla principal: `providers`
- `id` (PK)
- `name`
- `service_type`
- `description`
- `email` (único)
- `phone`
- `city`
- `ai_category`
- `created_at`
- `updated_at`

---

## 2) Backend (FastAPI)

### Instalación
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Variables de entorno
- `DATABASE_URL`: cadena de conexión PostgreSQL.
- `OPENAI_API_KEY`: clave para activar categorización con IA.
- `OPENAI_MODEL`: opcional (default `gpt-4o-mini`).

### Ejecución
```bash
uvicorn app.main:app --reload
```

### Endpoints
- `GET /health`
- `GET /providers?q=texto`
- `POST /providers`
- `PUT /providers/{id}`
- `DELETE /providers/{id}`

> Si no se configura `OPENAI_API_KEY`, la app usa una categorización de respaldo por keywords.

---

## 3) Frontend (Vue)

### Instalación y ejecución
```bash
cd frontend
npm install
npm run dev
```

### Configuración
Crear `.env` en `frontend/`:
```bash
VITE_API_URL=http://localhost:8000
```

Funcionalidades:
- Crear proveedor
- Listar proveedores
- Editar proveedor
- Eliminar proveedor
- Buscar por texto (nombre, servicio, descripción, ciudad o categoría IA)

---

## 4) Uso de IA

### Dentro de la app
Al crear/editar un proveedor, el backend:
1. toma la descripción,
2. llama al modelo de OpenAI,
3. guarda `ai_category` para mejorar descubrimiento/búsqueda.

### En el desarrollo
Se aplicó IA para acelerar:
- definición de estructura CRUD,
- diseño inicial del esquema de datos,
- redacción de documentación técnica.

---

## 5) DevOps / Despliegue sugerido

- Frontend: Vercel o Netlify.
- Backend: Railway / Render / Fly.io.
- DB: PostgreSQL administrado (Supabase, Railway PG, Neon).

Flujo recomendado:
1. Push a GitHub.
2. Deploy automático por rama `main`.
3. Variables de entorno en cada plataforma.

---

## 6) Entregables esperados

- URL del repositorio con este código.
- URL de la app en vivo (frontend + backend).
- Este README como documentación breve de arquitectura, local setup y uso de IA.
