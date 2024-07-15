from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import schedule
import time
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to scrape the website and return the price list
def scrape_prices():
    url = 'https://www.airbnb.de/s/Cluj~Napoca--Rumänien/homes?place_id=ChIJiwtskR8MSUcRixQfMxxgvAs&refinement_paths%5B%5D=%2Fhomes&checkin=2024-08-08&checkout=2024-08-12&date_picker_type=calendar&adults=2&search_type=filter_change&tab_id=home_tab&query=Cluj-Napoca%2C%20Rumänien&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-07-01&monthly_length=3&monthly_end_date=2024-10-01&search_mode=regular_search&disable_auto_translation=true&price_filter_input_type=0&price_filter_num_nights=4&channel=EXPLORE&price_max=68'  # Replace with the actual URL

    # Set up Selenium with ChromeDriver
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Navigate to the webpage
    driver.get(url)

    # Wait for the page to fully load
    driver.implicitly_wait(10)  # You can adjust the wait time as needed

    # Get the text content of the webpage
    text_content = driver.find_element(By.TAG_NAME, 'body').text

    # Close the WebDriver
    driver.quit()

    # Count the occurrences of the specific text 'Nacht'
    nacht_occurrences = text_content.count('Nacht')

    # Find all occurrences of the euro symbol (€) and prices
    euro_occurrences = text_content.count('€')

    # Use regular expression to find prices in the format 'xxx €' or 'xxx,xx €'
    #prices = re.findall(r'Vermieter:in\n\d+(?:,\d{2})?\s€', text_content)
    prices = re.findall(r'Vermieter:in\n(\d+(?:,\d{2})?\s€)', text_content)

    # Use regular expression to find the number before 'Unterkünfte'
    unterkunfte_number = re.search(r'(\d+)\s+Unterkünfte', text_content)

    # Extract the number if found
    if unterkunfte_number:
        unterkunfte_number = unterkunfte_number.group(1)
    else:
        unterkunfte_number = 'Not found'

   
    return unterkunfte_number,prices

# Function to send a Telegram notification
def send_telegram_notification(unterkunfte_number,new_prices, old_prices):
    bot_token = "7386501741:AAH61MTg7oYHpytm0cWQKhksEzjqTzG1lZM"  # Replace with your Telegram bot token
    chat_id = "2027643914"
    message = f"There are {unterkunfte_number} accomodations under 68€, and the different prices/night found on the webpage are: {new_prices}\n"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise ValueError(f"Request to Telegram returned an error {response.status_code}, the response is:\n{response.text}")

# Function to send an email notification
def send_email(unterkunfte_number,new_prices, old_prices):
    sender_email = "pianist.pablo@gmail.com"  # Replace with your email
    receiver_email = "pianist.pablo@gmail.com"  # Replace with recipient email
    password = ""  # Replace with your email password

    subject = "Price Change Notification"
     
    body=f"There are {unterkunfte_number} accomodations under 68€, and the different prices/night found on the webpage are: {new_prices}\nOld prices: {old_prices}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

# Function to compare prices and act accordingly
def check_prices():
    global last_prices
    unterkunfte_number,new_prices = scrape_prices()
    if new_prices != last_prices:
        send_telegram_notification(unterkunfte_number,new_prices, last_prices)
        #send_email(unterkunfte_number,new_prices, last_prices)
        last_prices = new_prices

# Initialize variables
last_prices = []
run_count = 0

# Schedule the task to run 10 times per day (every 2.4 hours)
#schedule.every(2.4).hours.do(check_prices)

# Run the task immediately
check_prices()

# Run the scheduler
#while True:
#    schedule.run_pending()

#    time.sleep(1)