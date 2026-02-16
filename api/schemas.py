from pydantic import BaseModel, Field

class CreditApplication(BaseModel):
    Age: int = Field(..., description="Age of the applicant", example=30)
    Sex: str = Field(..., description="Sex of the applicant (male/female)", example="male")
    Job: int = Field(..., description="Job level (0-3)", example=2)
    Housing: str = Field(..., description="Housing status (own/rent/free)", example="own")
    Saving_accounts: str = Field(..., description="Saving accounts status (little/moderate/rich/quite rich)", example="little")
    Checking_account: str = Field(..., description="Checking account status (little/moderate/rich)", example="moderate")
    Credit_amount: int = Field(..., description="Credit amount", example=5000)
    Duration: int = Field(..., description="Duration of the credit in months", example=24)
    Purpose: str = Field(..., description="Purpose of the credit (car/furniture/education/etc)", example="car")
