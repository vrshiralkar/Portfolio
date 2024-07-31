import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import openpyxl
import json

url= 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&supportedlang=english&infinite=1'
def totalresults(url):
    r = requests.get(url)
    data = dict(r.json())
    totalresults = data['total_count']
    print(totalresults)
    return int(totalresults)

def get_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return data['results_html']
def parse(data):
    games_list = []
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a', class_='search_result_row')
    for game in games:
        title = game.find('span', {'class': 'title'}).text.strip()
        released = game.find('div', {'class': 'col search_released responsive_secondrow'}).text.strip()

        original_price_elem = game.find('div', {'class': 'discount_original_price'})
        original_price = original_price_elem.text.strip().replace('€', '').replace(',', '.') if original_price_elem else 'N/A'

        discount_price_elem = game.find('div', {'class': 'discount_final_price'})
        discount_price = discount_price_elem.text.strip().replace('€', '').replace(',', '.') if discount_price_elem else 'N/A'

        platforms = []
        if game.find('span', class_='platform_img win'):
            platforms.append('Windows')
        if game.find('span', class_='platform_img mac'):
            platforms.append('Mac')
        if game.find('span', class_='platform_img linux'):
            platforms.append('Linux')

        game_data = {
            'title': title,
            'released': released,
            'platforms': ', '.join(platforms),
            'original_price': original_price,
            'discount_price': discount_price
        }
        games_list.append(game_data)
    return games_list

def cleaning(results):
    # Flattening the list of lists and creating a DataFrame
    games_df = pd.DataFrame([item for sublist in results for item in sublist])
    print("Initial DataFrame:\n", games_df.head())

    # Check for duplicates based on 'title' and 'released' columns
    before_deduplication = len(games_df)
    games_df = games_df.drop_duplicates(subset=['title', 'released'])
    after_deduplication = len(games_df)
    duplicates_removed = before_deduplication - after_deduplication
    print(f"Number of duplicates removed: {duplicates_removed}")

    # Convert 'released' to datetime, coercing errors to NaT (not a time)
    games_df['released'] = pd.to_datetime(games_df['released'], errors='coerce')

    # Remove rows where the datetime conversion was not successful (i.e., 'released' is NaT)
    cleaned_data_df = games_df.dropna(subset=['released'])
    print("After removing incorrect release dates, the count is:\n", len(cleaned_data_df))

    # Remove rows where the 'platforms' column is blank or contains empty strings(indicating its not a game)
    cleaned_data_df = cleaned_data_df[cleaned_data_df['platforms'].astype(bool)]  # This removes both NaN and empty strings
    print("After removing blank platforms, the count is:\n", len(cleaned_data_df))

    # Remove rows where the discount price is 'N/A'
    cleaned_data_df = cleaned_data_df[cleaned_data_df['discount_price'] != 'N/A']
    print("After removing N/A discount_price, the count is:\n", len(cleaned_data_df))


    # Format the 'released' date column for readability
    cleaned_data_df['released'] = cleaned_data_df['released'].dt.strftime('%d %B, %Y')
    print("DataFrame after formatting dates and cleaning platforms:\n", cleaned_data_df.head())

    return cleaned_data_df

def output(cleaned_data_df):
    # Save the cleaned data to an Excel file
    cleaned_data_df.to_excel('games_top_sellers.xlsx', index=False)
    print('Saved as Excel')

results = []
for x in range(0, totalresults(url), 50):
    data = get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&supportedlang=english&infinite=1')
    results.append(parse(data))
    print('Results Scraped: ', x)
    time.sleep(2.0)

cleaned_data = cleaning(results)
output(cleaned_data)