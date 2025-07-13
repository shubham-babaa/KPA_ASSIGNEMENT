from sqlalchemy import Column, String, Date, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from backend.database import Base

class WheelSpecification(Base):
    __tablename__ = "wheel_specifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form_number = Column(String, nullable=False, index=True)
    submitted_by = Column(String, nullable=False)
    submitted_date = Column(Date, nullable=False)
    fields = Column(JSON, nullable=False)