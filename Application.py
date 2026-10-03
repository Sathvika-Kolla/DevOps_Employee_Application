from flask import Flask, request, jsonify

app = Flask(__name__)

employees = [
    {"id": 1, "name": "Rahul", "role": "Cloud Engineer"},
    {"id": 2, "name": "Priya", "role": "DevOps Engineer"},
    {"id": 3, "name": "Arjun", "role": "Software Engineer"}
]


@app.route("/")
def home():
    return "Employee Management Application is running!"


@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "message": "Application is healthy"
    })


@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)


@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    employee = next(
        (emp for emp in employees if emp["id"] == employee_id),
        None
    )

    if employee:
        return jsonify(employee)

    return jsonify({"error": "Employee not found"}), 404


@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.get_json()

    new_employee = {
        "id": len(employees) + 1,
        "name": data["name"],
        "role": data["role"]
    }

    employees.append(new_employee)

    return jsonify(new_employee), 201


@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    employee = next(
        (emp for emp in employees if emp["id"] == employee_id),
        None
    )

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json()

    employee["name"] = data.get("name", employee["name"])
    employee["role"] = data.get("role", employee["role"])

    return jsonify(employee)


@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    employee = next(
        (emp for emp in employees if emp["id"] == employee_id),
        None
    )

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    employees.remove(employee)

    return jsonify({
        "message": "Employee deleted successfully"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)