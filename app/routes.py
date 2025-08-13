from flask import Blueprint, render_template, request, redirect, flash, url_for, session 
from datetime import date
from app.models import Employee, Task, WorkingCycle, SalaryLog
from app.extensions import db
from app.extensions import mail
from flask_mail import Message
from app.extensions import mail
from datetime import datetime
from flask import session, redirect, url_for, render_template, flash
from flask import send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from functools import wraps
from flask_login import current_user, login_required, login_user
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash







# MODELS IMPORT
from app.models import Employee, Task, WorkingCycle, SalaryLog


from flask import Blueprint, render_template

main = Blueprint('main', __name__)

admin = ("admin", "superadmin")


def task_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['admin', 'task_admin']:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'admin':
            flash("Access denied. Admins only.", "danger")
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'superadmin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.login_view'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
@login_required
def home():
    print('Current user:', current_user)
    return render_template('home.html')


@main.route('/login', methods=['GET', 'POST'])
def login_view():
    is_admin = session.get('role') == 'admin'
    print("Accessed login route")

    if request.method == 'POST':
        print("Login form submitted")

        email = request.form['email'].lower().strip()
        password = request.form['password'].strip()

        print(f"Email entered: '{email}'")
        print(f"Raw password input: '{password}'")

        user = Employee.query.filter_by(email=email).first()
        if user:
            print(f"User found: {user.email}")
            print(f"Checking password for: {email}")
            print("Stored hash:", user.password_hash)

            match = check_password_hash(user.password_hash, password)
            print("Password match:", match)

            if match:
                login_user(user)

                # Store session values
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['user_role'] = user.role


                # Redirect based on role
                if user.role in ['admin', 'superadmin']:
                    return redirect(url_for('main.home'))
                else:
                    return redirect(url_for('main.employee_dashboard'))
            else:
                print("Password mismatch")
        else:
            print("User not found")

        flash('Invalid credentials', 'danger')

    return render_template('auth/login.html', is_admin=is_admin)


@main.route('/logout')
def logout():
    session.clear()
    # flash("You have been logged out.", "info")
    return redirect(url_for('main.login_view'))

# ---------------- EMPLOYEE ----------------

@main.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    import secrets
    from werkzeug.security import generate_password_hash

    if request.method == 'POST':
        first_name = request.form['first_name']
        surname = request.form['surname']
        other_names = request.form.get('other_names')
        email = request.form['email']
        phone = request.form.get('phone')
        salary_per_day = float(request.form.get('salary_per_day', 0))
        status = request.form.get('status')
        office = request.form.get('office')
        role = request.form.get('role')

        # Check if email already exists
        if Employee.query.filter_by(email=email).first():
            flash("Email already exists. Try another.", "danger")
            return redirect(url_for('main.add_employee'))

        # 🔐 Generate password
        raw_password = secrets.token_urlsafe(10)
        hashed_password = generate_password_hash(raw_password)

        # ✅ Create new employee with login info
        new_emp = Employee(
            first_name=first_name,
            surname=surname,
            other_names=other_names,
            email=email,
            phone=phone,
            salary_per_day=salary_per_day,
            status=status,
            office=office,
            role=role,
            password_hash=hashed_password,
            must_reset_password=True
        )

        db.session.add(new_emp)
        db.session.commit()

        # ✉️ Send email with credentials
        try:
            subject = "Your Account Login - Dunamis TV Management"
            body = f"""
Dear {first_name},

Welcome to the Dunamis International Gospel Centre!

🎉 Your account has been created with the following credentials:

📧 Email: {email}
🔐 Password: {raw_password}

Congratulation!.

Blessings,  
DUNAMIS TV Management
"""
            msg = Message(subject, recipients=[email], body=body)
            mail.send(msg)
            print("✔ Login credentials emailed.")
        except Exception as e:
            print("❌ Email failed:", str(e))
            flash(f"Employee added, but email failed: {str(e)}", "warning")
        else:
            flash("Employee added and login credentials emailed successfully.", "success")

        return redirect(url_for('main.add_employee'))

    employees = Employee.query.order_by(Employee.id.desc()).all()
    is_admin = session.get('role') == 'admin'
    print("🛠 Rendering add_employee.html")
    return render_template('add_employee.html', is_admin=is_admin, employees=employees)


@main.route('/employees')
def view_employees():
    employees = Employee.query.all()
    is_admin = session.get('role') == ['admin', 'superadmin']
    print("employee successfully added")
    return render_template('view_employees.html', is_admin=is_admin, employees=employees)


