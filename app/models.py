from app import db
from app.extensions import db
from datetime import datetime
from flask_login import UserMixin


from werkzeug.security import generate_password_hash, check_password_hash

class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    other_names = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(300), nullable=False)
    must_reset_password = db.Column(db.Boolean, default=True)
    salary_per_day = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='full-time')
    office = db.Column(db.String(50), default='instrumentalist')
    role = db.Column(db.String(20), default='employee')  # or 'admin', 'task_admin'

    # ✅ Task relationships using explicit foreign_keys
    tasks_assigned = db.relationship(
        'Task',
        foreign_keys='Task.assigned_to',
        backref='assigned_user'
    )

    tasks_created = db.relationship(
        'Task',
        foreign_keys='Task.created_by',
        backref='creator'
    )

    tasks = db.relationship(  # renamed from ambiguous 'tasks' to 'tasks'
        'Task',
        foreign_keys='Task.employee_id',
        backref='employee_link',  # avoid naming clash with model name
        lazy=True
    )

    def full_name(self):
        return f"{self.first_name} {self.other_names or ''} {self.surname}".strip()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)




class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('employee.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('employee.id'))

    start_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    cycle_id = db.Column(db.Integer, db.ForeignKey('working_cycle.id'))
    cycle = db.relationship('WorkingCycle', backref='tasks')



from datetime import datetime

class WorkingCycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, start_date, end_date, is_active=True):
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.name = start_date.strftime('%B %Y')  # e.g., July 2025

    def __repr__(self):
        return f"<WorkingCycle {self.name}>"


# models.py
class SalaryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    cycle_id = db.Column(db.Integer, db.ForeignKey('working_cycle.id'), nullable=False)
    completed_tasks = db.Column(db.Integer, nullable=False)
    undone_tasks = db.Column(db.Integer, nullable=False)
    monthly_allowance = db.Column(db.Float, nullable=False)
    deduction = db.Column(db.Float, nullable=False)
    net_salary = db.Column(db.Float, nullable=False)
    computed_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref='salary_logs')
    cycle = db.relationship('WorkingCycle', backref='salary_logs')

