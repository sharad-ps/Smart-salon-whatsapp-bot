from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from database import Database
from whatsapp_handler import WhatsAppHandler
from config import Config
import os
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)

# Initialize
db = Database()
whatsapp = WhatsAppHandler()

# Ensure upload folder exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

def get_next_7_days():
    """Get next 7 days for booking"""
    today = datetime.now()
    dates = []
    for i in range(7):
        date = today + timedelta(days=i)
        label = "Today" if i == 0 else ("Tomorrow" if i == 1 else date.strftime("%d %b, %a"))
        dates.append({
            "value": date.strftime("%Y-%m-%d"),
            "label": label
        })
    return dates

def format_service_list():
    """Format service list for display"""
    text = "*📋 Our Services:*\n\n"
    for key, service in Config.SERVICES.items():
        text += f"{key}. {service['name']}\n"
        text += f"   💰 ₹{service['price']} | ⏱️ {service['duration']}\n\n"
    return text

def get_available_slots(date):
    """Get available time slots for a date"""
    booked_slots = db.get_booked_slots(date)
    available = [slot for slot in Config.TIME_SLOTS if slot not in booked_slots]
    return available

def is_valid_service_input(message):
    """Validate service selection format"""
    try:
        service_nums = [s.strip() for s in message.replace(' ', '').split(',')]
        for num in service_nums:
            if num not in Config.SERVICES:
                return False
        return len(service_nums) > 0
    except:
        return False

# =================== WEBHOOK VERIFICATION ===================

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verify webhook for WhatsApp"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == Config.VERIFY_TOKEN:
        return challenge, 200
    return 'Forbidden', 403

# =================== WEBHOOK HANDLER ===================

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    try:
        data = request.get_json()
        
        if not data.get('entry'):
            return jsonify({'status': 'ok'}), 200
        
        entry = data['entry'][0]
        changes = entry.get('changes', [])
        
        if not changes:
            return jsonify({'status': 'ok'}), 200
        
        change = changes[0]
        value = change.get('value', {})
        messages = value.get('messages', [])
        
        if not messages:
            return jsonify({'status': 'ok'}), 200
        
        message = messages[0]
        from_phone = message['from']
        
        # Handle different message types
        message_type = message.get('type')
        
        if message_type == 'text':
            text = message['text']['body']
            handle_text_message(from_phone, text)
        
        elif message_type == 'interactive':
            interactive = message['interactive']
            if interactive['type'] == 'button_reply':
                button_text = interactive['button_reply']['title']
                handle_text_message(from_phone, button_text)
            elif interactive['type'] == 'list_reply':
                list_text = interactive['list_reply']['title']
                handle_text_message(from_phone, list_text)
        
        elif message_type == 'image':
            media_id = message['image']['id']
            handle_payment_screenshot(from_phone, media_id)
        
        return jsonify({'status': 'ok'}), 200
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# =================== MESSAGE HANDLER ===================

def handle_text_message(phone, message):
    """Process text messages"""
    user_session = db.get_session(phone)
    step = user_session['step']
    data = user_session['data']
    
    new_step, new_data, response = process_bot_logic(phone, step, data, message)
    
    db.save_session(phone, new_step, new_data)
    
    send_bot_response(phone, new_step, new_data, response)

