
#Create a Python script that:
#Prompts the user for a URL containing an image
#Creates a directory called "Fetched_Images" if it doesn't exist
#Downloads the image from the provided URL
#Saves it to the Fetched_Images directory with an appropriate filename
#Handles errors gracefully, respecting that not all connections succeed


import os
import requests
from urllib.parse import urlparse
from pathlib import Path
from requests.exceptions import RequestException
from PIL import Image

def fetch_image(url):
    try:
        # Create directory if it doesn't exist
        directory = "Fetched_Images"
        Path(directory).mkdir(parents=True, exist_ok=True)

        # Get the image from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image"

        # Ensure the filename has an image extension
        if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
            filename += ".jpg"  # Default to .jpg if no valid extension

        # Save the image to the directory
        file_path = os.path.join(directory, filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)

        # Verify that the file is a valid image
        try:
            img = Image.open(file_path)
            img.verify()  # Verify that it is, in fact, an image
            print(f"Image successfully downloaded and saved to {file_path}")
        except (IOError, SyntaxError) as e:
            os.remove(file_path)  # Remove invalid image file
            print(f"Downloaded file is not a valid image. Error: {e}")

    except RequestException as e:
        print(f"Failed to download image. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    url = input("Please enter the URL of the image: ")
    fetch_image(url)

