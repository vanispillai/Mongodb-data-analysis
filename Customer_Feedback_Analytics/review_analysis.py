import pandas as pd
df = pd.read_csv("customer_review_analysis.csv")
'''print(df.head())
# 1. Dataset dimensions
print("Dataset shape:", df.shape)

# 2. Column names
print("\nColumn names:")
print(df.columns.tolist())

# 3. Data types and non-null counts
print("\nDataset information:")
df.info()

# 4. Statistical summary
print("\nStatistical summary:")
print(df.describe(include="all").T)'''

# Convert to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Display dates as DD-MM-YYYY
df["date"] = df["date"].dt.strftime("%d-%m-%Y")

print(df["date"].head())

'''# Missing values in each column
print("\nMissing values:")
print(df.isnull().sum())

# Total duplicate rows
print("\nDuplicate rows:", df.duplicated().sum())

# Empty text values
print("\nEmpty review texts:")
print(df["text"].astype("string").str.strip().eq("").sum())'''
'''# Check customer review ratings
print("\n--- Customer Rating Distribution ---")
print(df["stars_review"].value_counts().sort_index())

# Check for invalid ratings
invalid_ratings = df[
    ~df["stars_review"].between(1, 5)
]

print("Invalid customer ratings:", len(invalid_ratings))'''

'''#check sentiment labelprint("\n--- Sentiment Distribution ---")
print(df["rating_review"].value_counts(dropna=False))

print("\n--- Ratings vs Sentiment ---")
print(pd.crosstab(
    df["stars_review"],
    df["rating_review"],
    dropna=False
))'''
'''#check locations
print("\n--- Unique States ---")
print(sorted(df["state"].dropna().unique()))

print("\n--- Missing Locations ---")
print("Missing cities:", df["city"].isna().sum())
print("Missing states:", df["state"].isna().sum())

print("\n--- Top 10 Cities by Review Count ---")
print(df["city"].value_counts().head(10))'''
'''#check business categories
print("\n--- Top 10 Business Categories ---")
print(df["categories"].value_counts().head(10))'''
df.to_csv("customer_feedback_cleaned.csv", index=False)
print("CSV saved successfully!")





