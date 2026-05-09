from sklearn.linear_model import LinearRegression
import numpy as np

def train_forecast(df):
    df = df.sort_values("Order_Date")
    df["Day"] = np.arange(len(df))

    X = df[["Day"]]
    y = df["Total_Sales"]

    model = LinearRegression()
    model.fit(X, y)

    # Predict next 7 days
    future_days = np.arange(len(df), len(df) + 7).reshape(-1, 1)
    predictions = model.predict(future_days)

    return predictions