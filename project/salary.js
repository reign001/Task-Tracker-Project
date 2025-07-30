// document.addEventListener("DOMContentLoaded", () => {
//   const tableBody = document.getElementById("salaryTable");

//   fetch("http://localhost:3000/api/salary")
//     .then(res => res.json())
//     .then(data => {
//       data.forEach(entry => {
//         const totalDeduction = entry.missed * entry.deductionPerTask;
//         const netSalary = entry.grossSalary - totalDeduction;

//         const row = document.createElement("tr");
//         row.innerHTML = `
//             <td>${entry.id}</td>
//             <td>${entry.employeeId}</td>
//             <td>${entry.totalTasks}</td>
//             <td>${entry.completed}</td>
//             <td>${entry.missed}</td>
//             <td>₦${entry.deductionPerTask}</td>
//             <td>₦${entry.grossSalary}</td>
//             <td>₦${totalDeduction}</td>
//             <td><strong>₦${netSalary}</strong></td>
//           `;
//         tableBody.appendChild(row);
//       });
//     })
//     .catch(err => {
//       console.error("Error loading salary data:", err);
//     });
// });



// //access restriction//


// const role = sessionStorage.getItem("role");

