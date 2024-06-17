import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlretrieve
from subprocess import call

# Path to your Chrome profile
chrome_profile_path = "/Users/hmelenok/Library/Application Support/Google/Chrome"
profile_path = "Default"

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
chrome_options.add_argument(f"profile-directory={profile_path}")

# Initialize WebDriver with Chrome options
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://web.whatsapp.com')

# Wait for the user to manually log in if necessary
time.sleep(15)

# Function to get new images from a specific channel
def get_new_images(channel_name):
    images = []
    try:
        # Locate the chat with the given channel name
        channel = driver.find_element_by_xpath(f"//span[@title='{channel_name}']")
        channel.click()
        
        # Allow time for messages to load
        time.sleep(5)
        
        # Find all image elements in the chat
        image_elements = driver.find_elements_by_xpath("//img[contains(@src, 'blob:')]")
        
        for img in image_elements:
            img_url = img.get_attribute('src')
            images.append(img_url)
    except Exception as e:
        print(f"Error retrieving images: {e}")
    return images

# Function to download images to a specified folder
def download_images(image_urls, download_folder):
    downloaded_files = []
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    for index, url in enumerate(image_urls):
        try:
            filename = os.path.join(download_folder, f'image_{index}.jpg')
            urlretrieve(url, filename)
            downloaded_files.append(filename)
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Error downloading image {url}: {e}")
    return downloaded_files

# Function to send images via Signal CLI to a group
def send_images_to_group_via_signal(image_files, signal_number, group_id):
    for image in image_files:
        try:
            call(['signal-cli', '-u', signal_number, 'send', '-g', group_id, '-a', image])
            print(f"Sent {image} to group {group_id} via Signal")
        except Exception as e:
            print(f"Error sending image {image}: {e}")

# Main script logic
channel_name = 'Your Channel Name'  # Replace with the actual channel name
download_folder = '/Users/hmelenok/IdeaProjects/py-scrips'  # Replace with the desired download path
signal_number = '+380930978997'  # Your Signal phone number
group_id = 'your_group_id'  # Replace with your Signal group ID

while True:
    new_images = get_new_images(channel_name)
    if new_images:
        downloaded_files = download_images(new_images, download_folder)
        send_images_to_group_via_signal(downloaded_files, signal_number, group_id)
    time.sleep(60)  # Check for new images every minute

# Close the driver after use
driver.quit()
