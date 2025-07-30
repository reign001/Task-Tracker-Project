// const cycles = [];

// function addCycle(event) {
//   event.preventDefault();
//   const id = document.getElementById("workerId").value.trim();
//   const name = document.getElementById("workerName").value.trim();
//   const start = document.getElementById("startDate").value;
//   const end = document.getElementById("endDate").value;
//   const status = document.getElementById("status").value;

//   if (!id || !name || !start || !end || !status) return;

//   const cycle = { id, name, start, end, status };
//   cycles.push(cycle);
//   document.getElementById("cycle-form").reset();
//   renderCycles();
// }

// function renderCycles() {
//   const filter = document.getElementById("filterStatus").value;
//   const tbody = document.getElementById("cycleBody");
//   tbody.innerHTML = "";

//   cycles
//     .filter(c => filter === "All" || c.status === filter)
//     .forEach((cycle, index) => {
//       const row = document.createElement("tr");
//       row.innerHTML = `
//         <td>${cycle.id}</td>
//         <td>${cycle.name}</td>
//         <td>${cycle.start}</td>
//         <td>${cycle.end}</td>
//         <td>${cycle.status}</td>
//         <td class="actions"><button onclick="deleteCycle(${index})">Delete</button></td>
//       `;
//       tbody.appendChild(row);
//     });
// }

// function deleteCycle(index) {
//   cycles.splice(index, 1);
//   renderCycles();
// }

// function filterCycles() {
//   renderCycles();
// }



// //access restriction//


//   // const role = sessionStorage.getItem("role");

//   // // Redirect if not logged in
//   // if (!role) {
//   //   alert("You must log in first.");
//   //   window.location.href = "login.html";
//   // }

//   // // Restrict access: Employees can only access task.html
//   // const currentPage = window.location.pathname.split("/").pop();

//   // if (role === "employee" && currentPage !== "task.html") {
//   //   alert("Access Denied: You can only access the Task page.");
//   //   window.location.href = "task.html";
//   // }

//   // // Admin has full access – no redirect
