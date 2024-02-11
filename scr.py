import telebot
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from io import BytesIO
import time

bot = telebot.TeleBot('6942488105:AAGVGWj0jS0dPYjKqH7QPZXgh7s80PMrTlk')


# Define the channel ID where you want to post updates
channel_id = '@gsiuy7e76289y'

@bot.message_handler(commands=['start'])
def start(message):
    words = message.text.split()
    if len(words) > 1:
        # Extract the letter from the command
        letter = words[1].lower()  # Convert the letter to lowercase for consistency
        bot.send_message(message.chat.id, f"Started posting items starting with letter '{letter}'\n")
        send_updates(letter)
    else:
        # Provide instructions to the user if no letter is provided
        bot.send_message(message.chat.id, f"Welcome to the Bot!\n"
                                          f"Send /start followed by a letter to start posting businesses starting with that letter\n\n"
                                          f"For example: <code>/start e</code> will print all businesses that start with the letter 'e'\n"
                         , parse_mode='HTML')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "This bot sends updates periodically. Just type /start to begin receiving updates.")

def send_updates(letter):
    try:
        URL = 'https://www.ethyp.com/category/Ecommerce'
        page = requests.get(URL, timeout=30)
        soup = BeautifulSoup(page.content, "html.parser")
        posts = soup.find_all("div", class_="company with_img g_0")

        for post in posts:
            title = post.find("h4").text.strip()
            if title[0].lower() == letter:
                print('1')
                address = post.find("div", class_="address").text.strip()
                description = post.find("div", class_="desc").text.strip()
                verified = post.find("u", class_="v").text.strip() if post.find("u", class_="v") else "Not Verified"

                # Extracting image URL
                image_tag = post.find("img") 
                if image_tag:
                    image_url = f'https://www.ethyp.com{image_tag.get("data-src")}'
                    if image_url:
                        # Download the image
                        image_response = requests.get(image_url)
                        if image_response.status_code == 200:
                            # Send the image and text to the channel ID
                            bot.send_photo(channel_id, photo=BytesIO(image_response.content), caption=f"<b>{title}</b>\n\nAddress: {address}\nDescription: {description}\nVerified: {verified}", parse_mode="HTML")

                            # rest between posts 
                            time.sleep(7)
                        else:
                            bot.send_message(channel_id, f"Failed to download image for {title}")
                    else:
                        bot.send_message(channel_id, f"No valid Image URL found for {title}")
                else:
                    bot.send_message(channel_id, f"No Image Found for {title}")

    except Exception as e:
        print("An error occurred:", e)
        # You can choose to log the error, send it to your chat, or simply ignore it

bot.polling(none_stop=True)