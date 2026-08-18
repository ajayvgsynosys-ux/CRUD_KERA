import { useEffect, useState } from "react";
import EmployeeList from "./components/EmployeeList";
import Chatbot from "./components/Chatbot";
import AddEmployee from "./components/AddEmployee";

const API_URL = "http://localhost:8000";

function App() {
  const [employees, setEmployees] = useState([]);
  const [employeesLoading, setEmployeesLoading] = useState(true);
  const [employeesError, setEmployeesError] = useState("");
    function handleEmployeeAdded(newEmployee) {
    setEmployees((currentEmployees) => [
      ...currentEmployees,
      newEmployee,
    ]);
  }

  useEffect(() => {
    async function loadEmployees() {
      try {
        const response = await fetch(`${API_URL}/employees`);

        if (!response.ok) {
          throw new Error("Failed to load employees");
        }

        const data = await response.json();
        setEmployees(data);
      } catch (error) {
        setEmployeesError("Unable to connect to the server.");
      } finally {
        setEmployeesLoading(false);
      }
    }

    loadEmployees();
  }, []);

  return (
    <div className="page">
      <header className="header">
        
        <p>Ask me about our employees</p>
      </header>

      <main className="main-container">
        <EmployeeList
          employees={employees}
          loading={employeesLoading}
          error={employeesError}
        />
        <AddEmployee
           apiUrl={API_URL}
           onEmployeeAdded={handleEmployeeAdded}
        />
        <Chatbot apiUrl={API_URL} />
      </main>
    </div>
  );
}

export default App;
