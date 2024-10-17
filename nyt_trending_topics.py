import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# New York Times API Key
API_KEY = "6yavxZOLqbrHKoBPE0sL1hAqhQqw3Jwd"

# List of available sections
available_sections = [
    "arts",
    "automobiles",
    "autos",
    "blogs",
    "books",
    "booming",
    "business",
    "business day",
    "corrections",
    "crosswords & games",
    "dining & wine",
    "editors' notes",
    "education",
    "fashion & style",
    "food",
    "front page",
    "giving",
    "global home",
    "great homes & destinations",
    "health",
    "home & garden",
    "international home",
    "job market",
    "learning",
    "magazine",
    "movies",
    "multimedia",
    "nyregion",
    "nyt now",
    "national",
    "new york",
    "obituaries",
    "olympics",
    "open",
    "opinion",
    "paid death notices",
    "public editor",
    "real estate",
    "science",
    "sports",
    "style",
    "sunday magazine",
    "sunday review",
    "t magazine",
    "t:style",
    "technology",
    "the public editor",
    "the upshot",
    "theater",
    "times topics",
    "timesmachine",
    "today's headlines",
    "topics",
    "travel",
    "u.s.",
    "universal",
    "urbaneye",
    "washington",
    "week in review",
    "world",
    "your money",
]


# Step 1: Function to collect data from the New York Times API
def get_articles(section, start_date, end_date):
    """
    Fetch articles from the New York Times API, paginating through multiple calls to gather
    around 50-100 articles due to the 10-article limit per call.
    """
    all_articles = []  # List to store all articles
    base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

    for page in range(5):  # Adjust to control the number of articles (5 pages * 10 articles = 50) as per our project requirement 50 articles are fine.
        # Parameters for the API request
        params = {
            "fq": f'section_name:("{section}")',  # Section filter
            "begin_date": start_date,  # Start date in YYYYMMDD format
            "end_date": end_date,  # End date in YYYYMMDD format
            "api-key": API_KEY,  # API key embedded here
            "page": page,  # Pagination
        }
        response = requests.get(base_url, params=params)  # Send request to the NYT API

        if response.status_code != 200:
            print(
                f"Error: Unable to fetch articles (status code {response.status_code})"
            )
            return []  # Return an empty list if there's an error

        data = response.json()  # Convert the response to JSON
        articles = data.get("response", {}).get("docs", [])  # Get the list of articles

        if not articles:
            break  # Stop if no more articles found

        all_articles.extend(articles)  # Add articles to the list

    return all_articles  # Return the list of articles


# Step 2: Function to normalize and extract article data (updated to extract "value" from keywords)
def extract_article_data(articles):
    """
    Extract useful information like headline, publication date, and keywords from each article.
    """
    headlines = [
        article["headline"]["main"] for article in articles
    ]  # Extract article headlines
    pub_dates = [
        article["pub_date"][:10] for article in articles
    ]  # Extract the publication dates (YYYY-MM-DD)
    keywords_list = [
        article["keywords"] for article in articles
    ]  # Extract keyword data from each article

    # Extract keyword values (ignoring other fields like 'rank' and 'name')
    keywords = [[kw["value"] for kw in kws] for kws in keywords_list]

    # Debugging: Print all extracted keywords
    print("Extracted keywords:", keywords)

    # Create a DataFrame to organize the extracted data
    df = pd.DataFrame(
        {"headline": headlines, "pub_date": pub_dates, "keywords": keywords}
    )
    return df  # Return the DataFrame


# Step 3: Function to count keyword occurrences and return top 5 keywords
def analyze_keywords(df, top_n=5):
    """
    Count how many times each keyword appears in the dataset, extracting the 'value' field,
    and return only the top N most frequent keywords (default is 5).
    """
    keyword_count = {}  # Dictionary to store keyword frequencies

    # Loop through the keyword lists and count occurrences of the 'value' field
    for keywords in df[
        "keywords"
    ]:  # Each "keywords" is a list of keywords for an article
        for keyword in keywords:
            if keyword in keyword_count:
                keyword_count[keyword] += 1  # Increase count if keyword already exists
            else:
                keyword_count[keyword] = 1  # Initialize count if keyword is new

    # Convert the dictionary into a DataFrame for easy analysis
    keyword_df = pd.DataFrame(
        keyword_count.items(), columns=["Keyword", "Count"]
    ).sort_values(by="Count", ascending=False)

    # Return only the top N keywords (default is 5)
    return keyword_df.head(top_n)


