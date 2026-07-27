# 🤖 SahuPanel Telegram Payment Bot

Payment verification के लिए Telegram bot जो automatically customers के payments को verify करता है!

## ✨ Features

✅ **Automatic Payment Verification**
- Customer screenshot भेजता है
- Bot automatically check करता है
- Admin को notify करता है
- Order automatically approve हो जाता है

✅ **Admin Dashboard**
- सभी pending payments देख सकते हो
- One-click approve/reject
- Payment history

✅ **Customer Notifications**
- Real-time status updates
- Order confirmation
- Payment receipt

---

## 🚀 Installation

### Step 1: Python Install करो
```bash
python --version  # Python 3.8+ होना चाहिए
```

### Step 2: Dependencies Install करो
```bash
pip install -r requirements.txt
```

### Step 3: Bot Token Setup करो
`bot.py` में यह line खोजो:
```python
TELEGRAM_BOT_TOKEN = "8775002469:AAH-19Ww9lD19Je-8pT0rp_RyKtDI52eP_A"
ADMIN_ID = 93372553
```

✅ पहले से set है! (तुम्हारा token और ID)

---

## 🎯 Bot को Run करो

```bash
python bot.py
```

Output:
```
🤖 SahuPanel Bot शुरू हो रहा है...
✅ Bot ready! Type /start करो Telegram में...
```

---

## 📱 Telegram पर कैसे Use करें

### 1. Bot को Search करो
- Telegram खोलो
- `@SahuPanel_Bot` search करो
- या यह link खोलो: https://t.me/SahuPanel_Bot

### 2. /start करो
```
/start
```

Bot तुम्हें instructions देगा!

### 3. Payment Screenshot भेजो
- Screenshot लो
- Bot को भेजो
- Format में details दो:
```
Order ID: ABC123
Amount: ₹500
Phone: 9876543210
```

### 4. Bot Verify करेगा
```
✅ Screenshot received!
⏳ Admin verify कर रहे हैं...
✅ Order Approved!
```

---

## 🎛️ Admin Commands

**Admin केवल तुम हो (@93372553)**

### Approve करो
```
/approve_ABC123
```

### Reject करो
```
/reject_ABC123
```

### Status देखो
```
/status
```

---

## 📊 Bot का काम करने का तरीका

```
Customer                    Bot                    Admin (तुम)
   |                         |                         |
   |--/start---------------->|                         |
   |<----Instructions--------|                         |
   |                         |                         |
   |--Screenshot------------>|                         |
   |                         |--Notification-------->|
   |                         |                     (देख)
   |                         |                         |
   |                         |<---/approve_123-----|
   |                         |                         |
   |<---✅ Approved---------|                         |
   |                         |                         |
```

---

## 🔧 Configuration

`bot.py` में ये बदल सकते हो:

```python
# तुम्हारा Telegram ID (जहाँ notifications जाएंगे)
ADMIN_ID = 93372553

# तुम्हारा UPI ID
UPI_ID = "7250728059@ybl"

# Bot Token (पहले से set है)
TELEGRAM_BOT_TOKEN = "8775002469:AAH-19Ww9lD19Je-8pT0rp_RyKtDI52eP_A"
```

---

## 🐛 Troubleshooting

### Problem: Bot काम नहीं कर रहा
```bash
# Dependencies reinstall करो
pip install -r requirements.txt --force-reinstall

# Bot फिर से start करो
python bot.py
```

### Problem: Notifications नहीं आ रहे
- अपना Telegram User ID verify करो
- @userinfobot को message भेजो
- ID copy करो
- `bot.py` में update करो

### Problem: Screenshot Save नहीं हो रहा
- `payments/` folder बना (directory)
- या code में path change करो

---

## 📈 Future Improvements

- [ ] OCR से automatic UPI verification
- [ ] Database integration (MongoDB/SQL)
- [ ] Payment history report
- [ ] Multi-language support
- [ ] WhatsApp integration
- [ ] Email notifications

---

## 💡 Tips

1. **Bot को 24/7 चलाने के लिए:**
   - AWS Lambda का use करो
   - या Heroku पर deploy करो
   - या VPS किराए पर लो

2. **Security के लिए:**
   - Bot Token को `.env` file में रखो
   - Database use करो payments store के लिए

3. **Better UX के लिए:**
   - Website से direct Telegram link दो
   - QR code बना दो bot link का

---

## 📞 Support

अगर कोई problem हो:
- Instagram: @notx_ayus
- WhatsApp: +91 7250728059
- Telegram: @SahuPanel_Bot

---

## 📄 License

Free to use! Enjoy! 🎉

---

**बनाया गया:** July 2026  
**Updated:** July 27, 2026  
**Version:** 1.0.0
