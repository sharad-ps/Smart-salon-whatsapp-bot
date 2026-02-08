# 🇮🇳 WhatsApp Salon Bot - Complete Setup Guide (हिंदी में)

## 📱 यह Bot क्या करता है?

यह एक WhatsApp Chatbot है जो आपके Salon के लिए:
- ✅ Automatic booking लेता है
- ✅ Customer का नाम, service, date, time लेता है
- ✅ Payment QR code भेजता है
- ✅ Payment screenshot verify करता है
- ✅ Admin panel में सब bookings दिखाता है

---

## 🎯 STEP-BY-STEP SETUP (शुरू से अंत तक)

---

### **STEP 1: Meta (Facebook) Account Setup**

#### 1.1 Developer Account बनाएं
1. यहाँ जाएं: https://developers.facebook.com
2. अपने Facebook account से login करें
3. "My Apps" → "Create App" पर क्लिक करें
4. "Business" select करें → Continue
5. कोई भी नाम दें (जैसे "Salon Bot") → Create

#### 1.2 WhatsApp Add करें
1. Dashboard में "Add Product" पर क्लिक करें
2. "WhatsApp" ढूंढें → "Set Up" पर क्लिक करें
3. अब आपको WhatsApp setup page दिखेगा

#### 1.3 Important IDs Copy करें

**A) Phone Number ID लें:**
```
WhatsApp → Getting Started में जाएं
"Phone number ID" दिखेगा (जैसे: 123456789012345)
इसे कहीं save करें! 📝
```

**B) Temporary Token लें:**
```
Same page पर "Temporary access token" दिखेगा
यह 24 घंटे के लिए होता है
बाद में permanent लेंगे
```

**C) Permanent Token बनाएं (बहुत जरूरी!):**
```
यह थोड़ा tricky है, ध्यान से follow करें:

1. Meta Business Suite खोलें: https://business.facebook.com
2. Settings (⚙️) → Users → System Users पर जाएं
3. "Add" button → "Create System User" क्लिक करें
4. नाम दें (जैसे "Salon Bot User") → Admin role select करें
5. बनने के बाद, उस user पर क्लिक करें
6. "Add Assets" → "Apps" select करें
7. अपना app select करें → "Full control" दें
8. अब "Generate New Token" पर क्लिक करें
9. अपना App select करें
10. Permissions में ये सब select करें:
    ✅ whatsapp_business_messaging
    ✅ whatsapp_business_management
11. "Generate Token" पर क्लिक करें
12. ⚠️ TOKEN COPY करके safe जगह save करें! यह दोबारा नहीं मिलेगा!
```

#### 1.4 Test Number Add करें
```
WhatsApp → Getting Started
"To" field में अपना WhatsApp number डालें (+91xxxxxxxxxx)
"Send Message" से test करें
आपके WhatsApp पर message आना चाहिए
```

---

### **STEP 2: GitHub पर Code Upload करें**

#### 2.1 Git Install करें (अगर नहीं है)

**Windows:**
```
1. git-scm.com से download करें
2. Install करें (सब default settings)
```

**Mac:**
```
Terminal में: brew install git
```

**Linux:**
```
Terminal में: sudo apt install git
```

#### 2.2 GitHub Account बनाएं
```
1. github.com पर जाएं
2. Sign up करें (free account)
3. Email verify करें
```

#### 2.3 Repository बनाएं
```
1. GitHub पर login करें
2. "+" icon → "New repository" क्लिक करें
3. नाम दें: salon-whatsapp-bot
4. Public select करें
5. "Create repository" क्लिक करें
```

#### 2.4 Code Upload करें
```bash
# अपने project folder में जाएं (जहाँ सब files हैं)
# Terminal / Command Prompt खोलें वहीं से

# Git initialize करें
git init

# सब files add करें
git add .

# Commit करें
git commit -m "First commit"

# Branch बनाएं
git branch -M main

# GitHub से connect करें (अपना username डालें)
git remote add origin https://github.com/YOUR_USERNAME/salon-whatsapp-bot.git

# Upload करें
git push -u origin main

# अगर username/password मांगे:
# Username: आपका GitHub username
# Password: Personal Access Token (GitHub settings → Developer settings → PAT से बनाएं)
```

