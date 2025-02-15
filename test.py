# test.py
import pandas as pd
import asyncio
import pytz
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import Message
from telethon import events
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Admin details (separate from account details)
admins = [
    {
        "phone_number": os.getenv("ADMIN_PHONE_NUMBER"),
        "session_name": "admin_session",
        "api_id": int(os.getenv("ADMIN_API_ID")),
        "api_hash": os.getenv("ADMIN_API_HASH"),
        "csv_file": "admin_responses.csv"  # CSV with questions and admin answers
    }
]

# Telegram API credentials for different accounts
accounts = [
    {
        "phone_number": os.getenv("ACCOUNT1_PHONE_NUMBER"),
        "session_name": "carlos_session",
        "api_id": int(os.getenv("ACCOUNT1_API_ID")),
        "api_hash": os.getenv("ACCOUNT1_API_HASH"),
        "csv_file": "carlos.csv"
    },
    {
        "phone_number": os.getenv("ACCOUNT2_PHONE_NUMBER"),
        "session_name": "tommy_session",
        "api_id": int(os.getenv("ACCOUNT2_API_ID")),
        "api_hash": os.getenv("ACCOUNT2_API_HASH"),
        "csv_file": "tommy.csv"
    },
    {
        "phone_number": os.getenv("ACCOUNT3_PHONE_NUMBER"),
        "session_name": "alex_session",
        "api_id": int(os.getenv("ACCOUNT3_API_ID")),
        "api_hash": os.getenv("ACCOUNT3_API_HASH"),
        "csv_file": "bob.csv"
    }
]

# Set Bangladesh timezone, enter your timezone name, search on ptyz library
bd_timezone = pytz.timezone("Asia/Dhaka")

# Function to load CSV data for general accounts
def load_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.sample(frac=1).reset_index(drop=True)  # Shuffle
    return df

# Function to load Admin CSV data (with two columns)
def load_admin_csv(file_path):
    df = pd.read_csv(file_path)
    if df.shape[1] != 2:
        raise ValueError(f"Admin CSV file must have exactly 2 columns. Found {df.shape[1]} columns.")
    df = df.sample(frac=1).reset_index(drop=True)  # Shuffle
    return df

# Function to group messages by hour
def group_messages_by_hour(df):
    hourly_questions = {}
    for _, row in df.iterrows():
        hour = row["codetime"][:2]  # Extract the hour (e.g., "08" from "08:30")
        if hour not in hourly_questions:
            hourly_questions[hour] = []
        hourly_questions[hour].append(row)  # No limit now
    return hourly_questions

# Function to handle message scheduling for each account
async def schedule_messages(account):
    # Initialize Telegram Client for the account
    client = TelegramClient(account["session_name"], account["api_id"], account["api_hash"])
    
    # Load the corresponding CSV
    df = load_csv(account["csv_file"])
    
    # Group messages by hour (without limiting the number of messages)
    hourly_questions = group_messages_by_hour(df)
    
    # Connect to the Telegram Client
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(account["phone_number"])
        try:
            # Attempt to sign in with phone code
            await client.sign_in(account["phone_number"], input(f"Enter the code for {account['phone_number']}: "))
        except SessionPasswordNeededError:
            # If two-step verification is enabled, request the password
            password = input(f"Two-step verification is enabled for {account['phone_number']}. Enter the password: ")
            await client.sign_in(account["phone_number"], password=password)

    while True:
        now = datetime.now(bd_timezone).strftime("%H:%M")
        
        # Check for messages to send at this exact time
        for row in df.itertuples():
            if row.codetime == now:
                msg_content = row.question

                # Send message to the group
                group_username = "@State1Global"  # Define your group username
                await client.send_message(group_username, msg_content)

                print(f"✅ Sent by {account['phone_number']}: {msg_content} at {row.codetime}")

        await asyncio.sleep(60)  # Check every minute

# Function to handle admin replies
async def handle_admin_replies(admin):
    # Initialize Telegram Client for the admin
    client = TelegramClient(admin["session_name"], admin["api_id"], admin["api_hash"])
    
    # Load the corresponding CSV with admin responses (2 columns)
    df = load_admin_csv(admin["csv_file"])

    # Connect to the Telegram Client
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(admin["phone_number"])
        try:
            # Attempt to sign in with phone code
            await client.sign_in(admin["phone_number"], input(f"Enter the code for {admin['phone_number']}: "))
        except SessionPasswordNeededError:
            # If two-step verification is enabled, request the password
            password = input(f"Two-step verification is enabled for {admin['phone_number']}. Enter the password: ")
            await client.sign_in(admin["phone_number"], password=password)

    # Listen for new messages
    @client.on(events.NewMessage)
    async def handler(event: Message):
        user_message = event.text.lower()  # Convert message to lowercase to avoid case sensitivity
        
        # Search for matching question in the CSV
        for row in df.itertuples():
            question = row.question.lower()  # Compare case-insensitively
            answer = row.answer
            # If the answer is enclosed in quotes, remove them
            if answer.startswith('"') and answer.endswith('"'):
                answer = answer[1:-1]
            if question in user_message:
                if event.sender.username:
                    await event.respond(f"Hey @{event.sender.username}, {answer}")
                else:
                    await event.respond(f"Hey {event.sender.first_name}, {answer}")

                print(f"✅ Replied with: {answer}")
                break

    # Run the event loop to listen for new messages
    await client.run_until_disconnected()

# Main function to handle scheduling for all accounts and admin replies
async def main():
    # Create tasks for each account
    tasks = []
    for account in accounts:
        tasks.append(schedule_messages(account))
    
    # Create tasks for each admin to handle replies
    for admin in admins:
        tasks.append(handle_admin_replies(admin))

    # Run the tasks concurrently
    await asyncio.gather(*tasks)

# Run the main scheduling function
with asyncio.run(main()):
    pass
