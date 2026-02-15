# Options Profit Calculator

A web-based options profit/loss calculator with real-time data from Yahoo Finance.

## Features
- Real-time stock prices and option chains
- Multiple strategies (Long Call, Spreads, Iron Condors, etc.)
- Interactive P/L charts and heatmap tables
- Greeks calculation

## Deploy to Railway (Free)

### Step 1: Upload to GitHub

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** button (top right) → **New repository**
3. Name it `options-calculator`
4. Keep it **Public**
5. Click **Create repository**
6. On the next page, click **"uploading an existing file"**
7. Drag and drop ALL files from this folder
8. Click **Commit changes**

### Step 2: Deploy on Railway

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Choose your `options-calculator` repository
5. Railway will automatically detect it's a Python app
6. Wait 2-3 minutes for deployment
7. Click **Generate Domain** to get your public URL

### Done! 🎉

Your app will be live at something like:
`https://options-calculator-production.up.railway.app`

## Files

```
options-deploy/
├── app.py              # Flask backend
├── requirements.txt    # Python dependencies
├── Procfile           # Tells Railway how to run
├── railway.json       # Railway config
├── .gitignore         # Files to ignore
└── static/
    └── index.html     # The calculator frontend
```

## Data Source

Uses Yahoo Finance (15-30 min delayed data) - same as optionsprofitcalculator.com