---

### **STEP 3: Render पर Deploy करें (Free Hosting)**

#### 3.1 Render Account बनाएं
```
1. render.com पर जाएं
2. "Get Started" या "Sign Up" पर क्लिक करें
3. GitHub से Sign up करें (easy!)
4. Render को GitHub access दें
```

#### 3.2 Web Service Create करें
```
1. Dashboard में "New +" button → "Web Service" क्लिक करें
2. अपनी GitHub repository (salon-whatsapp-bot) select करें
3. "Connect" पर क्लिक करें
```

#### 3.3 Settings भरें
```
ये exactly ऐसे भरें:

Name: salon-whatsapp-bot (या कोई भी)
Region: Singapore (India के सबसे पास)
Branch: main
Root Directory: (खाली छोड़ें)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Instance Type: Free
```

#### 3.4 Environment Variables Add करें (सबसे जरूरी!)
```
"Environment" tab पर जाएं
"Add Environment Variable" पर क्लिक करके ये सब add करें:

Key                    Value
---                    -----
SECRET_KEY            = salon_secret_123456789
WHATSAPP_TOKEN        = EAAxxxxxxxxx... (वो permanent token जो आपने save किया था)
WHATSAPP_PHONE_ID     = 123456789012345 (Meta से copy किया था)
VERIFY_TOKEN          = salon_verify_token_123
ADMIN_PASSWORD        = YourStrongPassword123 (अपना मजबूत password)
UPI_ID                = yourname@paytm (या @ybl, @okaxis, etc.)

⚠️ हर variable को carefully डालें! एक भी गलत हुआ तो काम नहीं करेगा!
```

#### 3.5 Deploy करें!
```
1. सब check करने के बाद "Create Web Service" पर क्लिक करें
2. 2-3 मिनट इंतज़ार करें
3. Logs में "Build successful" दिखेगा
4. ऊपर green dot आएगा "Live"
5. आपका URL मिलेगा: https://salon-whatsapp-bot-xyz.onrender.com
```

---

### **STEP 4: Webhook Setup करें (WhatsApp को बताएं कहाँ message भेजना है)**

#### 4.1 Webhook Configure करें
```
1. Meta Developers में जाएं (developers.facebook.com)
2. अपना App खोलें
3. WhatsApp → Configuration पर जाएं
4. Webhook section में "Edit" पर क्लिक करें
5. भरें:
   
   Callback URL: https://salon-whatsapp-bot-xyz.onrender.com/webhook
   (अपना Render URL डालें, /webhook ज़रूर लगाएं!)
   
   Verify Token: salon_verify_token_123
   (वही जो .env में डाला था)

6. "Verify and Save" पर क्लिक करें
7. ✅ Green tick आना चाहिए!
```

#### 4.2 Message Subscribe करें
```
Same page पर नीचे "Webhook fields" दिखेगा
"Manage" पर क्लिक करें
"messages" को ✅ check करें
Save करें
```

---

### **STEP 5: UPI QR Code Upload करें**

#### 5.1 QR Code बनाएं
```
1. अपनी UPI app खोलें (Paytm / PhonePe / GPay)
2. "Receive Money" या "QR Code" section में जाएं
3. अपना UPI QR code screenshot लें या download करें
4. Save as: qr_code.jpg (exactly यही नाम!)
```

#### 5.2 Upload करें
```
Method 1 - GitHub से (आसान):
1. अपनी GitHub repository खोलें
2. "static" folder बनाएं (अगर नहीं है)
3. QR code upload करें as "qr_code.jpg"
4. Commit changes
5. Render automatically deploy कर देगा!

Method 2 - Direct:
1. अपनी project folder में जाएं
2. static/ folder में qr_code.jpg डालें
3. फिर से git add, commit, push करें
```

---

### **STEP 6: Testing (सब कुछ Test करें!)**

#### 6.1 Bot को Message भेजें
```
1. WhatsApp खोलें
2. उस number पर message भेजें जो Meta में दिया था
3. Type करें: "Hi" या "Hello"
4. Bot को reply करना चाहिए menu के साथ!
```

