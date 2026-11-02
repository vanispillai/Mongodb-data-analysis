
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load the cleaned customer feedback dataset
df = pd.read_csv("customer_feedback_cleaned.csv")

# Check that the review text column exists
print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())

# Create the sentiment analyser
analyzer = SentimentIntensityAnalyzer()

# Analyse the actual review text
def analyse_sentiment(text):
    if pd.isna(text) or str(text).strip() == "":
        return "Neutral"

    score = analyzer.polarity_scores(str(text))["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Store text-based sentiment separately from rating-based sentiment
df["sentiment_text"] = df["text"].apply(analyse_sentiment)

# Display the sentiment counts
print("\nText-based sentiment distribution:")
print(df["sentiment_text"].value_counts())

# Show sample reviews and their sentiment
print("\nSample results:")
print(
    df[["text", "stars_review", "rating_review", "sentiment_text"]]
    .head(10)
    .to_string(index=False)
)

# Save the results to a new CSV
df.to_csv("customer_feedback_sentiment.csv", index=False)

print("\nSaved results to customer_feedback_sentiment.csv")
