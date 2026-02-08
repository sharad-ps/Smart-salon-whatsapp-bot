import sqlite3
from datetime import datetime, timedelta
import json
from config import Config

class Database:
    def __init__(self, db_name="salon.db"):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                phone TEXT PRIMARY KEY,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT,
                name TEXT,
                services TEXT,
                date TEXT,
                time TEXT,
                total INTEGER,
                advance_required INTEGER DEFAULT 0,
                payment_screenshot TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                admin_notes TEXT,
                FOREIGN KEY (phone) REFERENCES users(phone)
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                phone TEXT PRIMARY KEY,
                step TEXT,
                data TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_user(self, phone, name=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (phone, name)
            VALUES (?, ?)
        ''', (phone, name))
        conn.commit()
        conn.close()
    
    def get_user(self, phone):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE phone = ?', (phone,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    def save_booking(self, phone, name, services, date, time, total, advance_required=0, status='pending'):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (phone, name, services, date, time, total, advance_required, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (phone, name, json.dumps(services), date, time, total, advance_required, status))
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return booking_id
    
    def get_bookings(self, phone=None, status=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = 'SELECT * FROM bookings WHERE 1=1'
        params = []
        
        if phone:
            query += ' AND phone = ?'
            params.append(phone)
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        query += ' ORDER BY created_at DESC'
        cursor.execute(query, params)
        bookings = cursor.fetchall()
        conn.close()
        return [dict(b) for b in bookings]
    
    def update_booking(self, booking_id, **kwargs):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        set_clause = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [booking_id]
        
        cursor.execute(f'''
            UPDATE bookings 
            SET {set_clause}
            WHERE id = ?
        ''', values)
        conn.commit()
        conn.close()
    
    def get_booking(self, booking_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,))
        booking = cursor.fetchone()
        conn.close()
        return dict(booking) if booking else None
    
    def save_session(self, phone, step, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO sessions (phone, step, data, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (phone, step, json.dumps(data)))
        conn.commit()
        conn.close()
    
    def get_session(self, phone):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sessions WHERE phone = ?', (phone,))
        session = cursor.fetchone()
        conn.close()
        if session:
            return {
                'step': session['step'],
                'data': json.loads(session['data'])
            }
        return {'step': 'menu', 'data': {}}
    
    def get_booked_slots(self, date):
        """Get already booked time slots for a date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT time FROM bookings 
            WHERE date = ? AND status IN ('confirmed', 'pending', 'payment_pending')
        ''', (date,))
        slots = cursor.fetchall()
        conn.close()
        return [s['time'] for s in slots]
    
    def delete_booking(self, booking_id):
        """Delete a booking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
        conn.commit()
        conn.close()
