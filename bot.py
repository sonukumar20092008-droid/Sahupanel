import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re
from datetime import datetime

# ===== CONFIG =====
TELEGRAM_BOT_TOKEN = "8775002469:AAH-19Ww9lD19Je-8pT0rp_RyKtDI52eP_A"
ADMIN_ID = 93372553
UPI_ID = "7250728059@ybl"  # तुम्हारा UPI ID

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== PAYMENT VERIFICATION LOGIC =====
def verify_payment(screenshot_path, upi_id, amount, user_phone):
    """
    यह function payment screenshot को verify करेगा
    अभी manual verification के लिए तैयार है
    Later में OCR add कर सकते हो
    """
    verification_data = {
        "status": "pending",
        "screenshot": screenshot_path,
        "upi_id": upi_id,
        "amount": amount,
        "phone": user_phone,
        "timestamp": datetime.now().isoformat()
    }
    return verification_data

# ===== BOT COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot शुरू करने के लिए"""
    user = update.effective_user
    message = f"""
🚀 **SahuPanel Payment Bot में स्वागत है!**

आप यहाँ अपने payment verification के लिए screenshot भेज सकते हो:

**कैसे करें:**
1. Payment का screenshot लो
2. यहाँ भेजो
3. Bot automatically verify करेगा ✅
4. Order approve हो जाएगा 🎉

**भेजते समय यह info दो:**
```
Order ID: ABC123
Amount: ₹500
Phone: 9876543210
```

किसी समस्या के लिए: @notx_ayus
"""
    await update.message.reply_text(message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """
📋 **Payment Bot Help**

**Commands:**
/start - Bot शुरू करो
/help - यह message
/status - तुम्हारे orders की status

**Screenshot भेजते समय लिखो:**
```
Order ID: [Order का नाम]
Amount: ₹[कितना]
Phone: [तुम्हारा नंबर]
```

फिर screenshot attach करो!
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Photo receive करने के लिए"""
    user = update.effective_user
    
    # Photo को save करो
    photo_file = await update.message.photo[-1].get_file()
    file_path = f"payments/{user.id}_{datetime.now().timestamp()}.jpg"
    
    try:
        await photo_file.download_to_drive(file_path)
        
        # User को confirmation दो
        await update.message.reply_text(
            "📸 Screenshot received! ✅\n\n"
            "अब इस format में payment details भेजो:\n"
            "```\n"
            "Order ID: ABC123\n"
            "Amount: ₹500\n"
            "Phone: 9876543210\n"
            "```",
            parse_mode='Markdown'
        )
        
        # Admin को notify करो
        admin_message = (
            f"🔔 **नया Payment Verification आया!**\n\n"
            f"👤 User: {user.first_name} (@{user.username})\n"
            f"🆔 User ID: {user.id}\n"
            f"📸 Screenshot: [देखो]\n"
            f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"✅ Verify करने के लिए reply करो: approve\n"
            f"❌ Reject करने के लिए reply करो: reject"
        )
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_message,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error handling photo: {e}")
        await update.message.reply_text(
            "❌ Error! Screenshot save नहीं हो सकी।\n\n"
            f"Error: {str(e)}"
        )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Text message handle करो"""
    user = update.effective_user
    text = update.message.text
    
    # अगर payment details हैं
    if "Order ID" in text or "Amount" in text:
        # Extract करो
        order_match = re.search(r'Order ID:\s*(\w+)', text)
        amount_match = re.search(r'Amount:\s*₹(\d+)', text)
        phone_match = re.search(r'Phone:\s*(\d+)', text)
        
        order_id = order_match.group(1) if order_match else "N/A"
        amount = amount_match.group(1) if amount_match else "N/A"
        phone = phone_match.group(1) if phone_match else "N/A"
        
        # User को confirmation
        await update.message.reply_text(
            f"✅ **Payment Details Received!**\n\n"
            f"📦 Order ID: `{order_id}`\n"
            f"💰 Amount: ₹`{amount}`\n"
            f"📱 Phone: `{phone}`\n\n"
            f"⏳ Processing... Admin will verify soon! 🔍"
        )
        
        # Admin को भेजो
        admin_msg = (
            f"💳 **Payment Verification Request**\n\n"
            f"👤 User: {user.first_name}\n"
            f"📦 Order ID: `{order_id}`\n"
            f"💰 Amount: ₹`{amount}`\n"
            f"📱 Phone: `{phone}`\n\n"
            f"✅ /approve_{order_id}\n"
            f"❌ /reject_{order_id}"
        )
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_msg,
            parse_mode='Markdown'
        )

async def approve_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Payment को approve करो (Admin only)"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ तुम्हें permission नहीं है!")
        return
    
    order_id = context.args[0] if context.args else "Unknown"
    
    await update.message.reply_text(
        f"✅ **Order {order_id} APPROVED!**\n\n"
        f"Customer को notify किया जा रहा है... 📨"
    )
    
    # यहाँ database update करो
    logger.info(f"Order {order_id} approved by admin")

async def reject_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Payment को reject करो (Admin only)"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ तुम्हें permission नहीं है!")
        return
    
    order_id = context.args[0] if context.args else "Unknown"
    
    await update.message.reply_text(
        f"❌ **Order {order_id} REJECTED!**\n\n"
        f"Customer को notify किया जा रहा है... 📨"
    )
    
    logger.info(f"Order {order_id} rejected by admin")

# ===== MAIN BOT =====
def main():
    """Bot को शुरू करो"""
    print("🤖 SahuPanel Bot शुरू हो रहा है...")
    
    # Application बनाओ
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Handlers जोड़ो
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Bot को run करो
    print("✅ Bot ready! Type /start करो Telegram में...")
    app.run_polling()

if __name__ == '__main__':
    main()
