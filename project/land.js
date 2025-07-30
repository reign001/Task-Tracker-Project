// function addTask(event) {
//   event.preventDefault();
//   const form = event.target;
//   const title = form.title.value;
//   const description = form.description.value;
//   const start = form.startDate.value;
//   const due = form.dueDate.value;
//   const assigned = form.assignedTo.value;
//   const status = form.status.value;

//   const tbody = document.getElementById("taskList");
//   const row = document.createElement("tr");

//   row.innerHTML = `
//       <td>${title}</td>
//       <td>${assigned}</td>
//       <td>${start}</td>
//       <td>${due}</td>
//       <td class="status">${status}</td>
//     `;

//   tbody.appendChild(row);
//   form.reset();
// }

// // Access control check
// const role = sessionStorage.getItem("role");

// if (!role) {
//   alert("Unauthorized access! Redirecting to login.");
//   window.location.href = "login.html";
// }






