
---

# Telegram Auto-Scheduler

This project automates sending messages to a Telegram group at specific times and handles admin replies based on predefined responses.

## Features
- Schedule messages to be sent at specific times.
- Automatically reply to user messages with predefined answers.
- Supports multiple Telegram accounts.

---

## Prerequisites
- Python 3.8 or higher
- A Telegram account and API credentials (API ID and API Hash)

---

## Setup

### 1. **Get Telegram API Credentials**
To use this project, you need to obtain your Telegram API credentials (API ID and API Hash). Follow these steps:

1. Go to [my.telegram.org](https://my.telegram.org).
2. Log in with your Telegram account.
3. Click on **"Create Application"**.
4. Fill in the required details (App title, Short name, etc.).
5. Once created, you will see your **API ID** and **API Hash**. Save these credentials.

---

### 2. **Install Required Python Libraries**
This project uses the following Python libraries:
- `telethon` (for interacting with Telegram's API)
- `pandas` (for handling CSV files)
- `python-dotenv` (for managing environment variables)
- `pytz` (for timezone handling)

Install them using the following command:

```bash
pip install telethon pandas python-dotenv pytz
```

---

### 3. **Clone the Repository**
Clone the repository to your local machine:

```bash
git clone https://github.com/rifatxtra/multiple-telegram-auto-scheduling-bot.git
cd telegram-auto-scheduler
```

---

### 4. **Set Up Environment Variables**
1. Create a `.env` file in the project root directory.
2. Add your Telegram API credentials and phone numbers to the `.env` file:

   ```env
   ADMIN_PHONE_NUMBER=+8801845878722
   ADMIN_API_ID=29437431
   ADMIN_API_HASH=92cf3838036d3e315251777f39764005

   ACCOUNT1_PHONE_NUMBER=+8801650029860
   ACCOUNT1_API_ID=23639554
   ACCOUNT1_API_HASH=ea5782cccfa7e84429ae5061dd227a79

   ACCOUNT2_PHONE_NUMBER=+8801917534467
   ACCOUNT2_API_ID=23502983
   ACCOUNT2_API_HASH=f3a29c5ac62a188f5baaab54e461ee37

   ACCOUNT3_PHONE_NUMBER=+8801834673401
   ACCOUNT3_API_ID=24072690
   ACCOUNT3_API_HASH=c7867e55b25298b32dd62700afc650ed
   ```

   Replace the placeholders with your actual credentials.

---

### 5. **Prepare CSV Files**
- Create CSV files for each account and admin with the required data.
- Example format for `admin_responses.csv`:

  ```csv
  question,answer
  "Good Morning!","Good Morning! How are you doing today?"
  "What is State1?","State1 is an innovative ecosystem..."
  ```

- Example format for `carlos.csv` (for scheduled messages):

  ```csv
  codetime,question
  "08:00","Good Morning!"
  "12:00","Good Afternoon!"
  ```

---

### 6. **Run the Script**
Run the script using the following command:

```bash
python test.py
```

---

## Configuration
- Update the `group_username` variable in the `schedule_messages` function to your Telegram group username.
- Modify the CSV files to customize questions and answers.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### **Additional Notes**
- Ensure the `.env` file is added to `.gitignore` to avoid uploading sensitive data to GitHub.
- The script uses the **Telethon** library, which requires an active internet connection to interact with Telegram's API.

---
