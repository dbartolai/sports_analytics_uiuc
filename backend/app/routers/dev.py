from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.dev import Dev
from app.schemas.dev import DevCreate, DevOut, DevUpdate

router = APIRouter(prefix="/devs", tags=["devs"])

@router.post("/", response_model=DevOut)
def create_dev(payload: DevCreate, db: Session = Depends(get_db)):
    dev = Dev(**payload.dict())
    db.add(dev)
    db.commit()
    db.refresh(dev)
    return dev

@router.get("/", response_model=list[DevOut])
def list_devs(db: Session = Depends(get_db)):
    return db.query(Dev).all()

@router.get("/{dev_id}", response_model=DevOut)
def get_dev(dev_id: int, db: Session = Depends(get_db)):
    dev = db.get(Dev, dev_id)
    if not dev:
        raise HTTPException(status_code=404, detail="Dev not found")
    return dev

@router.patch("/{dev_id}", response_model=DevOut)
def edit_dev(dev_id: int, payload: DevUpdate, db: Session = Depends(get_db)):
    dev = db.get(Dev, dev_id)
    if not dev:
        raise HTTPException(status_code=404, detail="Dev not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(dev, key, value)

    db.commit()
    db.refresh(dev)
    return dev


@router.delete("/{dev_id}")
def delete_dev(dev_id: int, db: Session = Depends(get_db)):
    dev = db.get(Dev, dev_id)
    if not dev:
        raise HTTPException(status_code=404, detail="Dev not found")
    db.delete(dev)
    db.commit()
    return {"message": f"Deleted dev {dev_id}"}
