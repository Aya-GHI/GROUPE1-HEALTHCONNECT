# HealthConnect Flask Backend
# Install required packages:
# pip install flask flask-cors mysql-connector-python python-dotenv bcrypt PyJWT

import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import bcrypt
import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
app.config['JWT_EXPIRATION_HOURS'] = 24

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'healthconnect')
}

# ==================== DATABASE CONNECTION ====================
def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def execute_query(query, params=None, fetch=True):
    """Execute a database query and return results"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid
        
        cursor.close()
        conn.close()
        return result
    except mysql.connector.Error as err:
        print(f"Query execution error: {err}")
        conn.close()
        return None

# ==================== AUTHENTICATION HELPERS ====================
def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify a password against a hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_token(user_id):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=app.config['JWT_EXPIRATION_HOURS'])
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# ==================== API ROUTES ====================

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API and database are working"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 500

# ==================== SPECIALTIES ROUTES ====================
@app.route('/api/specialties', methods=['GET'])
def get_specialties():
    """Get all specialties"""
    query = "SELECT * FROM specialties ORDER BY name"
    specialties = execute_query(query)
    
    if specialties is not None:
        return jsonify(specialties), 200
    return jsonify({'error': 'Failed to fetch specialties'}), 500

# ==================== DOCTORS ROUTES ====================
@app.route('/api/doctors', methods=['GET'])
def get_all_doctors():
    """Get all doctors with optional filters"""
    specialty = request.args.get('specialty')
    city = request.args.get('city')
    search = request.args.get('search')
    
    query = """
        SELECT 
            d.doctor_id,
            d.first_name,
            d.last_name,
            CONCAT(d.first_name, ' ', d.last_name) AS name,
            s.name AS specialty,
            d.email,
            d.phone,
            CONCAT(d.address, ', ', d.city, ', ', d.state) AS address,
            d.city,
            d.state,
            d.image_url AS image,
            d.bio,
            d.years_of_experience,
            d.education
        FROM doctors d
        JOIN specialties s ON d.specialty_id = s.specialty_id
        WHERE d.is_active = TRUE
    """
    
    params = []
    
    if specialty:
        query += " AND s.name = %s"
        params.append(specialty)
    
    if city:
        query += " AND d.city LIKE %s"
        params.append(f"%{city}%")
    
    if search:
        query += " AND (d.first_name LIKE %s OR d.last_name LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])
    
    query += " ORDER BY d.last_name, d.first_name"
    
    doctors = execute_query(query, tuple(params))
    
    if doctors is not None:
        return jsonify(doctors), 200
    return jsonify({'error': 'Failed to fetch doctors'}), 500

@app.route('/api/dentists', methods=['GET'])
def get_dentists():
    """Get all dentists"""
    query = """
        SELECT 
            d.doctor_id,
            CONCAT(d.first_name, ' ', d.last_name) AS name,
            s.name AS specialty,
            CONCAT(d.address, ', ', d.city, ', ', d.state) AS address,
            d.image_url AS image
        FROM doctors d
        JOIN specialties s ON d.specialty_id = s.specialty_id
        WHERE s.name = 'Dentistry' AND d.is_active = TRUE
    """
    doctors = execute_query(query)
    return jsonify(doctors if doctors else []), 200

@app.route('/api/cardiology', methods=['GET'])
def get_cardiologists():
    """Return all cardiologists from v_doctors_full"""
    query = """
        SELECT *
        FROM v_doctors_full
        WHERE specialty = %s
    """
    doctors = execute_query(query, ("Cardiology",))

    if doctors is not None:
        return jsonify(doctors), 200
    return jsonify({"error": "Failed to fetch cardiologists"}), 500


@app.route('/api/dermatology', methods=['GET'])
def get_dermatologists():
    """Get all dermatologists"""
    query = """
        SELECT 
            d.doctor_id,
            CONCAT(d.first_name, ' ', d.last_name) AS name,
            s.name AS specialty,
            CONCAT(d.address, ', ', d.city, ', ', d.state) AS address,
            d.image_url AS image
        FROM doctors d
        JOIN specialties s ON d.specialty_id = s.specialty_id
        WHERE s.name = 'Dermatology' AND d.is_active = TRUE
    """
    doctors = execute_query(query)
    return jsonify(doctors if doctors else []), 200

@app.route('/api/pediatrics', methods=['GET'])
def get_pediatricians():
    """Get all pediatricians"""
    query = """
        SELECT 
            d.doctor_id,
            CONCAT(d.first_name, ' ', d.last_name) AS name,
            s.name AS specialty,
            CONCAT(d.address, ', ', d.city, ', ', d.state) AS address,
            d.image_url AS image
        FROM doctors d
        JOIN specialties s ON d.specialty_id = s.specialty_id
        WHERE s.name = 'Pediatrics' AND d.is_active = TRUE
    """
    doctors = execute_query(query)
    return jsonify(doctors if doctors else []), 200

@app.route('/api/ophthalmology', methods=['GET'])
def get_ophthalmologists():
    """Get all ophthalmologists"""
    query = """
        SELECT 
            d.doctor_id,
            CONCAT(d.first_name, ' ', d.last_name) AS name,
            s.name AS specialty,
            CONCAT(d.address, ', ', d.city, ', ', d.state) AS address,
            d.image_url AS image
        FROM doctors d
        JOIN specialties s ON d.specialty_id = s.specialty_id
        WHERE s.name = 'Ophthalmology' AND d.is_active = TRUE
    """
    doctors = execute_query(query)
    return jsonify(doctors if doctors else []), 200

@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    """Get a specific doctor by ID"""
    query = """
        SELECT 
            d.*,
            s.name AS specialty_name,
            AVG(r.rating) AS average_rating,
            COUNT(r.review_id) AS review_count
        FROM doctors d
        JOIN specialties s ON d.specialty_id = s.specialty_id
        LEFT JOIN reviews r ON d.doctor_id = r.doctor_id
        WHERE d.doctor_id = %s AND d.is_active = TRUE
        GROUP BY d.doctor_id
    """
    doctor = execute_query(query, (doctor_id,))
    
    if doctor and len(doctor) > 0:
        return jsonify(doctor[0]), 200
    return jsonify({'error': 'Doctor not found'}), 404

@app.route('/api/doctors/<int:doctor_id>/availability', methods=['GET'])
def get_doctor_availability(doctor_id):
    """Get doctor availability schedule"""
    query = """
        SELECT 
            availability_id,
            day_of_week,
            start_time,
            end_time,
            is_available
        FROM doctor_availability
        WHERE doctor_id = %s AND is_available = TRUE
        ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    """
    availability = execute_query(query, (doctor_id,))
    
    if availability is not None:
        # Convert time objects to strings
        for slot in availability:
            slot['start_time'] = str(slot['start_time'])
            slot['end_time'] = str(slot['end_time'])
        return jsonify(availability), 200
    return jsonify({'error': 'Failed to fetch availability'}), 500

# ==================== USER AUTHENTICATION ROUTES ====================
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    
    # Validate required fields
    required_fields = ['firstName', 'surname', 'email', 'password', 'phoneNumber', 'dateOfBirth', 'gender']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if email already exists
    check_query = "SELECT user_id FROM users WHERE email = %s"
    existing_user = execute_query(check_query, (data['email'],))
    
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 409
    
    # Hash password
    hashed_pw = hash_password(data['password'])
    
    # Parse date of birth (DD/MM/YYYY to YYYY-MM-DD)
    try:
        dob = datetime.strptime(data['dateOfBirth'], '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use DD/MM/YYYY'}), 400
    
    # Insert new user
    insert_query = """
        INSERT INTO users 
        (first_name, last_name, email, password_hash, phone, date_of_birth, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data['firstName'],
        data['surname'],
        data['email'],
        hashed_pw,
        data['phoneNumber'],
        dob,
        data['gender']
    )
    
    user_id = execute_query(insert_query, params, fetch=False)
    
    if user_id:
        token = generate_token(user_id)
        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user_id': user_id
        }), 201
    
    return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    
    if not data.get('emailUsername') or not data.get('password'):
        return jsonify({'error': 'Email/Username and password required'}), 400
    
    # Get user by email
    query = "SELECT user_id, email, password_hash, first_name, last_name FROM users WHERE email = %s AND is_active = TRUE"
    user = execute_query(query, (data['emailUsername'],))
    
    if not user or len(user) == 0:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    user = user[0]
    
    # Verify password
    if not verify_password(data['password'], user['password_hash']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate token
    token = generate_token(user['user_id'])
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'user_id': user['user_id'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name']
        }
    }), 200

