✅ README.md (Webhook Deployment Guide):

# BD Translate Bot (Webhook Version)

একটি টেলিগ্রাম গ্রুপ অনুবাদ বট যা Flask + Webhook ব্যবহার করে কাজ করে।

---

## 🚀 Deploy করার নিয়ম (Render):

1. **GitHub Repo তৈরি করুন এবং সব ফাইল আপলোড করুন**
2. **Render.com-এ নতুন Web Service তৈরি করুন**
   - Python environment সিলেক্ট করুন
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
3. **Environment Variables সেট করুন:**
   - `TELEGRAM_BOT_TOKEN` → আপনার বট টোকেন
   - `WEBHOOK_URL` → Render থেকে পাওয়া public URL (e.g. `https://xyz.onrender.com`)
   - `WEBHOOK_SECRET_PATH` → একটি গোপন keyword (যেমন: `webhook123`)
4. **BotFather-এ webhook reset না করলেও চলবে — কোড থেকেই সেট হবে।**
5. **Bot কে গ্রুপে অ্যাড করে Admin দিন**

---

## 🧪 Local Test:

```bash
export TELEGRAM_BOT_TOKEN=your_token_here
export WEBHOOK_URL=https://yourdomain.com
export WEBHOOK_SECRET_PATH=webhook123
python main.py


---

💬 Developer

ডেভেলপার: @nknoman22

চ্যানেল: @BD_Translate

