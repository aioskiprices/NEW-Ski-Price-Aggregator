# SkiSniper

SkiSniper is a web application that helps users find the best deals on skis by aggregating prices from multiple retailers.

## Features

- Real-time price comparison across 10+ retailers
- Search functionality for specific ski models
- Clean, modern UI with responsive design
- Automatic price updates
- Direct links to retailer websites

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SkiSniper.git
cd SkiSniper
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## Project Structure

```
SkiSniper/
├── app.py              # Main Flask application
├── ski_prices.json     # Database of ski prices
├── requirements.txt    # Python dependencies
├── static/            
│   └── css/
│       └── styles.css  # Application styles
├── templates/
│   └── index.html     # Main template
└── scrapers/          # Price scraping scripts
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 