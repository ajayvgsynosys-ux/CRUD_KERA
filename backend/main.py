from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from chatbot import process_message
from database import Base, SessionLocal, engine, get_db
from models import Employee
from schemas import ChatRequest, ChatResponse, EmployeeCreate, EmployeeResponse

app = FastAPI(title="Employee Chatbot API")

# Allow the React Vite development server to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SAMPLE_EMPLOYEES = [
    {
        "name": "Rahul Kumar",
        "age": 25,
        "email": "rahul@example.com",
    },
    {
        "name": "Anjali Nair",
        "age": 28,
        "email": "anjali@example.com",
    },
    {
        "name": "Arjun Menon",
        "age": 32,
        "email": "arjun@example.com",
    },
    {
        "name": "Sneha Thomas",
        "age": 26,
        "email": "sneha@example.com",
    },
    {
        "name": "Vivek Sharma",
        "age": 30,
        "email": "vivek@example.com",
    },
]


def initialize_database():
    """Create the table and seed sample data only when the table is empty."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Employee).count() == 0:
            db.add_all([Employee(**employee) for employee in SAMPLE_EMPLOYEES])
            db.commit()
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    initialize_database()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).order_by(Employee.id).all()

    
@app.post("/employees", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
):
    new_employee = Employee(
        name=employee.name,
        age=employee.age,
        email=employee.email,
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    response = process_message(request.message, db)
    return {"response": response}
