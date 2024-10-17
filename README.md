# New York Times Trending Topics Analysis

## Overview

This Python project fetches news articles from the New York Times API for a specific section (e.g., Technology, Politics, Books), analyzes the frequency of keywords, and visualizes the data using bar charts and line graphs. The user interface allows selecting the section, date range, and periodicity (daily, weekly, or monthly).

## Features

1. **Data Collection**:

   - Uses the New York Times API to retrieve news articles from selected sections over a specified period.
   - Extracts and stores relevant data from articles, such as headlines, publication dates, and keywords.

2. **Keyword Frequency Analysis**:

   - Counts the occurrence of unique keywords in the selected section.
   - Displays the top 5 keywords based on frequency.

3. **Data Visualization**:
   - Bar chart showing the most frequently mentioned keywords in the section over the selected period.
   - Line chart illustrating the number of articles published per selected period (daily, weekly, monthly) to spot trends.

## How to Use

1. **Install Required Libraries**:
   Ensure you have the following Python libraries installed:

   - `requests`
   - `pandas`
   - `matplotlib`
   - `seaborn`

   You can install them using pip:

   ```bash
   pip install requests pandas matplotlib seaborn
   ```

2. **Run the Program**:
   - Add your API key in the code where the `API_KEY` variable is set.

3. **Input Parameters**:
   When you run the script, it will ask you to input the following:

   - **Section**: The section you want to analyze (e.g., `books`, `technology`).
   - **Start Date**: The starting date for fetching articles (in `YYYYMMDD` format).
   - **End Date**: The ending date for fetching articles (in `YYYYMMDD` format).
   - **Periodicity**: The periodicity for the line graph visualization (e.g., `daily`, `weekly`, `monthly`).

4. **View Results**:
   - After the script runs, it will display:
     - A bar chart of the top 5 keywords by frequency.
     - A line chart of the number of articles published over the selected period.

## Example Run

```bash
$ python nyt_trending_topics.py
Enter the section (e.g., Technology, Politics): books
Enter the start date (YYYYMMDD): 20240901
Enter the end date (YYYYMMDD): 20241012
Enter the periodicity for visualization (daily, weekly, monthly): daily
```

## Project Structure

NYT/
│
├── nyt_trending_topics.py # Main Python script for fetching and visualizing data
├── README.md # This file

## Notes

- The New York Times API has a limit of 10 articles per call, so the script paginates through multiple calls to fetch around 50-100 articles.
- The bar chart shows the top 5 most frequently mentioned keywords, while the line graph illustrates the number of articles published over the selected time period.