# ==================== APPOINTMENTS ROUTES ====================
@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    """Create a new appointment"""
    data = request.json
    
    # Validate token
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header.split(' ')[1]
    user_id = verify_token(token)
    
    if not user_id:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    # Validate required fields
    if not all(k in data for k in ['doctor_id', 'appointment_date', 'appointment_time']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if time slot is available
    check_query = """
        SELECT appointment_id FROM appointments 
        WHERE doctor_id = %s 
        AND appointment_date = %s 
        AND appointment_time = %s 
        AND status != 'cancelled'
    """
    existing = execute_query(check_query, (
        data['doctor_id'],
        data['appointment_date'],
        data['appointment_time']
    ))
    
    if existing:
        return jsonify({'error': 'Time slot not available'}), 409
    
    # Create appointment
    insert_query = """
        INSERT INTO appointments 
        (user_id, doctor_id, appointment_date, appointment_time, reason, status)
        VALUES (%s, %s, %s, %s, %s, 'scheduled')
    """
    params = (
        user_id,
        data['doctor_id'],
        data['appointment_date'],
        data['appointment_time'],
        data.get('reason', '')
    )
    
    appointment_id = execute_query(insert_query, params, fetch=False)
    
    if appointment_id:
        return jsonify({
            'message': 'Appointment created successfully',
            'appointment_id': appointment_id
        }), 201
    
    return jsonify({'error': 'Failed to create appointment'}), 500

@app.route('/api/appointments/user', methods=['GET'])
def get_user_appointments():
    """Get all appointments for logged-in user"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header.split(' ')[1]
    user_id = verify_token(token)
    
    if not user_id:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    query = """
        SELECT 
            a.*,
            CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
            s.name AS specialty,
            d.image_url AS doctor_image
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.doctor_id
        JOIN specialties s ON d.specialty_id = s.specialty_id
        WHERE a.user_id = %s
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
    """
    
    appointments = execute_query(query, (user_id,))
    
    if appointments is not None:
        # Convert date and time objects to strings
        for apt in appointments:
            apt['appointment_date'] = str(apt['appointment_date'])
            apt['appointment_time'] = str(apt['appointment_time'])
        return jsonify(appointments), 200
    
    return jsonify({'error': 'Failed to fetch appointments'}), 500

@app.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """Update appointment status"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header.split(' ')[1]
    user_id = verify_token(token)
    
    if not user_id:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    data = request.json
    
    # Verify appointment belongs to user
    check_query = "SELECT user_id FROM appointments WHERE appointment_id = %s"
    appointment = execute_query(check_query, (appointment_id,))
    
    if not appointment or appointment[0]['user_id'] != user_id:
        return jsonify({'error': 'Appointment not found'}), 404
    
    # Update status
    update_query = "UPDATE appointments SET status = %s WHERE appointment_id = %s"
    execute_query(update_query, (data.get('status'), appointment_id), fetch=False)
    
    return jsonify({'message': 'Appointment updated successfully'}), 200

# ==================== REVIEWS ROUTES ====================
@app.route('/api/reviews/doctor/<int:doctor_id>', methods=['GET'])
def get_doctor_reviews(doctor_id):
    """Get all reviews for a doctor"""
    query = """
        SELECT 
            r.*,
            CONCAT(u.first_name, ' ', u.last_name) AS user_name
        FROM reviews r
        JOIN users u ON r.user_id = u.user_id
        WHERE r.doctor_id = %s
        ORDER BY r.created_at DESC
    """
    
    reviews = execute_query(query, (doctor_id,))
    
    if reviews is not None:
        for review in reviews:
            review['created_at'] = str(review['created_at'])
        return jsonify(reviews), 200
    
    return jsonify({'error': 'Failed to fetch reviews'}), 500

@app.route('/api/reviews', methods=['POST'])
def create_review():
    """Create a new review"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    
    token = auth_header.split(' ')[1]
    user_id = verify_token(token)
    
    if not user_id:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    data = request.json
    
    if not all(k in data for k in ['doctor_id', 'rating']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Insert review
    insert_query = """
        INSERT INTO reviews (user_id, doctor_id, rating, comment)
        VALUES (%s, %s, %s, %s)
    """
    params = (
        user_id,
        data['doctor_id'],
        data['rating'],
        data.get('comment', '')
    )
    
    review_id = execute_query(insert_query, params, fetch=False)
    
    if review_id:
        return jsonify({
            'message': 'Review created successfully',
            'review_id': review_id
        }), 201
    
    return jsonify({'error': 'Failed to create review'}), 500

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/routes', methods=['GET'])
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'path': str(rule.rule)
        })
    return jsonify(routes), 200

# ==================== RUN APPLICATION ====================
if __name__ == '__main__':
    print("=" * 50)
    print("HealthConnect Flask Backend")
    print("=" * 50)
    print(f"Database: {DB_CONFIG['database']}")
    print(f"Host: {DB_CONFIG['host']}")
    print("Server starting on http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)