@main.route('/employee/<int:id>/update', methods=['GET', 'POST'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.first_name = request.form['first_name']
        employee.surname = request.form['surname']
        employee.other_names = request.form['other_names']
        employee.email = request.form['email']
        employee.phone = request.form['phone']
        employee.salary_per_day = float(request.form['salary_per_day'])
        employee.status = request.form['status']

        db.session.commit()
        flash("Employee updated successfully.")
        return redirect(url_for('main.update_employee', id=employee.id))

    return render_template('update_employee.html', employee=employee)

@main.route('/employee/delete/<int:emp_id>')
def delete_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    db.session.delete(emp)
    db.session.commit()
    flash("Employee deleted successfully.", "success")
    return redirect(url_for('main.add_employee'))

# ---------------- TASK ----------------
@task_admin_required
@main.route('/task/add', methods=['GET', 'POST'])
def add_task():
    active_cycle = WorkingCycle.query.filter_by(is_active=True).first()
    if not active_cycle:
        flash("No active working cycle found. Please add one.", "danger")
        return redirect(url_for('main.add_cycle'))

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        description = request.form['description']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()

        employee = Employee.query.get_or_404(employee_id)

        task = Task(
            employee_id=employee.id,
            description=description,
            start_date=start_date,
            due_date=due_date,
            completed=False,  # Always false on creation
            completed_at=None,
            cycle_id=active_cycle.id
        )
        db.session.add(task)
        db.session.commit()

        # Email notification
        try:
            subject = f"Dunamis! New Task for {active_cycle.name}"
            body = f"""
Dear {employee.first_name},

A new task has been assigned to you under the cycle **{active_cycle.name}**:

📌 Description: {description}  
📅 Start Date: {start_date.strftime('%Y-%m-%d')}  
📅 Due Date: {due_date.strftime('%Y-%m-%d')}  

Please complete the task before the deadline.

Blessings,  
DUNAMIS TV Management
"""
            msg = Message(subject, recipients=[employee.email], body=body)
            mail.send(msg)
            print("✔ Task email sent.")
        except Exception as e:
            print("❌ Task email failed:", str(e))
            flash(f"Task saved, but email failed: {str(e)}", "warning")
        else:
            flash("Task assigned and emailed successfully.", "success")

        return redirect(url_for('main.add_task'))

    employees = Employee.query.order_by(Employee.first_name).all()
    tasks = Task.query.filter_by(cycle_id=active_cycle.id).order_by(Task.due_date.desc()).all()
    return render_template('add_task.html', employees=employees, tasks=tasks, cycle=active_cycle)



@main.route('/task/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    employee = task.employee

    try:
        db.session.delete(task)
        db.session.commit()

        # Email to inform the employee
        subject = "Dunamis! Task Cancelled"
        body = f"""
Dear {employee.first_name},

Please be informed that your previously assigned task has been cancelled.

📌 Task: {task.description}  
Originally Due: {task.due_date.strftime('%Y-%m-%d')}

No action is required on your part.

Blessings,  
DUNAMIS TV Management
"""
        msg = Message(subject, recipients=[employee.email], body=body)
        mail.send(msg)
        flash("Task deleted and employee notified via email.", "success")
    except Exception as e:
        flash(f"Failed to delete task or send email: {str(e)}", "danger")

    return redirect(url_for('main.add_task'))


@main.route('/task/update-status/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    status = request.form.get('status')

    if status == 'completed':
        task.completed = True
        task.completed_at = datetime.utcnow()
    elif status == 'undone':
        task.completed = False
        task.completed_at = None
        monthly_allowance = Employee.salary_per_day * 23
        deduction = round(0.01 * monthly_allowance, 2)
        msg = Message(
            subject="⚠ Task Marked as Undone",
            recipients=[Employee.email],
            body=f"""
    Dear {Employee.first_name},

    Your task has been marked as **UNDONE**:

    📝 Task: {task.description}  
    📅 Scheduled from {task.start_date} to {task.due_date}

    ⚠ A deduction of ₦{deduction} will apply to your monthly allowance as a result.

    Blessings,  
    DUNAMIS TV Management
    """)

    db.session.commit()
    flash("Task status updated successfully.", "success")
    return redirect(url_for('main.add_task'))

# ---------------- WORKING CYCLE ----------------

@main.route('/cycle/add', methods=['GET', 'POST'])
@login_required
def add_cycle():
    if request.method == 'POST':
        try:
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')

            if not start_date_str or not end_date_str:
                flash("Start and end dates are required.", "warning")
                return redirect(url_for('main.add_cycle'))

            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            # Optional: Prevent duplicates
            existing = WorkingCycle.query.filter_by(start_date=start_date, end_date=end_date).first()
            if existing:
                flash("A cycle with these dates already exists.", "info")
                return redirect(url_for('main.add_cycle'))

            name = start_date.strftime('%B %Y')

            all_cycles = WorkingCycle(
                start_date=start_date,
                end_date=end_date,
                is_active=True,  # Optional: you can set only one active at a time
                
            )
            print("🚀 Creating cycle:", name)
            db.session.add(all_cycles)
            db.session.commit()

            flash("New cycle created.", "success")
        except Exception as e:
            print(f"❌ Error: {e}")
            flash("An error occurred while creating the cycle.", "danger")
        print("✅ Cycle added successfully!")
        return redirect(url_for('main.add_cycle'))

    cycles = WorkingCycle.query.order_by(WorkingCycle.start_date.desc()).all()
    return render_template('add_cycle.html', all_cycles=cycles)



# ---------------- SALARY COMPUTATION ----------------
@main.route('/salary/compute', methods=['GET', 'POST'])
@login_required
def compute_salary():
    active_cycle = WorkingCycle.query.filter_by(is_active=True).first()
    if not active_cycle:
        flash("No active working cycle found.", "danger")
        return redirect(url_for('main.add_cycle'))

    employees = Employee.query.all()
    working_days = 23
    salary_data = []

    for emp in employees:
        tasks = Task.query.filter_by(employee_id=emp.id, cycle_id=active_cycle.id).all()
        completed_tasks = [t for t in tasks if t.completed]
        undone_tasks = [t for t in tasks if not t.completed]

        monthly_allowance = emp.salary_per_day * working_days
        deduction = round((1 / 100) * monthly_allowance * len(undone_tasks), 2)
        net_salary = round(monthly_allowance - deduction, 2)

        # Log to DB only if not already computed for this employee and cycle
        existing_log = SalaryLog.query.filter_by(employee_id=emp.id, cycle_id=active_cycle.id).first()
        if not existing_log:
            salary_log = SalaryLog(
                employee_id=emp.id,
                cycle_id=active_cycle.id,
                completed_tasks=len(completed_tasks),
                undone_tasks=len(undone_tasks),
                monthly_allowance=monthly_allowance,
                deduction=deduction,
                net_salary=net_salary
            )
            db.session.add(salary_log)

        # Send salary summary email
        try:
            subject = f"Dunamis! 💼 Salary Summary - {active_cycle.name}"
            body = f"""
Dear {emp.first_name},

Your salary summary for the cycle **{active_cycle.name}**:

✅ Tasks Completed: {len(completed_tasks)}  
❌ Tasks Undone: {len(undone_tasks)}  

📌 Monthly Allowance: ₦{monthly_allowance}  
📉 Deduction: ₦{deduction}  
💰 Final Salary: ₦{net_salary}

Thank you for your dedication.

Blessings,  
DUNAMIS TV Management
"""
            msg = Message(subject, recipients=[emp.email], body=body)
            mail.send(msg)
        except Exception as e:
            print(f"❌ Could not send email to {emp.email}: {e}")

        salary_data.append({
            'employee': emp,
            'completed': len(completed_tasks),
            'undone': len(undone_tasks),
            'monthly_allowance': monthly_allowance,
            'deduction': deduction,
            'net_salary': net_salary
        })

    db.session.commit()
    return render_template('compute_salary.html', salary_data=salary_data, cycle=active_cycle)

@main.route('/salary/summary/pdf')
def download_salary_summary():
    active_cycle = WorkingCycle.query.filter_by(is_active=True).first()
    if not active_cycle:
        flash("No active cycle found.", "danger")
        return redirect(url_for('main.compute_salary'))

    logs = SalaryLog.query.filter_by(cycle_id=active_cycle.id).all()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    y = 750
    pdf.drawString(50, y, f"Salary Summary Report - {active_cycle.name}")
    y -= 30

    for log in logs:
        emp = log.employee
        text = (f"{emp.first_name} {emp.surname} | "
                f"Completed: {log.completed_tasks}, "
                f"Undone: {log.undone_tasks}, "
                f"Allowance: ₦{log.monthly_allowance}, "
                f"Deduction: ₦{log.deduction}, "
                f"Net Salary: ₦{log.net_salary}")
        pdf.drawString(50, y, text)
        y -= 20
        if y < 100:
            pdf.showPage()
            y = 750

    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="salary_summary.pdf", mimetype='application/pdf')


@main.route('/salary/logs')
def view_salary_logs():
    logs = SalaryLog.query.join(WorkingCycle).order_by(WorkingCycle.start_date.desc()).all()
    print("successfully viewed salary log")
    return render_template('salary_logs.html', logs=logs)


@main.route('/dashboard')
@login_required
def dashboard():
    assigned_tasks = []
    if current_user.role == 'employee':
        return redirect(url_for('main.employee_dashboard'))
    elif current_user.role == 'task_admin':
        assigned_tasks = Task.query.filter_by(assigned_to=current_user.id).all()
    elif current_user.role == 'task_admin':
        flash("Welcome, Task Admin. You can manage tasks.", "info")
    
    
    return render_template(
        'employee_dashboard.html',
        assigned_tasks=assigned_tasks,
        is_task_admin=(current_user.role == 'task_admin'),
        is_admin=(current_user.role in ['admin', 'super_admin'])
    )



@main.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm = request.form['confirm']

        if new_password != confirm:
            flash("Passwords do not match", "danger")
            return redirect(url_for('main.reset_password'))

        current_user.password_hash = generate_password_hash(new_password)
        current_user.must_reset_password = False
        db.session.commit()
        flash("Password reset successfully!", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('reset_password.html')

@main.route('/cycle/toggle/<int:cycle_id>', methods=['POST'])
@login_required
def toggle_cycle(cycle_id):
    cycle = WorkingCycle.query.get_or_404(cycle_id)
    cycle.is_active = not cycle.is_active
    db.session.commit()

    status = "activated" if cycle.is_active else "deactivated"
    flash(f"Cycle {cycle.name} has been {status}.", "success")
    print("✅ cycle_history route hit. Found cycles:", cycle)
    return redirect(url_for('main.cycle_history'))

@main.route('/cycle/history')
@login_required
def cycle_history():
    cycles = WorkingCycle.query.order_by(WorkingCycle.start_date.desc()).all()
    print("✅ cycle_history route hit. Found cycles:", cycles)
    return render_template('cycle_history.html', cycles=cycles)

@main.route('/cycle/<int:cycle_id>/detail')
@login_required
def cycle_detail(cycle_id):
    cycle = WorkingCycle.query.get_or_404(cycle_id)
    
    # Get all tasks and salary logs within this cycle
    tasks = Task.query.filter(Task.start_date >= cycle.start_date, Task.start_date <= cycle.end_date).all()
    salary_logs = SalaryLog.query.filter(SalaryLog.cycle_id == cycle.id).all()

    return render_template('cycle_detail.html', cycle=cycle, tasks=tasks, salary_logs=salary_logs)


# routes.py or your main Blueprint file
from flask_login import login_required, current_user
from datetime import date
@main.route('/employee/dashboard')
@login_required
def employee_dashboard():
    user = current_user
    today = date.today()

    # Get current active cycle
    active_cycle = WorkingCycle.query.filter_by(is_active=True).first()

    # Tasks for current user in active cycle
    tasks = Task.query.filter_by(employee_id=user.id, cycle_id=active_cycle.id).all() if active_cycle else []

    # Task performance
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.completed])
    missed_tasks = total_tasks - completed_tasks
    performance_percent = round((completed_tasks / total_tasks) * 100, 1) if total_tasks else 0

    # Salary log for the current cycle
    salary_log = SalaryLog.query.filter_by(employee_id=user.id, cycle_id=active_cycle.id).first() if active_cycle else None

    # Days left in cycle
    countdown_days = (active_cycle.end_date - date.today()).days if active_cycle else 0

    return render_template(
        'employee_dashboard.html',
        tasks=tasks,
        active_cycle=active_cycle,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        missed_tasks=missed_tasks,
        performance_percent=performance_percent,
        salary_log=salary_log,
        countdown_days=countdown_days,
        date_today=today
    )


@main.route('/tasks')
@login_required
def view_tasks():
    tasks = Task.query.order_by(Task.start_date.desc()).all()
    return render_template('add_task.html', tasks=tasks)





