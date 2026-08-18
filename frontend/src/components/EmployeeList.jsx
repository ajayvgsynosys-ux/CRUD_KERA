function EmployeeList({ employees, loading, error }) {
  return (
    <section className="card employee-card">
      <div className="card-header">
        <h2>Employee List</h2>
        <p>Employees stored in SQLite</p>
      </div>

      {loading && <p className="muted">Loading employees...</p>}

      {error && <p className="error-text">{error}</p>}

      {!loading && !error && (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Age</th>
                <th>Email</th>
              </tr>
            </thead>

            <tbody>
              {employees.map((employee) => (
                <tr key={employee.id}>
                  <td>{employee.name}</td>
                  <td>{employee.age}</td>
                  <td>
                    <a href={`mailto:${employee.email}`}>
                      {employee.email}
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

export default EmployeeList;
