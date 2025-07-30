// const mongoose = require('mongoose');
// mongoose.connect('mongodb://localhost:27017/tasktracker');

// // Employee Schema
// const employeeSchema = new mongoose.Schema({
//     firstName: String,
//     surname: String,
//     otherNames: String,
//     email: String,
//     phone: String,
//     status: String,
//     salaryPerDay: Number
// });
// const Employee = mongoose.model('Employee', employeeSchema);

// // Add new employee
// app.post('/api/employees', async (req, res) => {
//     try {
//         const emp = new Employee(req.body);
//         await emp.save();
//         res.status(201).json(emp);
//     } catch (err) {
//         res.status(400).json({ error: err.message });
//     }
// });

// // Get all employees
// app.get('/api/employees', async (req, res) => {
//     const emps = await Employee.find();
//     res.json(emps);
// });

// // Delete employee
// app.delete('/api/employees/:id', async (req, res) => {
//     try {
//         await Employee.findByIdAndDelete(req.params.id);
//         res.json({ message: 'Deleted' });
//     } catch (err) {
//         res.status(400).json({ error: err.message });
//     }
// });


