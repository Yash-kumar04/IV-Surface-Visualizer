# IV Surface Visualizer

Visualize implied volatility (IV) surfaces from options data across strikes and expirations.

## Features
- Pulls options chain using `yfinance`
- Extracts IV across multiple expiries and strikes
- Generates 3D surface plot of IV

## Usage
```bash
pip install -r requirements.txt
python src/main.py
```

## Example Output
See plots/ folder for a sample 3D IV surface.