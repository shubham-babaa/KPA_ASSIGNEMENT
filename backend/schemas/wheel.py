from pydantic import BaseModel
from datetime import date
from typing import Dict

class WheelFields(BaseModel):
    axleBoxHousingBoreDia: str
    bearingSeatDiameter: str
    condemningDia: str
    intermediateWWP: str
    lastShopIssueSize: str
    rollerBearingBoreDia: str
    rollerBearingOuterDia: str
    rollerBearingWidth: str
    treadDiameterNew: str
    variationSameAxle: str
    variationSameBogie: str
    variationSameCoach: str
    wheelDiscWidth: str
    wheelGauge: str
    wheelProfile: str

class WheelChecksheetCreate(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: date
    fields: WheelFields

class WheelChecksheetOut(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: date
    fields: dict
