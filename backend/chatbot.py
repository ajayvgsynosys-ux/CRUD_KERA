import re
from sqlalchemy.orm import Session
from sqlalchemy import func

from models import Employee

#this  function  is to retreive employees
def find_employee(db: Session, name_text: str):
    """Find an employee by first name or full name."""
    name_text = name_text.strip()

    # Exact full-name match first.
    employee = (
        db.query(Employee)
        .filter(func.lower(Employee.name) == name_text.lower())
        .first()
    )
    if employee:
        return employee

    # Then try first-name matching.
    first_name = name_text.split()[0]
    return (
        db.query(Employee)
        .filter(func.lower(Employee.name).like(f"{first_name.lower()}%"))
        .first()
    )


def employee_details(employee: Employee) -> str:
    return (
        f"{employee.name} is {employee.age} years old "
        f"and their email is {employee.email}."
    )


def process_message(message: str, db: Session) -> str:
    """Simple rule-based chatbot. No external LLM is used."""
    text = message.strip()
    lower = text.lower()

    if not text:
        return "Please type a question about the employees."

    # Count employees.
    if (
        ("how many" in lower and "employee" in lower)
        or lower in {"count employees", "employee count"}
    ):
        count = db.query(Employee).count()
        return f"There are {count} employees."

    # Show all employees.
    if (
        "show all" in lower
        or "list all" in lower
        or "all employees" in lower
        or lower in {"show employees", "list employees", "employees"}
    ):
        employees = db.query(Employee).order_by(Employee.id).all()
        if not employees:
            return "There are no employees in the database."

        details = [
            f"{employee.name} - Age {employee.age} - {employee.email}"
            for employee in employees
        ]
        return "Here are all employees:\n" + "\n".join(details)

    # Employees older than a given age.
    older_match = re.search(r"(?:older than|above|over)\s+(\d+)", lower)
    if older_match and "employee" in lower:
        age = int(older_match.group(1))
        employees = (
            db.query(Employee)
            .filter(Employee.age > age)
            .order_by(Employee.age)
            .all()
        )

        if not employees:
            return f"No employees are older than {age}."

        details = [
            f"{employee.name} - Age {employee.age} - {employee.email}"
            for employee in employees
        ]
        return f"Employees older than {age}:\n" + "\n".join(details)

    # Try to identify a named employee.
    employee = None
    for candidate in db.query(Employee).all():
        first_name = candidate.name.split()[0].lower()
        full_name = candidate.name.lower()

        if first_name in lower or full_name in lower:
            employee = candidate
            break

    if employee is None:
        return "Sorry, I couldn't find that employee."

    # Email question.
    if "email" in lower or "mail" in lower:
        return f"{employee.name}'s email is {employee.email}."

    # Age question.
    if "age" in lower or "old" in lower:
        return f"{employee.name} is {employee.age} years old."

    # General "who is" / employee information question.
    if "who is" in lower or "about" in lower or "details" in lower:
        return employee_details(employee)

    return employee_details(employee)
