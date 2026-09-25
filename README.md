# CodeAlpha - Web Scraping, EDA & Data Visualization

## Project Title
**Book Market Analysis using Web Scraping, EDA and Data Visualization**

## CodeAlpha Tasks Covered
- **Task 1:** Web Scraping
- **Task 2:** Exploratory Data Analysis (EDA)
- **Task 3:** Data Visualization

## Objective
This project collects book-product information from the public **Books to Scrape** demo website, converts the collected information into a structured CSV dataset, performs exploratory analysis, and creates visualizations to identify pricing, stock, category and rating patterns.

> Note: Books to Scrape is a demo website created for scraping practice. Its displayed prices/ratings are not real-world market values.

## Source Website
https://books.toscrape.com/

## Technologies
- Python
- Requests
- BeautifulSoup
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook / Google Colab

## Dataset Fields
- `title`
- `price_gbp`
- `availability`
- `rating`
- `category`
- `product_url`

## Project Workflow

```text
Public Website
      ↓
BeautifulSoup Web Scraping
      ↓
CSV Dataset
      ↓
Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Charts & Visualizations
      ↓
Insights
```

## How to Run

### 1. Install packages
```bash
pip install -r requirements.txt
```

### 2. Scrape the website
```bash
python scraper.py
```

This creates:
```text
data/books_scraped.csv
```

### 3. Run EDA + visualization
```bash
python eda_visualization.py
```

Charts will be saved inside:
```text
visualizations/
```

## Important EDA Questions
1. What is the average book price?
2. What are the minimum and maximum prices?
3. Which books are the most expensive?
4. How are books distributed by category?
5. How are ratings distributed?
6. What percentage/status of books are in stock?
7. Is there a visible relationship between rating and price?
8. Are there missing or duplicate records?
9. Are there unusual price values?

## Key Learning Outcomes
- HTML page structure and CSS selectors
- Multi-page web scraping
- Data extraction and CSV creation
- Missing-value and duplicate handling
- Descriptive statistics
- Trend/pattern identification
- Professional chart creation
- Communicating data-driven insights

## Repository Name
Use:

`CodeAlpha_BookMarketAnalysis`

## Suggested GitHub Structure

```text
CodeAlpha_BookMarketAnalysis/
│
├── data/
│   ├── books_sample.csv
│   └── books_scraped.csv
│
├── visualizations/
│
├── notebooks/
│   └── CodeAlpha_BookMarketAnalysis.ipynb
│
├── reports/
│   └── project_summary.md
│
├── scraper.py
├── eda_visualization.py
├── requirements.txt
├── README.md
└── .gitignore
```
