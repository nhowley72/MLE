import functions_framework
import numpy as np
import yfinance as yf
import joblib
from google.cloud import storage
import tempfile

BUCKET_NAME = "stock_bucket_gcp_tikr"
MODEL_FILE = "models/AAPL_model.joblib"
model = None

def load_model():
    global model
    if model is None:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(MODEL_FILE)

        with tempfile.NamedTemporaryFile(suffix=".joblib") as tmp:
            blob.download_to_filename(tmp.name)
            model = joblib.load(tmp.name)

@functions_framework.http
def predict_stock(request):
    request_json = request.get_json(silent=True)
    if not request_json or "ticker" not in request_json:
        return {"error": "Missing 'ticker' in request"}, 400

    ticker = request_json["ticker"]
    load_model()

    df = yf.download(ticker, period="90d", interval="1d")
    if df.empty or 'Close' not in df.columns or len(df['Close']) < 60:
        return {"error": f"Not enough data for ticker: {ticker}"}, 400

    close = df['Close'].values[-60:]
    input_data = np.reshape(close, (1, -1))  # update this to match your model's expected input

    prediction = model.predict(input_data)
    predicted_price = float(prediction[0])

    return {"ticker": ticker, "predicted_price": predicted_price}