**अगर reply नहीं आया?**
```
✅ Render logs check करें
✅ Webhook verify हुआ है check करें
✅ WHATSAPP_TOKEN सही है check करें
✅ 1-2 मिनट इंतज़ार करें (free plan में pehli baar slow hota hai)
```

#### 6.2 Booking Test करें
```
1. "📅 New Booking" पर क्लिक करें
2. अपना नाम enter करें
3. Service select करें (जैसे: 1,3)
4. Date select करें
5. Time slot choose करें
6. Confirmation check करें
```

#### 6.3 Payment Test करें
```
1. ₹1000+ की booking बनाएं
2. QR code आना चाहिए
3. कोई भी screenshot upload करें (test के लिए)
4. "Payment pending" status दिखना चाहिए
```

#### 6.4 Admin Panel Check करें
```
1. Browser में जाएं: https://your-app.onrender.com/admin
2. अपना ADMIN_PASSWORD डालें
3. Dashboard दिखना चाहिए
4. Test booking दिखनी चाहिए
5. "Approve" button try करें
6. WhatsApp पर confirmation message आना चाहिए
```

---

## 🔧 CUSTOMIZATION (अपने हिसाब से बदलें)

### Services बदलें
```python
# config.py file खोलें

SERVICES = {
    "1": {"name": "Haircut (Men)", "price": 150, "duration": "30 min"},
    "2": {"name": "Haircut (Women)", "price": 300, "duration": "45 min"},
    "3": {"name": "Facial", "price": 500, "duration": "60 min"},
    # अपनी services add करें यहाँ
}
```

### Time Slots बदलें
```python
# config.py में

TIME_SLOTS = [
    "09:00 AM", "10:00 AM", "11:00 AM",  # Morning
    "02:00 PM", "03:00 PM", "04:00 PM",  # Afternoon
    "06:00 PM", "07:00 PM", "08:00 PM"   # Evening
]
```

### Salon Details बदलें
```python
# config.py में

SALON_NAME = "आपके Salon का नाम"
SALON_ADDRESS = "आपका पता"
SALON_PHONE = "+91 9876543210"
```

### Payment Settings बदलें
```python
# config.py में

ADVANCE_PAYMENT_THRESHOLD = 500   # ₹500 से ज़्यादा पर advance
ADVANCE_PERCENTAGE = 0.3          # 30% advance (0.5 = 50%)
```

---

## ❌ COMMON PROBLEMS & SOLUTIONS

### 1. Bot Reply नहीं कर रहा
```
समस्या: Message भेजने पर कोई reply नहीं

Solutions:
✅ Render app "Live" है check करें (green dot)
✅ Logs में errors देखें (Render dashboard → Logs)
✅ Webhook properly configure है verify करें
✅ WHATSAPP_TOKEN correct है check करें
✅ Free plan है तो पहली बार 10-15 sec लग सकते हैं
```

### 2. Webhook Verify नहीं हो रहा
```
समस्या: "Webhook verification failed" error

Solutions:
✅ VERIFY_TOKEN बिलकुल same है (.env और Meta में)
✅ Render URL सही है (https:// से शुरू, /webhook से end)
✅ Render app deploy हो गया है confirm करें
```

### 3. Admin Panel नहीं खुल रहा
```
समस्या: /admin URL पर error या blank page

Solutions:
✅ URL check करें: https://your-app.onrender.com/admin
✅ ADMIN_PASSWORD सही है check करें
✅ Browser cache clear करें (Ctrl+Shift+Del)
✅ Incognito mode में try करें
```

### 4. QR Code नहीं दिख रहा
```
समस्या: Payment के time QR code send नहीं हो रहा

Solutions:
✅ static/qr_code.jpg exist करता है check करें
✅ File name बिलकुल correct है (lowercase, .jpg)
✅ File size 5MB से कम है
✅ Format JPG है (PNG convert करें अगर है)
```

