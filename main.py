from flask import Flask, request, jsonify
import sqlite3
import os

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

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Patient API'
    }), 200

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

