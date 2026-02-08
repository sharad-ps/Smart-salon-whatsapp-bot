# 💇 Smart Salon WhatsApp Bot

Complete WhatsApp booking bot for salon businesses using Meta WhatsApp Business API.

---

## 🎯 DEPLOYMENT GUIDE (Step-by-Step)

### **STEP 1: Meta WhatsApp Business Setup** 🚀

#### 1.1 Create Meta Developer Account
1. Go to: https://developers.facebook.com
2. Sign up / Login with Facebook account
3. Click "My Apps" → "Create App"
4. Select "Business" → Continue
5. Fill app details and create

#### 1.2 Add WhatsApp Product
1. In your app dashboard, click "Add Product"
2. Find "WhatsApp" → Click "Set Up"
3. You'll see WhatsApp Business API setup page

#### 1.3 Get Credentials
1. **Phone Number ID**: 
   - Go to WhatsApp → Getting Started
   - Copy the "Phone number ID" (looks like: 123456789012345)
   
2. **Access Token** (Temporary - 24 hours):
   - Copy the temporary token shown on same page
   - Later we'll get permanent token

3. **Permanent Access Token** (Important!):
   - Go to Settings → Basic
   - Note your "App ID" and "App Secret"
   - Go to Business Settings (https://business.facebook.com)
   - System Users → Add → Create system user
   - Assign assets → Select your app → Give full control
   - Generate token → Select WhatsApp permissions
   - **SAVE THIS TOKEN** - Yahi permanent hai!

#### 1.4 Add Test Number (For Testing)
1. In WhatsApp → Getting Started
2. Add your number in "To" field
3. Send test message to verify

---

### **STEP 2: Deployment on Render** ☁️

#### 2.1 Upload Code to GitHub
```bash
# If you don't have Git installed:
# Windows: Download from git-scm.com
# Mac: Install via Homebrew
# Linux: sudo apt install git

# Initialize Git (in project folder)
git init
git add .
git commit -m "Initial commit"

# Create new repo on GitHub.com
# Then connect and push:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/salon-bot.git
git push -u origin main
```

#### 2.2 Deploy on Render.com
1. **Sign Up**: https://render.com (use GitHub account)

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Select your salon-bot repo

3. **Configure Service**:
   ```
   Name: salon-whatsapp-bot
   Region: Singapore (or closest to India)
   Branch: main
   Root Directory: (leave blank)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   Instance Type: Free
   ```

4. **Add Environment Variables** (Very Important!):
   - Click "Environment" tab
   - Add these variables:
   
   ```
   SECRET_KEY = salon_secret_key_random_12345
   WHATSAPP_TOKEN = EAAxxxxxxxxxxxxx (your permanent token)
   WHATSAPP_PHONE_ID = 123456789012345 (from Meta dashboard)
   VERIFY_TOKEN = salon_verify_token_123
   ADMIN_PASSWORD = YourStrongPassword123
   UPI_ID = yourname@paytm (or @ybl, @okaxis, etc.)
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Note your app URL: https://your-app-name.onrender.com

---

### **STEP 3: Configure WhatsApp Webhook** 🔗

#### 3.1 Set Webhook URL
1. Go to Meta Developers → Your App → WhatsApp → Configuration
2. Click "Edit" in Webhook section
3. Enter:
   ```
   Callback URL: https://your-app-name.onrender.com/webhook
   Verify Token: salon_verify_token_123
   ```
4. Click "Verify and Save"

#### 3.2 Subscribe to Messages
1. In same page, find "Webhook fields"
2. Click "Manage"
3. Subscribe to: **messages**
4. Save

---

### **STEP 4: Upload UPI QR Code** 💳

#### 4.1 Generate QR Code
1. Open any UPI app (Paytm, PhonePe, GPay)
2. Go to "Receive Money" / "QR Code"
3. Download / Screenshot your QR code

#### 4.2 Upload to Project
**Option A - Via GitHub:**
1. Create folder: `static/` in your repo
2. Upload QR code as: `static/qr_code.jpg`
3. Commit and push
4. Render will auto-deploy

**Option B - Manual:**
1. In Render dashboard → Shell
2. Upload QR code to `/opt/render/project/src/static/`

---

### **STEP 5: Test Your Bot** ✅

#### 5.1 Send Test Message
1. Open WhatsApp
2. Send message to your WhatsApp Business number
3. Type: "Hi" or "Hello"
4. Bot should respond with menu!

#### 5.2 Test Booking Flow
1. Click "📅 New Booking"
2. Enter name (first time)
3. Select services (e.g., "1,3")
4. Choose date from list
5. Select time slot
6. Complete booking

#### 5.3 Test Admin Panel
1. Go to: https://your-app-name.onrender.com/admin
2. Login with your ADMIN_PASSWORD
3. Check bookings, approve payments

---

## 🛠️ TROUBLESHOOTING

### Bot Not Responding?
```
✅ Check: Webhook is configured in Meta Dashboard
✅ Check: WHATSAPP_TOKEN is permanent token (not temporary)
✅ Check: WHATSAPP_PHONE_ID is correct
✅ Check: Render app is running (check Logs)
✅ Check: Message is sent to correct WhatsApp number
```

### Webhook Verification Failed?
```
✅ Check: VERIFY_TOKEN in .env matches Meta configuration
✅ Check: Render app is deployed and running
✅ Check: URL is correct (https://your-app.onrender.com/webhook)
```

### Admin Panel Not Working?
```
✅ Check: ADMIN_PASSWORD is set in environment variables
✅ Check: Accessing correct URL: /admin
✅ Try: Clear browser cache
```

### Payment QR Not Showing?
```
✅ Check: QR code uploaded to static/qr_code.jpg
✅ Check: File size < 5MB
✅ Check: File format is .jpg or .jpeg
```

---

## 📱 Features

### For Customers:
- ✅ Book appointments via WhatsApp
- ✅ Select multiple services
- ✅ Choose date and time
- ✅ Auto-confirm for bookings < ₹1000
- ✅ UPI payment for bookings ≥ ₹1000
- ✅ Upload payment screenshot
- ✅ View booking history

### For Salon Owner:
- ✅ Admin panel to manage bookings
- ✅ Approve/reject payments
- ✅ View payment screenshots
- ✅ Real-time booking stats
- ✅ Customer contact details

---

## 💡 CUSTOMIZATION

### Change Services
Edit `config.py`:
```python
SERVICES = {
    "1": {"name": "Haircut (Men)", "price": 150, "duration": "30 min"},
    "2": {"name": "Your Service", "price": 500, "duration": "60 min"},
    # Add more...
}
```

### Change Time Slots
Edit `config.py`:
```python
TIME_SLOTS = [
    "10:00 AM", "11:00 AM", "12:00 PM",
    # Add your preferred slots
]
```

### Change Payment Threshold
Edit `config.py`:
```python
ADVANCE_PAYMENT_THRESHOLD = 1000  # Change amount
ADVANCE_PERCENTAGE = 0.5  # 50% advance
```

### Update Salon Details
Edit `config.py`:
```python
SALON_NAME = "Your Salon Name"
SALON_ADDRESS = "Your Address"
SALON_PHONE = "+91 9876543210"
```

---

## 📊 Database Schema

### Tables:
1. **users** - Customer information
2. **bookings** - All booking records
3. **sessions** - Active chat sessions

### Backup Database:
```bash
# Download salon.db file from Render
# Keep it safe for backup
```

---

## 🔐 Security Tips

1. **Never share** your WHATSAPP_TOKEN publicly
2. **Use strong** ADMIN_PASSWORD
3. **Don't commit** .env file to GitHub
4. **Enable** two-factor authentication on Meta account
5. **Regularly check** Render logs for suspicious activity

---

## 💰 Cost Breakdown

### Meta WhatsApp:
- First 1000 messages/month: **FREE**
- After: Very cheap (₹0.30 per conversation)

### Render Hosting:
- **Free Plan**: 
  - Good for 100-200 bookings/month
  - App sleeps after 15 mins inactivity
  - Wakes up when message received (10-15 sec delay)

- **Paid Plan** ($7/month):
  - Always active
  - No delays
  - Good for >500 bookings/month

---

## 📞 Support

### Resources:
- Meta Developers Docs: https://developers.facebook.com/docs/whatsapp
- Render Docs: https://render.com/docs
- Python-dotenv: https://pypi.org/project/python-dotenv/

### Common Issues:
1. **Render free plan**: App sleeps - first message delayed
2. **Token expired**: Get permanent token, not temporary
3. **QR not showing**: Check file path and format

---

## 🎉 Success Checklist

Before going live:
- [ ] Meta WhatsApp Business approved
- [ ] Permanent access token obtained
- [ ] Code deployed on Render
- [ ] Webhook verified and working
- [ ] QR code uploaded
- [ ] Admin panel accessible
- [ ] Test booking completed
- [ ] Payment flow tested
- [ ] All environment variables set
- [ ] Backup plan ready

---

## 🚀 Next Steps

1. **Get verified**: Apply for Meta Business Verification
2. **Add features**: 
   - Send reminder messages
   - Add cancellation feature
   - Integrate Google Calendar
   - Add staff assignment
3. **Marketing**: Promote WhatsApp number to customers
4. **Monitor**: Check admin panel daily

---

## 📝 License
MIT License - Free to use for your business!

---

**Made with ❤️ for Salon Businesses**

Need help? Check the troubleshooting section or Meta documentation.

**Important**: Test thoroughly before going live! 🧪
