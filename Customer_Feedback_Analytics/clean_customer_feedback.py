
import pandas as pd
from pathlib import Path

# 1. File paths
input_file = Path(
    r"E:\data_analytics\mongoDB\customer_review_analysis.csv"
)

output_file = Path(
    r"E:\data_analytics\mongoDB\customer_feedback_cleaned.csv"
)

# 2. Load original CSV
df = pd.read_csv(input_file, low_memory=False)

print("Original dataset loaded successfully")
print("Original rows:", len(df))
print("Original columns:", df.columns.tolist())

# 3. Check date column
if "date" not in df.columns:
    raise ValueError("The date column was not found!")

# 4. Preserve original date values for checking
original_dates = df["date"].copy()

# 5. Convert dates using the original format
# Example: 07-07-18 22:09
df["date"] = pd.to_datetime(
    original_dates,
    format="%d-%m-%y %H:%M",
    errors="coerce"
)

# 6. Try parsing any remaining unconverted dates
missing_dates = df["date"].isna()

if missing_dates.any():
    fallback_dates = pd.to_datetime(
        original_dates[missing_dates],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

    df.loc[missing_dates, "date"] = fallback_dates

# 7. Validate without deleting any records
total_rows = len(df)
valid_dates = int(df["date"].notna().sum())
missing_dates_count = int(df["date"].isna().sum())

print("\nDATE VALIDATION")
print("-------------------------")
print("Total records:", total_rows)
print("Valid dates:", valid_dates)
print("Missing dates:", missing_dates_count)

# 8. Display remaining problematic date values
if missing_dates_count > 0:
    print("\nExamples of unconverted dates:")
    print(
        original_dates[df["date"].isna()]
        .head(10)
        .to_list()
    )

# 9. Save dates in a consistent format
# All rows are retained, even if some dates remain missing.
df["date"] = df["date"].dt.strftime(
    "%Y-%m-%d %H:%M:%S"
)

df.to_csv(output_file, index=False)

print("\nCleaned CSV saved successfully!")
print("Output file:", output_file)
print("Final rows:", len(df))
