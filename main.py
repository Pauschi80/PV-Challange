from flask import Flask, request, jsonify
import sqlite3
import os
import requests
import json

app = Flask(__name__)

def get_db_connection():
    """Create and return a database connection"""
    if not os.path.exists('patients.db'):
        return None
    conn = sqlite3.connect('patients.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route('/patient/<name>', methods=['GET'])
def get_patient_by_name(name):
    """Get a patient and all their data by name"""
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database not found'}), 404

        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM patients WHERE name = ?
        ''', (name,))

        patient = cursor.fetchone()
        conn.close()

        if patient is None:
            return jsonify({'error': f'Patient with name "{name}" not found'}), 404

        # Convert Row object to dictionary
        patient_data = dict(patient)

        return jsonify({
            'status': 'success',
            'data': patient_data
        }), 200

    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/patients', methods=['GET'])
def get_all_patients():
    """Get all patients (optional endpoint for testing)"""
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database not found'}), 404

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients')
        patients = cursor.fetchall()
        conn.close()

        # Convert list of Row objects to list of dictionaries
        patients_data = [dict(patient) for patient in patients]

        return jsonify({
            'status': 'success',
            'count': len(patients_data),
            'data': patients_data
        }), 200

    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/patient/search', methods=['GET'])
def search_patients():
    """Search patients by partial name match"""
    search_term = request.args.get('q', '')

    if not search_term:
        return jsonify({'error': 'Search query parameter "q" is required'}), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database not found'}), 404

        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM patients WHERE name LIKE ?
        ''', (f'%{search_term}%',))

        patients = cursor.fetchall()
        conn.close()

        # Convert list of Row objects to list of dictionaries
        patients_data = [dict(patient) for patient in patients]

        return jsonify({
            'status': 'success',
            'count': len(patients_data),
            'data': patients_data
        }), 200

    except Exception as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/llm/analyze-patient', methods=['POST'])
def analyze_patient_with_llm():
    """Get a patient by name and analyze their rehabilitation goals, history, and diagnosis"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Request must include "name" field'}), 400

        patient_name = data['name']
        model = 'llama3.2:1b'  # Fixed model

        # Get patient data from database
        conn = get_db_connection()
        if conn is None:
            return jsonify({'error': 'Database not found'}), 404

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients WHERE name = ?', (patient_name,))
        patient = cursor.fetchone()
        conn.close()

        if patient is None:
            return jsonify({'error': f'Patient with name "{patient_name}" not found'}), 404

        # Convert patient data to dictionary
        patient_data = dict(patient)

        # Extract the three key fields for analysis
        teilhabeziel = patient_data.get('teilhabeziel', 'Nicht angegeben')
        reha_anamnese = patient_data.get('reha_spezifische_anamnese', 'Nicht angegeben')
        diagnose = patient_data.get('diagnose', 'Nicht angegeben')

        # Create focused analysis prompt in German
        analysis_prompt = f"""Bitte erstelle eine umfassende Zusammenfassung und Analyse basierend auf den folgenden Patienteninformationen:

1. DIAGNOSE: {diagnose}

2. REHA-SPEZIFISCHE ANAMNESE: {reha_anamnese}

3. TEILHABEZIEL: {teilhabeziel}

Bitte analysiere:
- Wie die Diagnose mit den Rehabilitationszielen zusammenhängt
- Ob die Teilhabeziele realistisch sind angesichts der Diagnose und Anamnese
- Wichtige Erkenntnisse über den Rehabilitationsverlauf des Patienten
- Mögliche Herausforderungen oder Chancen bei der Erreichung der Teilhabeziele
- Empfehlungen für den Rehabilitationsprozess

Bitte antworte auf Deutsch und strukturiere deine Antwort klar und verständlich."""

        # Query Ollama
        ollama_url = "http://localhost:11434/api/generate"
        ollama_payload = {
            "model": model,
            "prompt": analysis_prompt,
            "stream": False
        }

        response = requests.post(ollama_url, json=ollama_payload, timeout=60)

        if response.status_code != 200:
            return jsonify({
                'error': f'Ollama API error: {response.status_code}',
                'details': response.text
            }), 500

        ollama_response = response.json()

        return jsonify({
            'status': 'success',
            'patient_name': patient_name,
            'key_fields': {
                'diagnose': diagnose,
                'reha_spezifische_anamnese': reha_anamnese,
                'teilhabeziel': teilhabeziel
            },
            'analysis_summary': ollama_response.get('response', ''),
            'model': model
        }), 200

    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Cannot connect to Ollama. Make sure Ollama is running on localhost:11434'
        }), 503
    except Exception as e:
        return jsonify({'error': f'Patient analysis error: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if database exists on startup
    if not os.path.exists('patients.db'):
        print("Warning: patients.db not found. Please run the data loading script first.")

    app.run(debug=True, host='0.0.0.0', port=6969)

