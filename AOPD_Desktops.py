## Charlie Must
## 4/10/2024
## A script in python that fetches the Astronomy Picture of the Day (APOD) 
## from NASA's website for the past 20 days and saves them to a local directory.
## The script uses the requests library to fetch the HTML content and 
## BeautifulSoup to parse it.
import datetime
import requests
from bs4 import BeautifulSoup
from os import path, makedirs

# Configurable parameters
today = datetime.datetime.today().strftime("%y%m%d")  # Today's date in YYMMDD format
num_days = 20  # Number of days to retrieve

# Base URL
base_url = "https://apod.nasa.gov/apod/ap"

def generate_urls(today, num_days):
    # Convert start_date to datetime object
    origin = datetime.datetime.strptime(today, "%y%m%d")

    urls = []
    for i in range(num_days):
        # Calculate the previous date
        previous_date = origin - datetime.timedelta(days=i)
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
urls = generate_urls(today, num_days)

# Fetch and display image URLs
## Added code that checks for "Users/Public/Pictures/AOPD_Images" in Windows 
#  if it does not exist it makes the directory and saves the fetched images to 
# the new directory ONLY if they are new (checks the past 20 days)

for url in urls:
    try:
        image_url = fetch_AOPD_with_URL(url)
        print(f"Image found: {image_url}")
        print(f"Saving image to local Folder: C:\\Users\\Public\\Pictures\\AOPD_Images\\{image_url.split('/')[-1]}")
        try:
            img_data = requests.get(image_url).content
            with open(f"C:\\Users\\Public\\Pictures\\AOPD_Images\\{image_url.split('/')[-1]}", 'wb') as handler:
                handler.write(img_data)
            print("Image saved successfully.")
        except FileNotFoundError:
            print("Directory does not exist. Creating directory...")
            makedirs("C:\\Users\\Public\\Pictures\\AOPD_Images", mode=0o777, exist_ok=True)
            img_data = requests.get(image_url).content
            with open(f"C:\\Users\\Public\\Pictures\\AOPD_Images\\{image_url.split('/')[-1]}", 'wb') as handler:
                handler.write(img_data)
            print("Image saved successfully.")
        except FileExistsError:
            pass
    except Exception as e:
        print(f"Error fetching from {url}: {e}")