# Step 4: Function to visualize keyword frequency with a bar chart (with proper scaling)
def plot_keyword_frequency(keyword_df):
    """
    Create a bar chart showing the top N most frequently mentioned keywords.
    """
    plt.figure(figsize=(10, 6))  # Set figure size

    # Plot the bar chart using the keyword count data
    sns.barplot(x="Keyword", y="Count", data=keyword_df)

    # Set title and labels
    plt.title(f"Top 5 Most Frequent Keywords")
    plt.xlabel("Keyword")
    plt.ylabel("Count")

    # Set the x-axis tick marks to match the actual range of values
    plt.xticks(
        range(0, max(keyword_df["Count"]) + 1)
    )  # Set ticks based on actual count values

    plt.show()  # Show the chart


# Step 5: Function to visualize articles published over time
def plot_articles_over_time(df, periodicity):
    """
    Create a line chart to show the number of articles published per day, week, or month.
    """
    # Convert publication dates to datetime
    df["pub_date"] = pd.to_datetime(df["pub_date"])

    # Group by the chosen periodicity
    if periodicity == "daily":
        articles_per_period = (
            df.groupby(df["pub_date"].dt.date).size().reset_index(name="article_count")
        )
    elif periodicity == "weekly":
        articles_per_period = (
            df.groupby(df["pub_date"].dt.to_period("W"))
            .size()
            .reset_index(name="article_count")
        )
    elif periodicity == "monthly":
        articles_per_period = (
            df.groupby(df["pub_date"].dt.to_period("M"))
            .size()
            .reset_index(name="article_count")
        )
    else:
        print("Invalid periodicity selected. Defaulting to daily.")
        articles_per_period = (
            df.groupby(df["pub_date"].dt.date).size().reset_index(name="article_count")
        )

    # Ensure pub_date is converted to string for plotting
    articles_per_period["pub_date"] = articles_per_period["pub_date"].astype(str)

    # Ensure article_count is numeric
    articles_per_period["article_count"] = pd.to_numeric(
        articles_per_period["article_count"]
    )

    # Create the line plot
    plt.figure(figsize=(10, 6))  # Set figure size
    sns.lineplot(
        x="pub_date", y="article_count", data=articles_per_period
    )  # Create line plot
    plt.title(
        f"Number of Articles Published ({periodicity.capitalize()})"
    )  # Title of the chart
    plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
    plt.show()  # Show the chart


# Main function to handle user input and run the process
def main():
    # Step 1: Input from the user
    section = input("Enter the section (e.g., Technology, Politics): ").strip().lower()
    while section not in available_sections:
        print(f"Invalid section. Available sections are: {available_sections}")
        section = input("Enter a valid section: ").strip().lower()

    start_date = input("Enter the start date (YYYYMMDD): ")
    end_date = input("Enter the end date (YYYYMMDD): ")

    print("Fetching articles...")
    articles = get_articles(section, start_date, end_date)

    if not articles:
        print("No articles found for the given parameters.")
        return

    df = extract_article_data(articles)
    print(f"Extracted {len(df)} articles.")

    # Step 2: Perform keyword analysis and plot top 5 keywords
    keyword_df = analyze_keywords(df)
    plot_keyword_frequency(keyword_df)

    # Step 3: Ask the user for periodicity of the visualizations
    periodicity = (
        input("Enter the periodicity for visualization (daily, weekly, monthly): ")
        .strip()
        .lower()
    )

    # Step 4: Plot the articles over time based on the chosen periodicity
    plot_articles_over_time(df, periodicity)


if __name__ == "__main__":
    main()
