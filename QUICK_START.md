# ⚡ QUICK START GUIDE - 30 Minutes Setup

## 🎯 Prerequisites (पहले ये तैयार रखें)

```
✅ Facebook/Meta account
✅ GitHub account  
✅ Phone number for WhatsApp Business
✅ UPI ID for payments
✅ QR code image (from UPI app)
```

---

## 🚀 5-STEP DEPLOYMENT

### STEP 1: Meta Setup (10 mins)
```
1. Go to: developers.facebook.com
2. Create App → Business type
3. Add WhatsApp product
4. Copy Phone Number ID: ________________
5. Generate Permanent Token (Business Settings → System Users)
6. Save Token: ________________
```

### STEP 2: Upload to GitHub (5 mins)
```bash
# In project folder
git init
git add .
git commit -m "Initial commit"
git branch -M main

# Create repo on github.com, then:
git remote add origin https://github.com/USERNAME/salon-bot.git
git push -u origin main
```

### STEP 3: Deploy on Render (5 mins)
```
1. render.com → Sign up with GitHub
2. New Web Service → Connect repo
3. Settings:
   Build: pip install -r requirements.txt
   Start: gunicorn app:app
4. Add Environment Variables (see below)
5. Create Web Service
```

### STEP 4: Configure Webhook (3 mins)
```
Meta → WhatsApp → Configuration → Edit Webhook:

URL: https://YOUR-APP.onrender.com/webhook
Token: salon_verify_token_123
Subscribe to: messages
```

### STEP 5: Upload QR Code (2 mins)
```
GitHub repo → static/qr_code.jpg → Upload
Commit → Render auto-deploys
```

---

## 🔑 ENVIRONMENT VARIABLES (Copy-Paste Ready)

```env
SECRET_KEY=salon_secret_random_12345
WHATSAPP_TOKEN=YOUR_PERMANENT_TOKEN_HERE
WHATSAPP_PHONE_ID=YOUR_PHONE_ID_HERE
VERIFY_TOKEN=salon_verify_token_123
ADMIN_PASSWORD=ChangeMe123
UPI_ID=yourname@paytm
```

**⚠️ Replace:**
- `YOUR_PERMANENT_TOKEN_HERE` with token from Meta
- `YOUR_PHONE_ID_HERE` with Phone Number ID
- `ChangeMe123` with strong password
- `yourname@paytm` with your UPI ID

---

## ✅ VERIFICATION CHECKLIST

```
Test 1: Webhook
Meta → Configuration → Webhook shows ✅ green

Test 2: Bot Response
WhatsApp: "Hi" → Bot replies with menu

Test 3: Booking
Click "New Booking" → Complete flow

Test 4: Admin Panel
https://YOUR-APP.onrender.com/admin → Login works

Test 5: Payment
₹1000+ booking → QR code appears
```

---

## 🔧 CUSTOMIZATION (Optional)

Edit `config.py`:

```python
# Your Business Details
SALON_NAME = "Your Salon Name"
SALON_ADDRESS = "Your Address"
SALON_PHONE = "+91 9876543210"

# Your Services
SERVICES = {
    "1": {"name": "Service Name", "price": 200, "duration": "30 min"},
    # Add more...
}

# Time Slots
TIME_SLOTS = ["10:00 AM", "11:00 AM", "12:00 PM", ...]

# Payment Settings
ADVANCE_PAYMENT_THRESHOLD = 1000  # Amount for advance payment
```

---

## ❌ TROUBLESHOOTING

**Bot not replying?**
```
→ Check Render logs
→ Verify webhook status (Meta dashboard)
→ Wait 1-2 mins (free plan wakes from sleep)
```

**Webhook failed?**
```
→ Check VERIFY_TOKEN matches in .env and Meta
→ Ensure Render app is deployed (green dot)
```

**Admin not opening?**
```
→ Clear browser cache
→ Check ADMIN_PASSWORD in environment variables
```

---

## 📱 URLs

```
Webhook:    https://YOUR-APP.onrender.com/webhook
Admin:      https://YOUR-APP.onrender.com/admin
Health:     https://YOUR-APP.onrender.com/health
```

---

## 🎉 DONE!

Your bot is now **LIVE**! 🚀

Test it:
1. Send "Hi" on WhatsApp
2. Book an appointment
3. Check admin panel

---

## 📚 FULL GUIDES

- Complete Setup: `README.md`
- Hindi Guide: `DEPLOYMENT_GUIDE_HINDI.md`
- Customization: `config.py`

---

**Time Taken:** ~30 minutes
**Cost:** ₹0 (100% Free!)
**Support:** Check README.md troubleshooting section

**Good luck! 💪**
