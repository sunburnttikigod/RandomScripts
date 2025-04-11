# Author: Charlie Must
# A Python script to fetch Astronomy Picture of the Day (APOD) images from NASA's website.
# This script generates URLs for the APOD page based on a given start date and number of days,
# and retrieves the image URLs from those pages.
import datetime
import requests
from bs4 import BeautifulSoup


# Configurable parameters
start_date = "250321"  # Format: YYMMDD (e.g., 250321)
num_days = 10  # Number of days to retrieve

# Base URL
base_url = "https://apod.nasa.gov/apod/ap"

def generate_urls(start_date, num_days):
    # Convert start_date to datetime object
    start_date_obj = datetime.datetime.strptime(start_date, "%y%m%d")

    urls = []
    for i in range(num_days):
        # Calculate the previous date
        previous_date = start_date_obj - datetime.timedelta(days=i)
        formatted_date = previous_date.strftime("%y%m%d")
        
        # Construct the URL
        url = f"{base_url}{formatted_date}.html"
        urls.append(url)
    
    return urls

def fetch_AOPD_with_URL(url):
    response = requests.get(url)
    response.raise_for_status()

    # Parse the HTML to find the image URL
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tag = soup.find('img')

    if image_tag:
        image_url = "https://apod.nasa.gov/apod/" + image_tag['src']
        return image_url
    else:
        raise ValueError('No valid image found on the APOD page.')

# Generate URLs
urls = generate_urls(start_date, num_days)

# Fetch and display image URLs
for url in urls:
    try:
        image_url = fetch_AOPD_with_URL(url)
        print(f"Image found: {image_url}")
    except Exception as e:
        print(f"Error fetching from {url}: {e}")