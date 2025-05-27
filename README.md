# Binance Futures Trading Bot

A simplified trading bot for Binance Futures Testnet that supports market and limit orders.

## Features

- Market and Limit order support
- Buy and Sell order sides
- Command-line interface
- Comprehensive logging
- Error handling
- Support for Binance Futures Testnet

## Setup

1. Create a Binance Futures Testnet account at https://testnet.binancefuture.com
2. Generate API credentials from the testnet dashboard
3. Create a `.env` file with your credentials:
   ```
   BINANCE_API_KEY=CIm7Qx9DntpKgsmvoh1ib1gVA4lAeaTf6c7vXjxLaDUMjwraECpvu3nRJGeRXqte
   BINANCE_API_SECRET=H5AblHU5a6EBLiTx34wr6ZUd02zytdGgJrpnN0I30zjidlYuejd4cdB1cdC9gXLi
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the bot:
```bash
python trading_bot.py
```

## Available Commands

- Place Market Order: `market <symbol> <side> <quantity>`
- Place Limit Order: `limit <symbol> <side> <quantity> <price>`
- Get Order Status: `status <order_id>`
- Exit: `exit`

## Example

```bash
# Place a market buy order for 0.1 BTC
market BTCUSDT buy 0.1

# Place a limit sell order for 0.1 BTC at $50,000
limit BTCUSDT sell 0.1 50000
``` 