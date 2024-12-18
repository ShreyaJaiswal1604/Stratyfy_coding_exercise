import uuid
from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class Sundae(Base):
    __tablename__ = "sundaes"

    id = Column(String, primary_key=True, index=True)  # String-based ID (e.g., "banana-split")
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)





class Sale(Base):
    __tablename__ = "sales"

    sale_id_pk = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    sundae_id = Column(String, ForeignKey("sundaes.id"), nullable=False)  # Foreign key to sundaes
    timestamp = Column(Float, nullable=False)  # Unix timestamp as float
    price = Column(Float, nullable=False)  # Price of the sale
