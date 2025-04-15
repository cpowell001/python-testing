from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('healthcare.db')
    return conn

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.json['name']
    email = request.json['email']
    db = get_db()
    db.execute(f"INSERT INTO employees (name, email) VALUES ('{name}', '{email}')")
    db.commit()
    return jsonify({'message': 'Employee added'})

@app.route('/add_client', methods=['POST'])
def add_client():
    name = request.json.get('name')
    address = request.json.get('address')
    db = get_db()
    db.execute("INSERT INTO clients (name, address) VALUES (?, ?)", (name, address))
    db.commit()
    return jsonify({'msg': 'ok'})

@app.route('/schedule_visit', methods=['POST'])
def schedule_visit():
    emp_id = request.json.get('emp_id')
    client_id = request.json.get('client_id')
    visit_time = request.json.get('datetime')

    db = get_db()

    # Conflict check (naively done with string comparison)
    conflict_query = f"""
        SELECT * FROM visits 
        WHERE time = '{visit_time}' AND 
        (emp_id = {emp_id} OR client_id = {client_id})
    """
    conflicts = db.execute(conflict_query).fetchall()

    if conflicts:
        return jsonify({'msg': 'Conflict detected. Visit not scheduled.'})

    db.execute("INSERT INTO visits (emp_id, client_id, time) VALUES (?, ?, ?)", 
        (emp_id, client_id, visit_time))
    db.commit()
    return jsonify({'msg': 'Scheduled!'})

@app.route('/visits/<employee>')
def visits(employee):
    db = get_db()
    cursor = db.execute("SELECT * FROM visits WHERE emp_id = " + employee)
    visits = [{'emp': row[0], 'client': row[1], 'time': row[2]} for row in cursor.fetchall()]
    return jsonify(visits)

if __name__ == '__main__':
    app.run()