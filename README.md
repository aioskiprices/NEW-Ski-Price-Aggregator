# Ski Price Aggregator

A Python tool that tracks ski prices across different websites. The tool automatically scrapes and updates prices for specified ski models.

## Features

- Tracks ski prices from multiple websites
- Automatically updates prices when run
- Stores data in JSON format
- Easy to add new skis to track

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Add skis to track in `ski_prices.json`
2. Run the script:
   ```bash
   python3 main.py
   ```

## Data Structure

The `ski_prices.json` file contains:
- Site name
- Site URL
- Ski name
- Current price (automatically updated)

## Requirements

- Python 3.8 or higher
- requests
- beautifulsoup4 