def process_bot_logic(phone, step, data, message):
    """Main bot logic with improved error handling"""
    if step is None or step =="":
       step="menu"
    
    if not data:
        data = {
            'services': [],
            'total': 0,
            'date': None,
            'time': None,
            'name': None
        }
    
    response = ""
    
    # Universal menu command
    if message.lower() in ['menu', 'main menu', 'start', 'restart', 'back to menu']:
        user = db.get_user(phone)
        if user and user.get('name'):
            response = f"👋 Welcome back *{user['name']}*!\n\n"
        else:
            response = f"👋 Welcome to *{Config.SALON_NAME}*!\n\n"
        response += "How can I help you today?"
        return 'menu', {}, response
    
    # Menu
    if step == message.lower() in ['hi', 'hello', 'hey', 'namaste']:
        user = db.get_user(phone)
        if user and user.get('name'):
            response = f"👋 Welcome back *{user['name']}*!\n\n"
        else:
            response = f"👋 Welcome to *{Config.SALON_NAME}*!\n\n"
        
        response += "How can I help you today?"
        step = 'menu'
        data = {}
    
    # New Booking
    elif "New Booking" in message:
        user = db.get_user(phone)
        if not user or not user.get('name'):
            response = "Please enter your name:"
            step = 'get_name'
        else:
            data['name'] = user['name']
            response = format_service_list()
            response += "📝 *How to select:*\n"
            response += "Reply with service numbers separated by commas\n"
            response += "Example: 1,3,5\n\n"
            response += "Type *Menu* to go back"
            step = 'select_services'
    
    # Get Name
    elif step == 'get_name':
        name = message.strip()
        if len(name) < 2:
            response = "❌ Please enter a valid name (at least 2 characters):"
            return step, data, response
        
        if name.lower() == 'menu':
            return 'menu', {}, "Returning to main menu..."
        
        data['name'] = name
        db.save_user(phone, name)
        
        response = f"Nice to meet you, *{name}*! 😊\n\n"
        response += format_service_list()
        response += "📝 *How to select:*\n"
        response += "Reply with service numbers separated by commas\n"
        response += "Example: 1,3,5\n\n"
        response += "Type *Menu* to cancel"
        step = 'select_services'
    
    # Select Services
    elif step == 'select_services':
        if message.lower() in ['cancel', 'back']:
            return 'menu', {}, "❌ Booking cancelled. Returning to main menu..."
        
        if not is_valid_service_input(message):
            response = "❌ *Invalid format!*\n\n"
            response += "Please enter service numbers separated by commas.\n"
            response += "Example: 1,3,5\n\n"
            response += format_service_list()
            response += "Or type *Menu* to cancel"
            return step, data, response
        
        try:
            service_numbers = [s.strip() for s in message.replace(' ', '').split(',')]
            valid_services = []
            total = 0
            
            for num in service_numbers:
                if num in Config.SERVICES:
                    valid_services.append(num)
                    total += Config.SERVICES[num]['price']
            
            if not valid_services:
                response = "❌ No valid services selected. Please try again.\n\n"
                response += format_service_list()
                return step, data, response
            
            data['services'] = valid_services
            data['total'] = total
            
            response = "*✅ Selected Services:*\n\n"
            for num in valid_services:
                service = Config.SERVICES[num]
                response += f"✓ {service['name']} - ₹{service['price']}\n"
            
            response += f"\n*💰 Total Amount: ₹{total}*\n\n"
            
            if total >= Config.ADVANCE_PAYMENT_THRESHOLD:
                advance = int(total * Config.ADVANCE_PERCENTAGE)
                data['advance_required'] = advance
                response += f"⚠️ *Advance Payment: ₹{advance} required*\n"
                response += "(50% advance to confirm booking)\n\n"
            
            response += "📅 Now, select your preferred date:"
            step = 'select_date'
        
        except Exception as e:
            response = "❌ Something went wrong. Please try again.\n\n"
            response += "Example format: 1,3,5\n\n"
            response += format_service_list()
            return step, data, response
    
    # Select Date
    elif step == 'select_date':
        if message.lower() in ['back', 'change services']:
            response = format_service_list()
            response += "Reply with service numbers (e.g., 1,3,5)"
            return 'select_services', {'name': data.get('name')}, response
        
        dates = get_next_7_days()
        date_mapping = {d['label']: d['value'] for d in dates}
        
        if message in date_mapping:
            data['date'] = date_mapping[message]
            data['date_label'] = message
            
            available_slots = get_available_slots(data['date'])
            
            if not available_slots:
                response = "❌ *No slots available!*\n\n"
                response += f"Sorry, all time slots are booked for {message}.\n"
                response += "Please select another date.\n\n"
                response += "Type *Back* to change services or *Menu* to cancel"
                return step, data, response
            
            response = f"*📅 Date Selected: {message}*\n\n"
            response += "⏰ *Available Time Slots:*\n\n"
            for slot in available_slots:
                response += f"• {slot}\n"
            response += "\nReply with your preferred time\n"
            response += "Or type *Back* to change date"
            step = 'select_time'
        else:
            response = "❌ Invalid date selection.\n\n"
            response += "Please choose from the available dates.\n"
            response += "Type *Back* to change services or *Menu* to cancel"
    
    # Select Time
    elif step == 'select_time':
        if message.lower() in ['back', 'change date']:
            response = "Select your preferred date:"
            return 'select_date', data, response
        
        available_slots = get_available_slots(data['date'])
        
        if message in available_slots:
            data['time'] = message
            
            response = "*📋 Booking Summary*\n\n"
            response += f"*👤 Name:* {data['name']}\n"
            response += f"*📅 Date:* {data.get('date_label', data['date'])}\n"
            response += f"*🕐 Time:* {data['time']}\n\n"
            
            response += "*💇 Services:*\n"
            for num in data['services']:
                service = Config.SERVICES[num]
                response += f"• {service['name']} - ₹{service['price']}\n"
            
            response += f"\n*💰 Total Amount: ₹{data['total']}*\n\n"
            
            if data['total'] >= Config.ADVANCE_PAYMENT_THRESHOLD:
                advance = data.get('advance_required', 0)
                response += f"💳 *Advance Payment: ₹{advance}*\n"
                response += "50% advance required to confirm booking.\n\n"
                response += "Click *Proceed to Payment* to continue\n"
                response += "or *Cancel* to go back"
                step = 'confirm_with_payment'
            else:
                response += "✅ No advance payment required!\n\n"
                response += "Click *Confirm Now* to book your appointment\n"
                response += "or *Cancel* to go back"
                step = 'confirm_without_payment'
        else:
            response = "❌ Invalid time slot.\n\n"
            response += "Please choose from available slots:\n"
            for slot in available_slots:
                response += f"• {slot}\n"
            response += "\nType *Back* to change date"
    
    # Confirm without payment (< ₹1000)
    elif step == 'confirm_without_payment':
        if message in ["✅ Confirm Now", "Confirm", "Yes", "Book"]:
            booking_id = db.save_booking(
                phone=phone,
                name=data['name'],
                services=data['services'],
                date=data['date'],
                time=data['time'],
                total=data['total'],
                advance_required=0,
                status='confirmed'
            )
            
            response = "🎉 *Booking Confirmed!*\n\n"
            response += f"*Booking ID:* #{booking_id}\n"
            response += f"*Date:* {data.get('date_label', data['date'])}\n"
            response += f"*Time:* {data['time']}\n\n"
            
            services_text = ', '.join([Config.SERVICES[s]['name'] for s in data['services']])
            response += f"*Services:* {services_text}\n"
            response += f"*Total:* ₹{data['total']}\n\n"
            
            response += f"✨ See you at *{Config.SALON_NAME}*!\n\n"
            response += f"📍 {Config.SALON_ADDRESS}\n"
            response += f"📞 {Config.SALON_PHONE}\n\n"
            response += "Type *Menu* for more options"
            
            step = 'menu'
            data = {}
        
        elif message in ["❌ Cancel", "Cancel", "No", "Back"]:
            response = "❌ Booking cancelled.\n\n"
            response += "Type *Menu* to return to main menu\n"
            response += "or *New Booking* to start again"
            step = 'menu'
            data = {}
        
        else:
            response = "Please select an option:\n"
            response += "• *Confirm Now* - To confirm your booking\n"
            response += "• *Cancel* - To cancel and go back"
    
    # Confirm with payment (≥ ₹1000)
    elif step == 'confirm_with_payment':
        if message in ["💳 Proceed to Payment", "Pay Now", "Payment", "Proceed"]:
            step = 'show_payment'
            response = ""
        
        elif message in ["❌ Cancel", "Cancel", "No", "Back"]:
            response = "❌ Booking cancelled.\n\n"
            response += "Type *Menu* to return to main menu\n"
            response += "or *New Booking* to start again"
            step = 'menu'
            data = {}
        
        else:
            response = "Please select an option:\n"
            response += "• *Proceed to Payment* - To make payment\n"
            response += "• *Cancel* - To cancel booking"
    
    # Show payment
    elif step == 'show_payment':
        if message in ["✅ I Have Paid", "Paid", "Done", "Completed"]:
            response = "📸 *Please upload your payment screenshot*\n\n"
            response += "Send the screenshot as an image here.\n"
            response += "Our team will verify and confirm within 1 hour.\n\n"
            response += "Type *Cancel* if you haven't paid yet"
            step = 'waiting_payment_screenshot'
        
        elif message in ["🔙 Back", "Back", "Cancel"]:
            advance = data.get('advance_required', 0)
            response = f"Going back to booking confirmation...\n\n"
            response += f"Advance required: ₹{advance}"
            step = 'confirm_with_payment'
        
        else:
            response = "Please select an option:\n"
            response += "• *I Have Paid* - If you've completed payment\n"
            response += "• *Back* - To go back"
    
    # Waiting for screenshot
    elif step == 'waiting_payment_screenshot':
        if message.lower() in ['cancel', 'back']:
            response = "Payment cancelled. Returning to payment page..."
            return 'show_payment', data, response
        else:
            response = "⚠️ *Please send the payment screenshot as an IMAGE*\n\n"
            response += "Don't send text. Upload the screenshot.\n\n"
            response += "Type *Cancel* to go back"
    
    # My Bookings
    elif "My Bookings" in message:
        bookings = db.get_bookings(phone=phone)
        
        if bookings:
            response = "*📋 Your Bookings:*\n\n"
            for i, booking in enumerate(bookings[:5], 1):
                services = json.loads(booking['services'])
                service_names = [Config.SERVICES[s]['name'] for s in services]
                
                status_emoji = {
                    'confirmed': '✅',
                    'pending': '⏳',
                    'payment_pending': '💳',
                    'cancelled': '❌',
                    'rejected': '❌'
                }.get(booking['status'], '❓')
                
                response += f"*{i}. Booking #{booking['id']}* {status_emoji}\n"
                response += f"📅 {booking['date']} at {booking['time']}\n"
                response += f"💇 {', '.join(service_names)}\n"
                response += f"💰 ₹{booking['total']}\n"
                response += f"Status: {booking['status'].replace('_', ' ').title()}\n\n"
            
            if len(bookings) > 5:
                response += f"...and {len(bookings)-5} more\n\n"
        else:
            response = "📭 You don't have any bookings yet.\n\n"
            response += "Book your first appointment now!"
        
        response += "\nType *Menu* to go back"
        step = 'menu'
    
    # Contact
    elif "Contact Us" in message:
        response = f"*📞 Contact {Config.SALON_NAME}*\n\n"
        response += f"📍 *Address:*\n{Config.SALON_ADDRESS}\n\n"
        response += f"📱 *Phone:*\n{Config.SALON_PHONE}\n\n"
        response += f"💳 *UPI ID:*\n{Config.UPI_ID}\n\n"
        response += "*🕐 Working Hours:*\n"
        response += "Monday - Sunday\n"
        response += "10:00 AM - 8:00 PM\n\n"
        response += "Type *Menu* to go back"
        step = 'menu'
    
    # Default
    else:
        response = "❓ I didn't understand that.\n\n"
        response += "Type *Menu* to see all options\n"
        response += "or choose from:\n"
        response += "• *New Booking* - Book appointment\n"
        response += "• *My Bookings* - View bookings\n"
        response += "• *Contact Us* - Get contact info"
    
    return step, data, response

