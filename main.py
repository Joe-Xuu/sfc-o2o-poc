import os
import sys
import json
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv

# LINE SDK
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Google Sheets SDK
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables
load_dotenv()

app = FastAPI()

# ================= config =================
# 1. LINE Config
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 2. Google Sheets Config
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
SHEET_URL = os.getenv("GOOGLE_SHEET_URL")
OVERDUE_DAYS = int(os.getenv("OVERDUE_DAYS", 3))

# connect to Google Sheets
def get_worksheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # read local service_account.json
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
    client = gspread.authorize(creds)
    return client.open_by_url(SHEET_URL).sheet1

# ================= business process logic =================

# 1. LINE Webhook (handle user messages)
@app.post("/callback")
async def callback(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    body_str = body.decode('utf-8')

    try:
        handler.handle(body_str, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    user_id = event.source.user_id
    
    if msg.startswith("borrow"):
        item_id = msg.replace("borrow", "").strip()
        
        try:
            sheet = get_worksheet()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 写入表格: [User ID, Item ID, Date, Status]
            sheet.append_row([user_id, item_id, timestamp, "BORROWED"])
            
            reply = f"✅ register succeeded！\nitem: {item_id}\ntime: {timestamp}\nRemember to return it in {OVERDUE_DAYS} days!"
        except Exception as e:
            print(e)
            reply = "❌ System error, unable to connect to the database."

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

# 2. Days Later Reminder
# This endpoint does not run automatically; you need to access it once a day (or use UptimeRobot to access it regularly)
@app.get("/api/cron/check_overdue")
def check_overdue_items():
    sheet = get_worksheet()
    rows = sheet.get_all_records() # Assuming the first row is headers: UserID, ItemID, Date, Status
    
    # sheet's first row must have English headers: UserID, ItemID, Date, Status
    # Otherwise, get_all_records will raise an error
    
    reminded_count = 0
    now = datetime.now()
    
    for i, row in enumerate(rows):
        # row keys must exactly match the headers in your sheet's first row
        status = row.get("Status")
        borrow_date_str = row.get("Date")
        user_id = row.get("UserID")
        item_id = row.get("ItemID")

        if status == "BORROWED" and borrow_date_str:
            try:
                borrow_date = datetime.strptime(borrow_date_str, "%Y-%m-%d %H:%M:%S")
                # 计算借了多久
                delta = now - borrow_date
                
                if delta.days >= OVERDUE_DAYS:
                    # Send overdue reminder
                    push_text = f"⚠️ 【Overdue Reminder】\nThe item {item_id} you borrowed has been overdue for more than {OVERDUE_DAYS} days.\nPlease return it as soon as possible!"
                    try:
                        line_bot_api.push_message(user_id, TextSendMessage(text=push_text))
                        print(f"Sent reminder to {user_id}")
                        reminded_count += 1
                    except Exception as e:
                        print(f"Failed to send to {user_id}: {e}")
                        
            except ValueError:
                continue # 日期格式不对跳过

    return {"status": "success", "reminded_count": reminded_count}