"""
Options Profit Calculator - Backend API
Fetches real options data from Yahoo Finance
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import yfinance as yf
from datetime import datetime
import numpy as np
import os

app = Flask(__name__, static_folder='static')
CORS(app)


# Serve the frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        
        current_price = (
            info.get('currentPrice') or 
            info.get('regularMarketPrice') or 
            info.get('previousClose', 0)
        )
        
        previous_close = info.get('previousClose', current_price)
        change = current_price - previous_close if current_price and previous_close else 0
        change_percent = (change / previous_close * 100) if previous_close else 0
        
        return jsonify({
            'symbol': symbol.upper(),
            'name': info.get('shortName', info.get('longName', symbol.upper())),
            'currentPrice': current_price,
            'previousClose': previous_close,
            'change': round(change, 2),
            'changePercent': round(change_percent, 2),
            'volume': info.get('volume', 0),
            'marketCap': info.get('marketCap', 0),
            'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh', 0),
            'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow', 0),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e), 'symbol': symbol}), 400


@app.route('/api/options/<symbol>/expirations', methods=['GET'])
def get_option_expirations(symbol):
    try:
        ticker = yf.Ticker(symbol.upper())
        expirations = ticker.options
        
        return jsonify({
            'symbol': symbol.upper(),
            'expirations': list(expirations),
            'count': len(expirations)
        })
    except Exception as e:
        return jsonify({'error': str(e), 'symbol': symbol}), 400


@app.route('/api/options/<symbol>/chain', methods=['GET'])
def get_option_chain(symbol):
    try:
        expiration = request.args.get('expiration')
        
        ticker = yf.Ticker(symbol.upper())
        
        info = ticker.info
        underlying_price = (
            info.get('currentPrice') or 
            info.get('regularMarketPrice') or 
            info.get('previousClose', 0)
        )
        
        if not expiration:
            expirations = ticker.options
            if not expirations:
                return jsonify({'error': 'No options available for this symbol'}), 400
            expiration = expirations[0]
        
        opt_chain = ticker.option_chain(expiration)
        
        calls = []
        for _, row in opt_chain.calls.iterrows():
            calls.append({
                'contractSymbol': row.get('contractSymbol', ''),
                'strike': float(row.get('strike', 0)),
                'lastPrice': float(row.get('lastPrice', 0)),
                'bid': float(row.get('bid', 0)),
                'ask': float(row.get('ask', 0)),
                'change': float(row.get('change', 0)) if not np.isnan(row.get('change', 0)) else 0,
                'percentChange': float(row.get('percentChange', 0)) if not np.isnan(row.get('percentChange', 0)) else 0,
                'volume': int(row.get('volume', 0)) if not np.isnan(row.get('volume', 0)) else 0,
                'openInterest': int(row.get('openInterest', 0)) if not np.isnan(row.get('openInterest', 0)) else 0,
                'impliedVolatility': float(row.get('impliedVolatility', 0)),
                'inTheMoney': bool(row.get('inTheMoney', False)),
                'type': 'call'
            })
        
        puts = []
        for _, row in opt_chain.puts.iterrows():
            puts.append({
                'contractSymbol': row.get('contractSymbol', ''),
                'strike': float(row.get('strike', 0)),
                'lastPrice': float(row.get('lastPrice', 0)),
                'bid': float(row.get('bid', 0)),
                'ask': float(row.get('ask', 0)),
                'change': float(row.get('change', 0)) if not np.isnan(row.get('change', 0)) else 0,
                'percentChange': float(row.get('percentChange', 0)) if not np.isnan(row.get('percentChange', 0)) else 0,
                'volume': int(row.get('volume', 0)) if not np.isnan(row.get('volume', 0)) else 0,
                'openInterest': int(row.get('openInterest', 0)) if not np.isnan(row.get('openInterest', 0)) else 0,
                'impliedVolatility': float(row.get('impliedVolatility', 0)),
                'inTheMoney': bool(row.get('inTheMoney', False)),
                'type': 'put'
            })
        
        exp_date = datetime.strptime(expiration, '%Y-%m-%d')
        days_to_expiry = (exp_date - datetime.now()).days + 1
        
        return jsonify({
            'symbol': symbol.upper(),
            'expiration': expiration,
            'daysToExpiry': max(0, days_to_expiry),
            'underlyingPrice': underlying_price,
            'calls': calls,
            'puts': puts,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e), 'symbol': symbol}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
