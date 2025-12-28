# U.S. Economic Analysis Dashboard

An interactive Streamlit dashboard analyzing U.S. economic conditions as of year-end 2025, focusing on the tensions between official economic data and consumer experience.

## The Central Question

Official GDP shows 3.8-4.3% growth in Q2-Q3 2025, while consumer sentiment sits at the second-lowest level ever recorded. This dashboard explores why.

## Features

- **GDP Controversy Analysis** — Comparison of official BEA figures vs. disputed calculations from Rosenberg Research
- **Consumer Sentiment Tracking** — Michigan Index and Conference Board data with recession signal indicators
- **Labor Market Stratification** — Overall unemployment vs. recent graduate employment crisis
- **Housing Affordability** — Price-to-income ratios and first-time buyer accessibility
- **Vehicle Market Analysis** — Transaction prices and affordability collapse
- **K-Shape Economy Framework** — Understanding the divergence between asset owners and non-asset owners
- **Investment Guidance** — Framework for positioning in an uncertain environment

## Data Sources

- Bureau of Economic Analysis (BEA)
- Rosenberg Research
- Federal Reserve Banks
- Bureau of Labor Statistics (BLS)
- University of Michigan Consumer Sentiment
- Conference Board
- National Association of Realtors (NAR)
- Cox Automotive / Kelley Blue Book

## Installation

```bash
# Clone the repository
git clone https://github.com/philescandon/2026EconomicOutlook.git
cd 2026EconomicOutlook

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install streamlit pandas plotly
```

## Usage

```bash
source venv/bin/activate
streamlit run streamlit_app.py
```

The dashboard will open at `http://localhost:8501`

## Requirements

- Python 3.10+
- streamlit
- pandas
- plotly

## Disclaimer

This analysis is for informational purposes only and does not constitute investment advice. All investments carry risk, including potential loss of principal. Investors should consult qualified financial advisors before making investment decisions.

## License

MIT
