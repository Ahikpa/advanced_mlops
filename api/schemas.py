from pydantic import BaseModel, Field

class CreditApplication(BaseModel):
    Age: int = Field(..., description="Age of the applicant")
    Sex: str = Field(..., description="Sex of the applicant (male/female)")
    Job: int = Field(..., description="Job level (0-3)")
    Housing: str = Field(..., description="Housing status (own/rent/free)")
    Saving_accounts: str = Field(..., description="Saving accounts status (little/moderate/rich/quite rich)")
    Checking_account: str = Field(..., description="Checking account status (little/moderate/rich)")
    Credit_amount: int = Field(..., description="Credit amount")
    Duration: int = Field(..., description="Duration of the credit in months")
    Purpose: str = Field(..., description="Purpose of the credit (car/furniture/education/etc)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Age": 30,
                    "Sex": "male",
                    "Job": 2,
                    "Housing": "own",
                    "Saving_accounts": "little",
                    "Checking_account": "moderate",
                    "Credit_amount": 5000,
                    "Duration": 24,
                    "Purpose": "car"
                }
            ]
        }
    }
