// async function login() {
//   const email = document.getElementById('email').value.trim();
//   const password = document.getElementById('password').value.trim();

//   if (!email || !password) {
//     alert('Please fill in all fields');
//     return;
//   }

//   try {
//     const res = await fetch('/api/login', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({ email, password })
//     });

//     const data = await res.json();

//     if (data.role) {
//       localStorage.setItem('userId', data.userId);
//       localStorage.setItem('role', data.role);
//       showDashboard(data.userId, data.role);
//     } else {
//       alert(data.error || 'Login failed');
//     }
//   } catch (err) {
//     console.error(err);
//     alert('Server error');
//   }
// }






// /*access control*/

// async function showDashboard(userId, role) {
//   document.getElementById('login-view').style.display = 'none';
//   document.getElementById('dashboard-view').style.display = 'block';
//   document.getElementById('role-header').innerText = `${role.toUpperCase()} Dashboard`;

//   const res = await fetch(`/api/tasks/${userId}/${role}`);
//   const tasks = await res.json();

//   const taskList = document.getElementById('task-list');
//   taskList.innerHTML = '';

//   tasks.forEach(task => {
//     const div = document.createElement('div');
//     div.className = 'task-item';
//     div.innerHTML = `<strong>${task.title}</strong><br>Status: ${task.status}<br>Due: ${task.dueDate || 'N/A'}`;
//     taskList.appendChild(div);
//   });
// }

// function logout() {
//   localStorage.clear();
//   document.getElementById('dashboard-view').style.display = 'none';
//   document.getElementById('login-view').style.display = 'block';
// }




// // login.js

// const allowedUsers = {
//   "admin001": "admin",
//   "emp101": "employee",
//   "emp102": "employee"
// };

// document.getElementById("loginForm").addEventListener("submit", function (e) {
//   e.preventDefault();
//   const userId = document.getElementById("userId").value.trim();
//   const role = allowedUsers[userId];

//   if (role) {
//     sessionStorage.setItem("userId", userId);
//     sessionStorage.setItem("role", role);

//     window.location.href = "landing.html";
//   } else {
//     document.getElementById("error").textContent = "Invalid ID or unauthorized access.";
//   }
// });

// localStorage.setItem("userRole", "admin"); // or "employee"
