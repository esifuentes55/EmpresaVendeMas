from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from .ai import categorize_provider
from .database import Base, engine, get_db
from .models import Provider
from .schemas import ProviderCreate, ProviderOut, ProviderUpdate

app = FastAPI(title="Directorio de Proveedores Inteligente", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/providers", response_model=list[ProviderOut])
def list_providers(
    q: str | None = Query(default=None, description="Texto para búsqueda inteligente"),
    db: Session = Depends(get_db),
) -> list[Provider]:
    stmt = select(Provider)
    if q:
        pattern = f"%{q.strip()}%"
        stmt = stmt.where(
            or_(
                Provider.name.ilike(pattern),
                Provider.service_type.ilike(pattern),
                Provider.description.ilike(pattern),
                Provider.city.ilike(pattern),
                Provider.ai_category.ilike(pattern),
            )
        )

    return list(db.execute(stmt.order_by(Provider.id.desc())).scalars().all())


@app.post("/providers", response_model=ProviderOut, status_code=201)
def create_provider(payload: ProviderCreate, db: Session = Depends(get_db)) -> Provider:
    exists = db.execute(select(Provider).where(Provider.email == payload.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Ya existe un proveedor con ese email")

    provider = Provider(**payload.model_dump())
    provider.ai_category = categorize_provider(payload.description)
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


@app.put("/providers/{provider_id}", response_model=ProviderOut)
def update_provider(
    provider_id: int,
    payload: ProviderUpdate,
    db: Session = Depends(get_db),
) -> Provider:
    provider = db.get(Provider, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(provider, key, value)

    if "description" in update_data:
        provider.ai_category = categorize_provider(provider.description)

    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


@app.delete("/providers/{provider_id}", status_code=204)
def delete_provider(provider_id: int, db: Session = Depends(get_db)) -> None:
    provider = db.get(Provider, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    db.delete(provider)
    db.commit()