### 5. Payment Screenshot Upload नहीं हो रहा
```
समस्या: Image send करने पर error

Solutions:
✅ static/uploads/ folder exist करता है
✅ Render में write permissions हैं check करें
✅ Image size check करें (5MB से कम)
✅ Logs देखें क्या error आ रहा है
```

---

## 💰 COST (खर्चा कितना आएगा?)

### Meta WhatsApp API:
```
✅ पहले 1000 conversations per month: FREE
✅ उसके बाद: ~₹0.30 per conversation
✅ छोटे salon के लिए mostly FREE!

Conversation = 24 hours का back-and-forth messaging
```

### Render Hosting:
```
FREE Plan:
✅ 750 hours per month (पूरे महीने के लिए काफी)
✅ 100GB bandwidth
✅ Limitation: 15 मिनट बाद sleep (पर message पर wake होगा)
✅ छोटे business के लिए perfect!

Paid Plan ($7/month):
✅ हमेशा active रहेगा
✅ No sleeping
✅ Fast response
✅ Busy salon के लिए better
```

### Total Monthly Cost:
```
Startup: ₹0 (100% FREE!)
Growing: ₹500-600/month (Render paid plan)
Established: ₹1000-1500/month (features add करने पर)
```

---

## 📈 NEXT STEPS (आगे क्या करें?)

### 1. Business Verification (जरूरी नहीं पर अच्छा है)
```
- Meta Business verification apply करें
- Green tick badge मिलेगा
- Customer trust बढ़ेगा
- Higher message limits
```

### 2. Marketing शुरू करें
```
- अपना WhatsApp number promote करें
- Visiting cards में print करें
- Instagram/Facebook पर share करें
- दुकान में QR code लगाएं
```

### 3. Monitor & Improve
```
- रोज़ admin panel check करें
- Customer feedback लें
- Services update करें
- Timings adjust करें
```

### 4. Extra Features Add करें
```
- Reminder messages (booking से 1 दिन पहले)
- Cancellation option
- Rating & Review system
- Multiple staff assignment
- Google Calendar integration
```

---

## 🆘 HELP & SUPPORT

### Documentation:
```
Meta WhatsApp Docs: developers.facebook.com/docs/whatsapp
Render Docs: render.com/docs
Python Flask: flask.palletsprojects.com
```

### Video Tutorials (YouTube):
```
Search for:
- "WhatsApp Business API setup"
- "Deploy Flask app on Render"
- "Meta webhook configuration"
```

### Community:
```
Stack Overflow: stackoverflow.com (technical doubts)
Reddit: r/webdev, r/flask (help & tips)
Meta Developer Community: developers.facebook.com/community
```

---

## ✅ FINAL CHECKLIST (Live जाने से पहले)

```
[ ] Meta Developer account बना लिया
[ ] WhatsApp Business API setup किया
[ ] Permanent Access Token मिल गया
[ ] GitHub पर code upload किया
[ ] Render पर deploy किया
[ ] सब Environment Variables सही हैं
[ ] Webhook verify हो गया
[ ] QR code upload किया
[ ] Test booking successfully हुई
[ ] Payment flow test किया
[ ] Admin panel accessible है
[ ] Logs में कोई error नहीं
[ ] Real customer से test किया
[ ] Backup plan ready है (database download)
```

---

## 🎉 CONGRATULATIONS!

अगर सब steps follow किए हैं तो अब आपका WhatsApp Bot **LIVE** है! 🚀

अब आप:
- ✅ WhatsApp पर bookings ले सकते हैं
- ✅ Automatic messages भेज सकते हैं
- ✅ Payments track कर सकते हैं
- ✅ Admin panel से manage कर सकते हैं

**All the best for your business! 💪**

---

## 📞 Quick Reference

```
Render Dashboard: render.com/dashboard
Meta Developers: developers.facebook.com
Admin Panel: https://your-app.onrender.com/admin
Webhook URL: https://your-app.onrender.com/webhook
GitHub Repo: github.com/YOUR_USERNAME/salon-whatsapp-bot
```

---

**कोई भी doubt हो तो:**
1. README.md फिर से पढ़ें
2. Logs check करें
3. Meta documentation देखें
4. Google/YouTube पर search करें

**Happy Coding! 🎉**
