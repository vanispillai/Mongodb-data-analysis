# Customer Feedback Analytics Using MongoDB

## 1. Project Overview

The **Customer Feedback Analytics** project focuses on analysing customer reviews using MongoDB and Python. The objective is to understand customer satisfaction, identify review patterns, and explore how ratings and sentiment vary across different locations and time periods.

The project uses MongoDB for storing and querying review data and Streamlit for building an interactive dashboard.

## 2. Project Objectives

- Analyse customer feedback and review ratings.
- Understand the distribution of positive, negative, and neutral reviews.
- Compare customer sentiment with star ratings.
- Analyse customer reviews across different states and cities.
- Identify monthly review trends.
- Present insights through an interactive dashboard.

## 3. Dataset Information

- **Dataset:** Yelp Restaurant Reviews Sentiment Dataset
- **Original filename:** `yelp_sentiment_master_dataset.csv`
- **Records analysed:** 14,351
- **Source:** [Zenodo Dataset](https://zenodo.org/records/18723813)
- **DOI:** [10.5281/zenodo.18723813](https://doi.org/10.5281/zenodo.18723813)
- **Author:** G, Saravanarajan

The dataset was cleaned and processed before being used for MongoDB analysis and dashboard development.

The cleaned dataset is available in the `project_data` folder.

## 4. Tools and Technologies

- **MongoDB:** Database storage, querying, and aggregation.
- **Python:** Data cleaning and analysis.
- **PyMongo:** Connecting Python with MongoDB.
- **Pandas:** Data manipulation and processing.
- **Streamlit:** Interactive dashboard development.
- **Plotly:** Data visualisation.

## 5. Project Workflow

1. Dataset collection and initial inspection.
2. Data cleaning and date formatting using Python.
3. Importing cleaned data into MongoDB.
4. Performing MongoDB queries and aggregation analysis.
5. Analysing customer ratings and sentiment.
6. Developing an interactive dashboard using Streamlit.
7. Presenting findings through visualisations.

## 6. MongoDB Analysis

The project uses the database:

`customer_feedback_analysis`

Collection:

`feedback`

MongoDB queries and aggregation operations were used to explore:

- Total customer reviews.
- Average review ratings.
- Rating distribution.
- Sentiment distribution.
- Review trends over time.
- Customer feedback across states and cities.

## 7. Sentiment Analysis

A separate Python script, `sentimental_analysis.py`, demonstrates text-based sentiment analysis of customer reviews.

For the final dashboard, the existing `rating_review` field in the dataset is used to visualise positive, negative, and neutral sentiment categories.

**Important:** The text-based sentiment analysis exercise and the dataset's existing sentiment labels are separate parts of this project.

## 8. Dashboard Features

The interactive Streamlit dashboard includes:

- Total review count and key performance indicators.
- Average star rating.
- Positive, negative, and neutral sentiment distribution.
- Star rating analysis.
- Monthly review trends.
- State-level review analysis.
- City-level review analysis.
- Review details and rating comparisons.

## 9. Key Findings

Based on the 14,351 reviews analysed:

| Metric | Result |
|---|---:|
| Total Reviews | 14,351 |
| Average Star Rating | 3.81 |
| Positive Reviews | 9,857 |
| Negative Reviews | 2,699 |
| Neutral Reviews | 1,795 |

Positive reviews represent the largest sentiment category in the dataset.

These findings provide an overview of customer feedback patterns and satisfaction levels.

## 10. Project Screenshots

Dashboard screenshots are available in the `project_screenshot` folder.

They demonstrate the KPI overview, sentiment distribution, star ratings, monthly trends, and geographical analysis.

## 11. How to Run the Project

### Prerequisites

- Python installed.
- MongoDB installed and running.
- Required Python libraries.

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the dashboard

Make sure MongoDB is running and the database connection settings in the dashboard script are configured correctly.

```bash
streamlit run feedback_dashboard.py
```

## 12. Project Structure

```text
Customer_Feedback_Analytics/
│
├── project_data/
│   └── customer_feedback_cleaned.csv
│
├── project_screenshot/
│   └── Dashboard screenshots
│
├── clean_customer_feedback.py
├── feedback_dashboard.py
├── review_analysis.py
├── sentimental_analysis.py
├── requirements.txt
└── Readme.md
```

## 13. Conclusion

This project provided practical experience in working with MongoDB, Python, data cleaning, aggregation queries, and interactive dashboard development.

It demonstrates how customer feedback data can be transformed into meaningful insights through database analysis and visualisation.

---

**Project Category:** Data Analytics | MongoDB | Python | Streamlit