from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Sundae, Sale

router = APIRouter(prefix="/sundaes", tags=["Sundaes"])

@router.get("/")
def get_sundaes(db: Session = Depends(get_db)):
    """Fetch all sundaes from the database."""
    sundaes = db.query(Sundae).all()
    return [{"id": s.id, "name": s.name, "description": s.description} for s in sundaes]

@router.get("/{id}")
def get_sundae_details(id: str, db: Session = Depends(get_db)):
    """Fetch a specific sundae along with its sales volume."""
    sundae = db.query(Sundae).filter(Sundae.id == id).first()
    if not sundae:
        raise HTTPException(status_code=404, detail="Sundae not found")

    # Aggregate sales data
    sales = db.query(Sale).filter(Sale.sundae_id == id).all()
    volume = sum(sale.quantity for sale in sales)

    return {
        "id": sundae.id,
        "name": sundae.name,
        "description": sundae.description,
        "volume": volume
    }