def handle_payment_screenshot(phone, media_id):
    """Handle payment screenshot upload"""
    user_session = db.get_session(phone)
    step = user_session['step']
    data = user_session['data']
    
    if step == 'waiting_payment_screenshot':
        filename = f"payment_{phone}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        downloaded = whatsapp.download_media(media_id, save_path)
        
        if downloaded:
            booking_id = db.save_booking(
                phone=phone,
                name=data['name'],
                services=data['services'],
                date=data['date'],
                time=data['time'],
                total=data['total'],
                advance_required=data.get('advance_required', 0),
                status='payment_pending'
            )
            
            db.update_booking(booking_id, payment_screenshot=filename)
            
            response = "✅ *Payment Screenshot Received!*\n\n"
            response += f"*Booking ID:* #{booking_id}\n\n"
            response += "🔍 *Under Review*\n"
            response += "Our team will verify your payment and confirm within *1 hour*.\n\n"
            response += "You'll receive a confirmation message once approved. 🎉\n\n"
            response += "Type *Menu* for more options"
            
            whatsapp.send_message(phone, response)
            
            db.save_session(phone, 'menu', {})
        else:
            whatsapp.send_message(phone, "❌ Failed to receive image. Please try uploading again.")

def send_bot_response(phone, step, data, text_response):
    """Send appropriate response based on step"""
    
    if step == 'menu':
        buttons = ["📅 New Booking", "📋 My Bookings", "📞 Contact Us"]
        whatsapp.send_interactive_buttons(phone, text_response, buttons)
    
    elif step == 'select_date':
        dates = get_next_7_days()
        sections = [{
            "title": "Available Dates",
            "rows": [{"id": d['value'], "title": d['label']} for d in dates]
        }]
        whatsapp.send_interactive_list(phone, text_response, "📅 Choose Date", sections)
    
    elif step == 'confirm_without_payment':
        whatsapp.send_interactive_buttons(phone, text_response, ["✅ Confirm Now", "❌ Cancel"])
    
    elif step == 'confirm_with_payment':
        whatsapp.send_interactive_buttons(phone, text_response, ["💳 Proceed to Payment", "❌ Cancel"])
    
    elif step == 'show_payment':
        advance = data.get('advance_required', 0)
        caption = f"*💳 Payment Required*\n\n"
        caption += f"*Amount:* ₹{advance}\n"
        caption += f"*UPI ID:* {Config.UPI_ID}\n\n"
        caption += "📱 Scan the QR code above to pay.\n\n"
        caption += "After payment, click *I Have Paid* button"
        
        whatsapp.send_image(phone, Config.QR_CODE_PATH, caption)
        whatsapp.send_interactive_buttons(phone, "Have you completed the payment?", ["✅ I Have Paid", "🔙 Back"])
    
    else:
        if text_response:
            whatsapp.send_message(phone, text_response)

