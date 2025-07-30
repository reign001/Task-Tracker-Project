// // Add Employee
// async function addEmployee(event) {
//   event.preventDefault();
//   const form = document.getElementById('add-employee-form');
//   const formData = new FormData(form);
//   const employee = Object.fromEntries(formData.entries());

//   try {
//     const res = await fetch('/api/employees', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(employee)
//     });
//     if (!res.ok) throw new Error('Add failed');
//     alert('Employee added!');
//     form.reset();
//     fetchEmployees(); // refresh list
//   } catch (err) {
//     console.error(err);
//     alert('Failed to add employee');
//   }
// }

// // Fetch and Display Employees
// async function fetchEmployees() {
//   try {
//     const res = await fetch('/api/employees');
//     const employees = await res.json();
//     const tbody = document.getElementById('employee-list');
//     tbody.innerHTML = employees.map(emp => `
//         <tr>
//           <td>${emp.firstName} ${emp.surname}</td>
//           <td>${emp.email}</td>
//           <td>${emp.status}</td>
//           <td>₦${emp.salaryPerDay}</td>
//           <td>
//             <button onclick="deleteEmployee('${emp._id}')">Delete</button>
//           </td>
//         </tr>
//       `).join('');
//   } catch (err) {
//     console.error(err);
//   }
// }

// // Delete Employee
// async function deleteEmployee(id) {
//   if (!confirm("Delete this employee?")) return;
//   try {
//     const res = await fetch(`/api/employees/${id}`, {
//       method: 'DELETE'
//     });
//     if (!res.ok) throw new Error('Delete failed');
//     alert('Deleted!');
//     fetchEmployees();
//   } catch (err) {
//     console.error(err);
//     alert('Error deleting employee');
//   }
// }

// // Fetch employees on page load
// window.onload = fetchEmployees;





