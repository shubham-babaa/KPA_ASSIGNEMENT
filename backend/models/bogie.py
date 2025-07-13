# backend/models/bogie_checksheet.py

from sqlalchemy import Column, String, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from backend.database import Base
import uuid


class BogieChecksheet(Base):
    __tablename__ = "bogie_checksheets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    form_number = Column(String, nullable=False)
    inspection_by = Column(String, nullable=False)
    inspection_date = Column(Date, nullable=False)
    bogie_details = Column(JSONB, nullable=False)
    bogie_checksheet = Column(JSONB, nullable=False)
    bmbc_checksheet = Column(JSONB, nullable=False)
