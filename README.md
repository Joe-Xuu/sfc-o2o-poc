# 🤖 LINE Bot Smart Lending System (PoC)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)
![LINE API](https://img.shields.io/badge/LINE-Messaging_API-00C300.svg)
![Google Sheets](https://img.shields.io/badge/Database-Google_Sheets-34A853.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A Proof of Concept (PoC) system for tracking item borrowing and returning using a **LINE Chatbot** interface. This project is designed for an empirical experiment to validate O2O (Online-to-Offline) interactions without a complex database setup, utilizing **Google Sheets** for real-time data visualization and management.

## Key Features

* **Scan to Borrow**: Users scan a QR code on the item, which triggers a LINE message to the bot. The bot logs the transaction into Google Sheets.
* **Tap to Return**: An **M5Stack** device (NFC/RFID) detects the returned item and calls the backend API to update the status.
* **Instant Feedback**: The LINE Bot replies immediately upon borrowing and sends a **Push Message** upon successful return.
* **Auto-Reminder**: A cron-triggered function checks Google Sheets for overdue items (e.g., > 3 days) and automatically sends **Push Notifications** to remind users.

## System Architecture

```mermaid
graph TD
    subgraph User Interaction
        User[User] -- 1. Scan QR --> LINE[LINE App]
        User -- 4. Tap NFC Card --> M5[M5Stack Device]
    end

    subgraph Cloud Backend (Render)
        LINE -- 2. Webhook --> FastAPI[FastAPI Backend]
        M5 -- 5. API Request --> FastAPI
        FastAPI -- 3. Reply/Push --> LINE
        FastAPI -- 6. Read/Write --> GSheet[(Google Sheets)]
    end

    subgraph Reminder System
        Cron[UptimeRobot / Cron] -- Daily Trigger --> FastAPI
        FastAPI -- Check Overdue --> GSheet
        FastAPI -- Send Reminder --> LINE
    end
```

## Tech Stack
- Backend: Python, FastAPI, Uvicorn

- Interface: LINE Messaging API (Chatbot)

- Database: Google Sheets (via gspread & Google Drive API)

- Hardware Endpoint: M5Stack AtomS3 + RFID Unit (C++)

- Deployment: Render.com

## Setup & Installation
**Prerequisites**

1. LINE Official Account: Create a channel with Messaging API enabled.

2. Google Cloud Platform:

    - Enable Google Sheets API and Google Drive API.

    - Create a Service Account and download the service_account.json key.

3. Google Sheet: Create a sheet and share it (Editor access) with the Service Account email.

    - Header Row (Must be exact): UserID | ItemID | Date | Status

1. Local Development

Clone the repository and set up the environment:

``` Bash
git clone [https://github.com/YOUR_USERNAME/line-bot-lending.git](https://github.com/YOUR_USERNAME/line-bot-lending.git)
cd line-bot-lending

# Create Virtual Environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# .\venv\Scripts\activate  # Windows

# Install Dependencies
pip install -r requirements.txt
```

2. Configuration (.env)

Create a .env file in the root directory and add your credentials:

```Ini, TOML
LINE_CHANNEL_ACCESS_TOKEN=your_long_token_here
LINE_CHANNEL_SECRET=your_secret_here
GOOGLE_SHEET_NAME=Name_Of_Your_Google_Sheet
OVERDUE_DAYS=3
Note: Place your service_account.json file in the root directory for local testing. DO NOT commit this file to GitHub.
```

3. Run Locally

``` Bash
uvicorn main:app --reload
```

Use Ngrok to expose your local server to LINE:

```Bash
ngrok http 8000
```

- Copy the Ngrok HTTPS URL.

- Set LINE Webhook URL to: https://your-ngrok-url.ngrok-free.app/callback

## ☁️ Deployment (Render)
1. Create a new Web Service on Render.

2. Connect this GitHub repository.

3. Build Command: pip install -r requirements.txt

4. Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

5. Environment Variables:

    - Add all variables from .env.

    - **Crucial Step**: Create a variable named GOOGLE_JSON. Paste the entire content of your service_account.json file into the value field. The code is designed to load credentials from this variable in production.

## API Endpoints
```Plaintext
Method	Endpoint	Description
POST	/callback	The Webhook URL for LINE Messaging API.
GET	/	Health check.
GET	/api/cron/check_overdue	Trigger this manually or via a cron job service (e.g., UptimeRobot) to send reminders.
```

## Project Structure
``` Plaintext
.
├── main.py              # Main application logic (FastAPI + Bot)
├── gen_qr_bot.py        # Script to generate Deep Link QR codes
├── requirements.txt     # Python dependencies
├── .env                 # Local secrets (Ignored by Git)
├── service_account.json # Google Cloud Key (Ignored by Git)
└── .gitignore           # Git ignore rules
```

## License
This project is licensed under the MIT License.
Kouzen Jo. 2025.