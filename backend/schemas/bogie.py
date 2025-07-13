# backend/schemas/bogie.py
from pydantic import BaseModel, Field
from typing import Literal
from datetime import date

class BogieDetails(BaseModel):
    bogieNo: str = Field(..., min_length=3)
    dateOfIOH: date
    deficitComponents: str
    incomingDivAndDate: str
    makerYearBuilt: str

class BogieChecksheetFields(BaseModel):
    axleGuide: Literal["Worn", "Good", "Cracked"]
    bogieFrameCondition: str
    bolster: str
    bolsterSuspensionBracket: str
    lowerSpringSeat: str

class BMBCChecksheetFields(BaseModel):
    adjustingTube: Literal["GOOD", "DAMAGED"]
    cylinderBody: str
    pistonTrunnion: str
    plungerSpring: str

class BogieChecksheetCreate(BaseModel):
    form_number: str = Field(..., min_length=5)
    inspection_by: str
    inspection_date: date
    bogie_details: BogieDetails
    bogie_checksheet: BogieChecksheetFields
    bmbc_checksheet: BMBCChecksheetFields
