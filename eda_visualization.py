"""
CodeAlpha Tasks 2 & 3 - EDA + Data Visualization

Run this after scraper.py.
If books_scraped.csv is not available, the script uses books_sample.csv.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_FILE = Path("data/books_scraped.csv")
SAMPLE_FILE = Path("data/books_sample.csv")
OUT_DIR = Path("visualizations")
OUT_DIR.mkdir(exist_ok=True)

file_to_use = DATA_FILE if DATA_FILE.exists() else SAMPLE_FILE
df = pd.read_csv(file_to_use)

print("=" * 60)
print("CODEALPHA - BOOK MARKET EDA & VISUALIZATION")
print("=" * 60)

# -------------------------
# DATA UNDERSTANDING
# -------------------------
print("\n1. DATASET SHAPE")
print(df.shape)

print("\n2. FIRST FIVE ROWS")
print(df.head())

print("\n3. DATA TYPES")
print(df.dtypes)

print("\n4. MISSING VALUES")
print(df.isnull().sum())

print("\n5. DUPLICATE ROWS")
print(df.duplicated().sum())

# -------------------------
# DATA CLEANING
# -------------------------
df = df.drop_duplicates().copy()

df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

df["stock_status"] = df["availability"].astype(str).str.contains(
    "In stock", case=False, na=False
).map({True: "In Stock", False: "Other"})

df["title_length"] = df["title"].astype(str).str.len()

# -------------------------
# EDA QUESTIONS
# -------------------------
print("\n6. BASIC STATISTICS")
print(df[["price_gbp", "rating", "title_length"]].describe())

print("\n7. AVERAGE PRICE")
print(round(df["price_gbp"].mean(), 2))

print("\n8. MINIMUM PRICE")
print(round(df["price_gbp"].min(), 2))

print("\n9. MAXIMUM PRICE")
print(round(df["price_gbp"].max(), 2))

print("\n10. MOST EXPENSIVE BOOKS")
print(
    df[["title", "price_gbp"]]
    .sort_values("price_gbp", ascending=False)
    .head(10)
    .to_string(index=False)
)

print("\n11. CATEGORY SUMMARY")
if df["category"].notna().any() and (df["category"] != "Unknown").any():
    category_summary = (
        df[df["category"] != "Unknown"]
        .groupby("category")
        .agg(
            product_count=("title", "count"),
            average_price=("price_gbp", "mean")
        )
        .sort_values("product_count", ascending=False)
    )
    print(category_summary.head(15))
else:
    print("Category data is unavailable in the starter dataset.")
    print("Run scraper.py to collect category data from product pages.")

print("\n12. RATING SUMMARY")
if df["rating"].notna().any():
    print(df["rating"].value_counts().sort_index())

# -------------------------
# VISUALIZATION
# -------------------------
sns.set_theme(style="whitegrid")

# 1. Price distribution
plt.figure(figsize=(9, 5))
sns.histplot(df["price_gbp"].dropna(), bins=20, kde=True)
plt.title("Distribution of Book Prices")
plt.xlabel("Price (£)")
plt.ylabel("Number of Books")
plt.tight_layout()
plt.savefig(OUT_DIR / "01_price_distribution.png", dpi=200)
plt.show()

# 2. Top 10 expensive books
top10 = df.nlargest(10, "price_gbp").sort_values("price_gbp")
plt.figure(figsize=(10, 6))
sns.barplot(data=top10, x="price_gbp", y="title")
plt.title("Top 10 Most Expensive Books")
plt.xlabel("Price (£)")
plt.ylabel("Book")
plt.tight_layout()
plt.savefig(OUT_DIR / "02_top_10_expensive_books.png", dpi=200)
plt.show()

# 3. Stock status
plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="stock_status")
plt.title("Book Stock Status")
plt.xlabel("Stock Status")
plt.ylabel("Number of Books")
plt.tight_layout()
plt.savefig(OUT_DIR / "03_stock_status.png", dpi=200)
plt.show()

# 4. Category count, only when category data exists
category_df = df[df["category"].notna() & (df["category"] != "Unknown")]

if not category_df.empty:
    category_counts = category_df["category"].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=category_counts.values, y=category_counts.index)
    plt.title("Top Book Categories by Number of Products")
    plt.xlabel("Number of Books")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "04_category_distribution.png", dpi=200)
    plt.show()

# 5. Rating distribution, only when rating data exists
rating_df = df.dropna(subset=["rating"])

if not rating_df.empty:
    plt.figure(figsize=(7, 5))
    sns.countplot(data=rating_df, x="rating")
    plt.title("Book Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Number of Books")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "05_rating_distribution.png", dpi=200)
    plt.show()

# 6. Price vs rating, only when rating data exists
if not rating_df.empty:
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=rating_df, x="rating", y="price_gbp", alpha=0.7)
    plt.title("Price vs Rating")
    plt.xlabel("Rating")
    plt.ylabel("Price (£)")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "06_price_vs_rating.png", dpi=200)
    plt.show()

print("\nAnalysis and visualization completed.")
print(f"Charts saved in: {OUT_DIR}")
