from pydantic import BaseModel
class EmployeeCreate(BaseModel):
    name: str
    age: int
    email: str


class EmployeeResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
