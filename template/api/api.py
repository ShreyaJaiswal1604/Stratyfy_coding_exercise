from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .schema import SundaeBase, SundaeWithMetrics
from sqlalchemy import text

app = FastAPI()

# GET /sundaes - Return all sundaes
@app.get("/sundaes", response_model=list[SundaeBase])
def get_all_sundaes(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM sundaes")).fetchall()
        if not result:
            raise HTTPException(status_code=404, detail="No sundaes found")
        return [dict(row._mapping) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET /sundaes/{id} - Return sundae details with metrics
@app.get("/sundaes/{id}", response_model=SundaeWithMetrics)
def get_sundae_by_id(id: str, db: Session = Depends(get_db)):
    try:
        # Get sundae details
        sundae = db.execute(
            text("SELECT * FROM sundaes WHERE id = :id"), {"id": id}
        ).fetchone()
        if not sundae:
            raise HTTPException(status_code=404, detail="Sundae not found")
        
        # Calculate metrics: volume and revenue
        sales = db.execute(
            text("""
                SELECT COUNT(*) AS volume, SUM(price) AS revenue
                FROM sales
                WHERE sundae_id = :id
            """), {"id": id}
        ).fetchone()

        sundae_data = dict(sundae._mapping)
        sundae_data["volume"] = sales.volume or 0
        sundae_data["revenue"] = round(float(sales.revenue or 0),2)

        return sundae_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
