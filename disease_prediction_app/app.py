from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Zukaata_1245",
        database="diseaseprediction"
    )

# Fetch symptoms from database for dropdown
@app.route("/get_symptoms", methods=["GET"])
def get_symptoms():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT symptoms FROM Diseases")
    symptoms = cursor.fetchall()
    conn.close()
    
    symptom_list = []
    for symptom in symptoms:
        symptom_list.extend(symptom[0].split(", "))  # Splitting symptom list
    
    return jsonify(list(set(symptom_list)))  # Returning unique symptoms


# Predict disease based on symptoms
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    selected_symptoms = data.get("symptoms", [])

    if not selected_symptoms:
        return jsonify({"error": "No symptoms provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Find disease matching the highest number of symptoms
    cursor.execute("SELECT disease, symptoms FROM Diseases")
    diseases = cursor.fetchall()
    
    best_match = None
    max_count = 0

    for disease, symptoms in diseases:
        disease_symptoms = symptoms.split(", ")
        match_count = len(set(selected_symptoms) & set(disease_symptoms))

        if match_count > max_count:
            max_count = match_count
            best_match = disease

    if not best_match:
        return jsonify({"error": "No matching disease found"}), 404

    # Fetch doctors treating the predicted disease
    cursor.execute("SELECT name, degree, specialization, hospital, location FROM Doctors WHERE disease = %s", (best_match,))
    doctors = cursor.fetchall()
    conn.close()

    return jsonify({
        "disease": best_match,
        "doctors": [{"name": doc[0], "degree": doc[1], "specialization": doc[2], "hospital": doc[3], "location": doc[4]} for doc in doctors]
    })


# Load the main page
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
