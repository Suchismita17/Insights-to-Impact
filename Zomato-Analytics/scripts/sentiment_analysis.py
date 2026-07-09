import pandas as pd
import os
import re
from textblob import TextBlob

# =========================
# LOAD DATA
# =========================
file_path = os.path.join("Data", "Zomato_Python.xlsm")
df = pd.read_excel(file_path, engine="openpyxl")

# =========================
# TEXT CLEANING FUNCTION
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df["Clean_Feedback"] = df["Customer_Feedback"].apply(clean_text)

# =========================
# SENTIMENT ANALYSIS
# =========================
def get_sentiment(text):
    score = TextBlob(text).sentiment.polarity

    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

df["Sentiment"] = df["Clean_Feedback"].apply(get_sentiment)

# =========================
# SAVE OUTPUT
# =========================
df.to_csv("Zomato_with_Sentiment.csv", index=False)

# =========================
# ANALYSIS
# =========================
print("Sentiment Distribution:\n", df["Sentiment"].value_counts())
print("\nSentiment %:\n", df["Sentiment"].value_counts(normalize=True) * 100)

print("\nCustomer Experience by Sentiment:\n",
      df.groupby("Sentiment")["Customer Experience"].mean())
