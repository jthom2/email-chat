from pydantic import BaseModel

class CreateDraftSchema(BaseModel):
    to: str
    subject: str
    
draft = CreateDraftSchema(
    to="recipient@email.com",
    subject="Email subject" 
)

class GenerateInput(BaseModel):
    prompt: str