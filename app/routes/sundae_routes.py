from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import text

router = APIRouter()

# GET /sundaes: Return all available sundaes
@router.get("/sundaes")
def get_all_sundaes(db: Session = Depends(get_db)):
    """
    Fetch all available sundaes.
    """
    try:
        # Execute raw SQL query to fetch all sundaes
        result = db.execute(text("SELECT * FROM sundaes")).fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="No sundaes found")

        # Convert result to list of dictionaries
        sundaes = [dict(row._mapping) for row in result]
        
        return sundaes

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET /sundaes/{id}: Return details of a specific sundae with volume and revenue
@router.get("/sundaes/{id}")
def get_sundae_by_id(id: str, db: Session = Depends(get_db)):
    """
    Fetch details of a specific sundae, including volume and revenue.
    """
    try:
        # Query to get sundae details
        sundae_result = db.execute(
            text("SELECT * FROM sundaes WHERE id = :id"), {"id": id}
        ).fetchone()

        if not sundae_result:
            raise HTTPException(status_code=404, detail=f"Sundae with ID '{id}' not found")

        # Convert result to dictionary
        sundae = dict(sundae_result._mapping)

        # Query to calculate volume (number of sales) and revenue (total price)
        sales_result = db.execute(
            text(
                """
                SELECT COUNT(*) AS volume, SUM(price) AS revenue
                FROM sales
                WHERE sundae_id = :id
                """
            ),
            {"id": id},
        ).fetchone()

        # Extract sales data
        volume = sales_result.volume or 0
        revenue = float(sales_result.revenue) if sales_result.revenue else 0.0

        # Add volume and revenue to the sundae details
        sundae["volume"] = volume
        sundae["revenue"] = revenue

        return sundae

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
