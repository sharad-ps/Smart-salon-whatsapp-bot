import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'salon_secret_key_change_me')
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    
    # WhatsApp API (Meta)
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
    WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN', 'salon_verify_token_123')
    
    # Business Settings
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    SALON_NAME = "Smart Salon"
    SALON_ADDRESS = "123 Main Street, City"
    SALON_PHONE = "+91 9876543210"
    
    # Payment
    UPI_ID = os.getenv('UPI_ID', 'salon@upi')
    QR_CODE_PATH = 'static/qr_code.jpg'  # Upload your QR code here
    
    # Services
    SERVICES = {
        "1": {"name": "Haircut (Men)", "price": 150, "duration": "30 min"},
        "2": {"name": "Haircut (Women)", "price": 300, "duration": "45 min"},
        "3": {"name": "Beard Trim", "price": 80, "duration": "15 min"},
        "4": {"name": "Haircut + Beard Combo", "price": 200, "duration": "45 min"},
        "5": {"name": "Facial Treatment", "price": 500, "duration": "60 min"},
        "6": {"name": "Hair Coloring", "price": 800, "duration": "90 min"},
        "7": {"name": "Spa Package", "price": 1500, "duration": "120 min"},
        "8": {"name": "Bridal Makeup", "price": 2500, "duration": "180 min"},
    }
    
    # Time Slots
    TIME_SLOTS = [
        "10:00 AM", "11:00 AM", "12:00 PM",
        "01:00 PM", "02:00 PM", "03:00 PM",
        "04:00 PM", "05:00 PM", "06:00 PM", "07:00 PM"
    ]
    
    # Payment threshold
    ADVANCE_PAYMENT_THRESHOLD = 1000
    ADVANCE_PERCENTAGE = 0.5  # 50%
