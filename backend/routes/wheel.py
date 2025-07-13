from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from backend.database import get_db
from backend.models.wheel import WheelSpecification
from backend.schemas.wheel import WheelChecksheetCreate, WheelChecksheetOut
from typing import List, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="",
    tags=["Wheel"]
    
)




def validate_iso_date(submittedDate: str) -> datetime.date:
    """
    Validates that the input string is in ISO 8601 (YYYY-MM-DD) format.

    Args:
        submittedDate (str): The date string to validate.

    Returns:
        datetime.date: Parsed date object.

    Raises:
        HTTPException: If the format is invalid.
    """
    try:
        return datetime.strptime(submittedDate, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid date format",
                "message": "Date must be in ISO 8601 format (YYYY-MM-DD)",
                "example": "2023-05-15",
                "received_value": submittedDate
            }
        )




@router.post("/wheel-specifications", status_code=status.HTTP_201_CREATED)
def create_wheel_spec(data: WheelChecksheetCreate, db: Session = Depends(get_db)):
    # 1. Duplicate form number check
    try:
        existing = db.query(WheelSpecification).filter_by(form_number=data.formNumber).first()
    except SQLAlchemyError as e:
        logger.error(f"Database query error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error"
        )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Form with this number already exists."
        )

    # 2. Create and save new entry
    try:
        new_entry = WheelSpecification(
            id=str(uuid.uuid4()),
            form_number=data.formNumber,
            submitted_by=data.submittedBy,
            submitted_date=data.submittedDate,
            fields=data.fields.dict() if data.fields else None
        )
        db.add(new_entry)
        db.commit()
        
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Data integrity violation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data violates database constraints"
        )
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database operation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
        
    except Exception as e:
        db.rollback()
        logger.critical(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    # 3. Success response
    return {
        "data": {
            "formNumber": new_entry.form_number,
            "submittedBy": new_entry.submitted_by,
            "submittedDate": new_entry.submitted_date,
            "status": "Saved"
        },
        "message": "Wheel specification submitted successfully.",
        "success": True
    }


@router.get("/wheel-specifications", response_model=dict)
def get_wheel_specs(
    formNumber: Optional[str] = Query(None, description="Filter by form number"),
    submittedBy: Optional[str] = Query(None, description="Filter by submitter name"),
    submittedDate: Optional[str] = Query(None, description="Filter by submission date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    try:
        # Validate and parse date if provided
        parsed_date = None
       # Updated date validation section
        if submittedDate:
           parsed_date = validate_iso_date(submittedDate)

        # Build query with filters
        query = db.query(WheelSpecification)
        if formNumber:
           query = query.filter(WheelSpecification.form_number == formNumber.strip())

        if submittedBy:
            query = query.filter(WheelSpecification.submitted_by == submittedBy.strip())
        if parsed_date:
            query = query.filter(WheelSpecification.submitted_date == parsed_date)

        # Execute query
        results = query.order_by(WheelSpecification.submitted_date.desc()).all()
        # Format response
        return {
            "data": [
                {
                    "formNumber": row.form_number,
                    "submittedBy": row.submitted_by,
                    "submittedDate": row.submitted_date.isoformat(),
                    "fields": row.fields
                } for row in results
            ],
            "message": "Wheel specifications fetched successfully.",
            "success": True,
            "count": len(results)
        }

    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
        
    except HTTPException:
        # Re-raise already handled HTTP exceptions
        raise
        
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
