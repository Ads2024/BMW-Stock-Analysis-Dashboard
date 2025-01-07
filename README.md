# BMW Stock Analytics Dashboard 🚗

A modern, interactive dashboard built with Streamlit for analyzing BMW stock data. Features a beautiful UI with glassmorphism effects and dynamic starfield background animation.

![Dashboard Preview](assets\Preview.gif)

## 🌟 Features

- **Interactive Stock Analysis**
  - Real-time candlestick charts
  - Volume analysis
  - Technical indicators (Moving Averages, Bollinger Bands)
  - RSI (Relative Strength Index) visualization

- **Advanced Analytics**
  - Returns distribution analysis
  - Volatility tracking
  - Key statistical metrics
  - Technical pattern detection

- **Modern UI/UX**
  - Glassmorphism effect
  - Dynamic starfield background
  - Responsive layout
  - Interactive controls
  - Custom styling and animations

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Ads2024/bmw-stock-analytics.git
cd bmw-stock-analytics
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run src/app.py
```

## 📁 Project Structure

```
bmw-stock-analytics/
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── assets/
│   └── giphy.webp          # Dashboard assets
├── data/
│   └── BMW_Data.csv        # Stock data
├── src/
│   ├── app.py              # Main application
│   └── styles.py           # Styling and animations
├── .gitattributes
├── .gitignore
├── LICENSE
└── README.md
```

## 🛠️ Built With

- [Streamlit](https://streamlit.io/) - The web framework
- [Plotly](https://plotly.com/) - Interactive charts
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [NumPy](https://numpy.org/) - Numerical computations
- [SciPy](https://scipy.org/) - Statistical analysis

## 📊 Dashboard Components

1. **Main Price Chart**
   - Candlestick visualization
   - Volume subplot
   - Customizable technical indicators

2. **Metrics Overview**
   - Current price
   - Price change
   - Average volume
   - Volatility metrics

3. **Technical Analysis**
   - RSI indicator
   - Moving averages
   - Bollinger Bands
   - Technical signals detection

4. **Statistical Analysis**
   - Returns distribution
   - Rolling volatility
   - Key performance metrics

## 🎨 Customization

The dashboard's appearance can be customized by modifying:
- `src/styles.py` - Contains styling and animation configurations
- `.streamlit/config.toml` - Streamlit-specific settings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

