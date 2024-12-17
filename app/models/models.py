from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Sundae(Base):
    """Model representing sundae menu items."""
    __tablename__ = "sundaes"

    id = Column(String, primary_key=True, index=True)  # Unique ID for sundaes
    name = Column(String, nullable=False)  # Name of the sundae
    description = Column(String, nullable=False)  # Description of the sundae

    # Relationship to the 'sales' table
    sales = relationship("Sale", back_populates="sundae", cascade="all, delete-orphan")


class Sale(Base):
    """Model representing sales transactions."""
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # Auto-incremented ID
    sundae_id = Column(String, ForeignKey("sundaes.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(Float, nullable=False)  # Unix timestamp of the sale
    quantity = Column(Integer, default=1)  # Quantity sold in this sale

    # Relationship back to the 'sundaes' table
    sundae = relationship("Sundae", back_populates="sales")