# =================== ADMIN PANEL ===================

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        if password == Config.ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid password!', 'error')
    
    return render_template('admin.html', page='login')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    bookings = db.get_bookings()
    
    stats = {
        'total': len(bookings),
        'confirmed': len([b for b in bookings if b['status'] == 'confirmed']),
        'pending': len([b for b in bookings if b['status'] == 'payment_pending']),
        'cancelled': len([b for b in bookings if b['status'] in ['cancelled', 'rejected']])
    }
    
    return render_template('admin.html', 
                         page='dashboard', 
                         bookings=bookings, 
                         stats=stats,
                         services=Config.SERVICES)

@app.route('/admin/booking/<int:booking_id>/approve', methods=['POST'])
def approve_booking(booking_id):
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    booking = db.get_booking(booking_id)
    if booking:
        db.update_booking(booking_id, status='confirmed')
        
        services = json.loads(booking['services'])
        service_names = [Config.SERVICES[s]['name'] for s in services]
        
        message = "🎉 *Payment Verified - Booking Confirmed!*\n\n"
        message += f"*Booking ID:* #{booking_id}\n"
        message += f"*Name:* {booking['name']}\n"
        message += f"*Date:* {booking['date']}\n"
        message += f"*Time:* {booking['time']}\n"
        message += f"*Services:* {', '.join(service_names)}\n"
        message += f"*Total:* ₹{booking['total']}\n\n"
        message += f"✨ See you at *{Config.SALON_NAME}*!\n\n"
        message += f"📍 {Config.SALON_ADDRESS}\n"
        message += f"📞 {Config.SALON_PHONE}"
        
        whatsapp.send_message(booking['phone'], message)
        
        flash(f'Booking #{booking_id} approved and customer notified!', 'success')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/booking/<int:booking_id>/reject', methods=['POST'])
def reject_booking(booking_id):
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    notes = request.form.get('notes', 'Payment verification failed')
    booking = db.get_booking(booking_id)
    
    if booking:
        db.update_booking(booking_id, status='rejected', admin_notes=notes)
        
        message = "❌ *Booking Payment Rejected*\n\n"
        message += f"*Booking ID:* #{booking_id}\n"
        message += f"*Reason:* {notes}\n\n"
        message += "Please contact us for clarification:\n"
        message += f"📞 {Config.SALON_PHONE}\n\n"
        message += "You can rebook by typing *New Booking*"
        
        whatsapp.send_message(booking['phone'], message)
        
        flash(f'Booking #{booking_id} rejected!', 'warning')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# =================== HEALTH CHECK ===================

@app.route('/')
def home():
    return jsonify({
        'status': 'active',
        'app': Config.SALON_NAME,
        'webhook': '/webhook',
        'admin': '/admin'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
