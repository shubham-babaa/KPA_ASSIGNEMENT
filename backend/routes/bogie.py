from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.database import get_db
from backend.models.bogie import BogieChecksheet
from backend.schemas.bogie import BogieChecksheetCreate
import uuid
from datetime import date, datetime

router = APIRouter(    
    prefix="/bogie-checksheet",
    tags=["Bogie"],
)

# Dependency for getting DB session


# Utility function to convert all date/datetime to ISO strings in JSON-like objects
def convert_dates_to_strings(data):
    if isinstance(data, dict):
        return {k: convert_dates_to_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_dates_to_strings(item) for item in data]
    elif isinstance(data, (date, datetime)):
        return data.isoformat()
    else:
        return data

@router.post("/bogie-checksheet",status_code=status.HTTP_201_CREATED)
async def create_bogie_checksheet(data: BogieChecksheetCreate, db: Session = Depends(get_db)):
    try:
        # Check for duplicate form number
        existing = db.query(BogieChecksheet).filter_by(form_number=data.form_number).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Form with this number already exists."
            )

        # Safely encode all date/datetime inside JSON fields
        bogie_details = convert_dates_to_strings(data.bogie_details.dict())
        bogie_checksheet = convert_dates_to_strings(data.bogie_checksheet.dict())
        bmbc_checksheet = convert_dates_to_strings(data.bmbc_checksheet.dict())

        new_checksheet = BogieChecksheet(
            id=uuid.uuid4(),
            form_number=data.form_number,
            inspection_by=data.inspection_by,
            inspection_date=data.inspection_date,
            bogie_details=bogie_details,
            bogie_checksheet=bogie_checksheet,
            bmbc_checksheet=bmbc_checksheet
        )

        db.add(new_checksheet)
        db.commit()
        db.refresh(new_checksheet)

        return {
            "data": {
                "formNumber": data.form_number,
                "inspectionBy": data.inspection_by,
                "inspectionDate": data.inspection_date,
                "status": "Saved"
            },
            "message": "Bogie checksheet submitted successfully",
            "success": True
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Integrity error: possibly duplicate or bad data."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
        )
