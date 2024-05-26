# Simple Python Script - Birthday Notification Reminder Telegram Bot
# Authored by - Vinay Kumar Sahu | Email: vinaykumar.sahu093@gmail.com | Insta ID: me_vinay_sahu
'''
This is simple Python script bot to get birthday reminder on Telegram of your beloved ones.
Easy to configure & deploy.
------- Follow the Guidelines below ----------

- Installation: pip install telebot
- First create your own Telegram bot with the help of "BotFather" and get the Telegram API KEY
- Get your CHAT ID with this link: https://api.telegram.org/bot<API_KEY>/getUpdates
- Create your own News API KEY from https://newsapi.org/ and add it to the configs
- Add these two values to the script
- Add the birthdates in form of dictionary to the script
- Visit here to Host for free: https://www.pythonanywhere.com/
- Upload the script in "Files" section
- Schedule the script in "Tasks" section
- In order to receive the telegram bot commands, we need to run the file constantly in terminal background.
- For that Run the file in the console using nohup command: nohup python filename.py &
- To check if the file is running in background or not. Run this command: ps aux | grep filename.py
- To kill the process, Run this command: kill -9 PID. Get the PID from the above command (2nd column).

You are good to go now !!! (Reachout if case of any queries)
'''

import pytz, requests, traceback, math
import numpy as np
import telebot
from telebot import types
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

configs = {
    'TELEGRAM_API_KEY': '',
    'TELEGRAM_CHAT_ID': '',
    'NEWSAPI_API_KEY': '',
    # These are the news categories: business, entertainment, general, health, science, sports, technology
    'NEWS_CATEGORY': 'technology',
    # Date Format: dd-mm-yyyy
    'BIRTHDATES': {
        # '27-11-1993': 'Vinay',
        '12-10-1949': 'Daddy',
        '10-12-1956': 'Mummy',
        '06-05-1995': 'Lipika',
        '17-07-1956': 'Bhaiya',
        '23-07-1956': 'Bhabi',
        '20-02-2007': 'Deepan',
        '15-01-2000': 'Rony',
        '03-11-1991': 'Kartik',
        '10-11-1993': 'Akash Reddy',
        '12-11-1993': 'L Sidharth',
        '21-03-1993': 'K Kiran Kumar',
        '14-09-1995': 'Shivangi Swain',
        '16-09-1995': 'Dazy didi (Shivangi Sis)',
        '03-03-1993': 'Daddy and Mummy Anniversary',
        '30-04-1993': 'Bhaiya and Bhabi Anniversary',
        '27-01-2022': 'Vinay and Lipika Anniversary',
        '22-01-2023': 'Jai Shree Ram',
        '10-05-1995': 'Basuki',
        '03-03-2023': 'Prahalad ADP',
        '14-04-1997': 'Abhinav ADP',
        '25-11-2023': 'Bhakti ADP',
        '03-04-1990': 'Kalpesh ADP',
        '16-05-2024': 'Mother day',
        # US holidays 2024
        '01-01-2024': 'New year Day',
        '15-01-2024': 'Martin Luther King Jr Day',
        '19-02-2024': 'Washington Birthday',
        '27-05-2024': 'US Memorial Day',
        '19-06-2024': 'US Juneteeth',
        '04-07-2024': 'US Independence Day',
        '02-09-2024': 'US Labor Day',
        '11-11-2024': 'US Veterans Day',
        '28-11-2024': 'US Thanksgiving Day',
        '25-12-2024': 'Christmas Day',
    },
    'REMIND_DATES': {
        '03-01-2023': 'Upcoming payments for:\n'
                      '- House Rent - GPay\n'
                      '- House Maintenance - PhonePe\n'
                      '- Electricity Payment - Cred/PhonePe\n'
                      '- Internet Bill - Cred/AirtelApp\n'
                      '- Credit Card Bills Payment - Cred\n'
                      '- Do Investments\n'
    },
    'every_month_remind_date': '02-01-2023',
    'OFFICE_HOLIDAYS': {
        '15-01-2024': 'Makar Sankranthi (Hyd Only)',
        '26-01-2024': 'Republic Day',
        '08-03-2024': 'Maha Shivratri (Pune Only)',
        '09-04-2024': 'Ugadi/Gudi Padwa',
        '11-04-2024': 'Ramzan',
        '01-05-2024': 'Labour Day/Maharastra Day',
        '13-05-2024': 'Telengana Election',
        '15-08-2024': 'Independence Day',
        '02-10-2024': 'Gandhi Jayanti',
        '31-10-2024': 'Diwali',
        '25-12-2024': 'Christmas',
    },
}

consts = {
    'timezone': 'Asia/kolkata',
}


# https://api.telegram.org/bot6649388608:AAGUSudo-eCJy1_iV4mrTk5UfkYuV_7gQNo/getUpdates
def telegram_send_msg(text_message='', is_parse_html=False):
    try:
        url = f"https://api.telegram.org/bot{configs['TELEGRAM_API_KEY']}/sendMessage?chat_id={configs['TELEGRAM_CHAT_ID']}&text={text_message}"
        url += "&parse_mode=HTML" if is_parse_html else ""
        print(requests.get(url).json())  # this sends the message

    except Exception as e:
        print('Exception while sending msg', e)
        print(traceback.format_exc())


class Notifier:

    def __init__(self, configs):
        self.bot = telebot.TeleBot(configs['TELEGRAM_API_KEY'])
        self.prior_reminder_flag = False
        self.no_of_days_before_reminder = 1
        self.today_date = datetime.now(pytz.timezone(consts['timezone'])).strftime("%d-%m")
        self.today_date_dd_only = datetime.now(pytz.timezone(consts['timezone'])).strftime("%d")
        self.today_date_mm_only = datetime.now(pytz.timezone(consts['timezone'])).strftime("%m")
        self.today_date_yyyy_only = datetime.now(pytz.timezone(consts['timezone'])).strftime("%Y")

    def calculate_age(self, dob_str):
        dob = datetime.strptime(dob_str, '%d-%m-%Y')
        age = relativedelta(date.today(), dob)
        return age.years

    def _trigger_birthday_notification(self, birthdate, birthday_person):
        print(f"Today's Date: {self.today_date}")
        text_message = (
            f"Birthday Reminder of {birthday_person}\n"
            f"Birthdate: {birthdate}\n"
            f"Age: {self.calculate_age(birthdate)}"
        )
        print(text_message)
        telegram_send_msg(text_message)

    def _trigger_reminder_notification(self, remind_date, remind_thing):
        print(f"Today's Date: {self.today_date}")
        text_message = (
            f"General Monthly Reminder: \n{remind_thing}\n"
            f"Please do the needful !!!"
        )
        print(text_message)
        telegram_send_msg(text_message)

    def remind_before_birthdate(self, birthdate, no_of_days_before=1):
        next_date = (date.today() + timedelta(days=no_of_days_before)).strftime('%d-%m')
        return bool(next_date == birthdate[:-5])

    def is_birthday_today(self):
        for birthdate, birthday_person in configs['BIRTHDATES'].items():
            if self.prior_reminder_flag and self.remind_before_birthdate(birthdate, self.no_of_days_before_reminder):
                self._trigger_birthday_notification(birthdate, birthday_person)
            # Get only the day and month part of the date
            if self.today_date == birthdate[:-5]:
                self._trigger_birthday_notification(birthdate, birthday_person)

    def is_monthly_reminder_today(self):
        for remind_date, remind_thing in configs['REMIND_DATES'].items():
            # Get only the day part of the date
            if self.today_date_dd_only == remind_date[:-8]:
                self._trigger_reminder_notification(remind_date, remind_thing)

    def is_any_office_holiday_this_month(self):
        # Check at the beginning of the month for all the holidays of the month
        if self.today_date_dd_only == configs['every_month_remind_date'][:-8]:
            text_message = ''
            for holidate, holiday_occasion in configs['OFFICE_HOLIDAYS'].items():
                if self.today_date_mm_only == holidate[3:5]:
                    if not text_message:
                        text_message += "Office Holidays this Month:\n"
                    text_message += f"{holidate}: {holiday_occasion}\n"
            if text_message:
                print(text_message.strip())
                telegram_send_msg(text_message.strip())

    def monthly_working_days_counts(self):
        if self.today_date_dd_only == configs['every_month_remind_date'][:-8]:
            # Get number of working days in a month (excludes Saturdays & Sundays)
            month_working_days = np.busday_count(self.today_date_yyyy_only + '-' + self.today_date_mm_only,
                                                 self.today_date_yyyy_only + '-' + f'{int(self.today_date_mm_only)+1:02d}')
            next_month_working_days = np.busday_count(self.today_date_yyyy_only + '-' + f'{int(self.today_date_mm_only) + 1:02d}',
                                                 self.today_date_yyyy_only + '-' + f'{int(self.today_date_mm_only) + 2:02d}')
            sixty_percent_days = math.ceil(month_working_days * 0.6)
            next_month_sixty_percent_days = math.ceil(next_month_working_days * 0.6)
            text_message = (
                f"This Month: {self.today_date_mm_only}, {self.today_date_yyyy_only}\n"
                f"Working days for this month: {month_working_days} days\n"
                f"Sixty percent attendance: {sixty_percent_days} days\n\n"
                f"Next Month: {int(self.today_date_mm_only)+1:02d}, {self.today_date_yyyy_only}\n"
                f"Working days for next month: {next_month_working_days} days\n"
                f"Sixty percent attendance: {next_month_sixty_percent_days} days"
            )
            print(text_message)
            telegram_send_msg(text_message)

    def weekly_news_notification(self):
        # Trigger weekly news notification only on Friday. 4 Denotes Friday
        if datetime.today().weekday() == 4:
            # Get Saturday date of previous week
            last_saturday_date = (datetime.now() - timedelta(days=(datetime.now().weekday() - 5)%7)).strftime('%Y-%m-%d')
            # NewsAPI service to get the news
            newsapi_url = f"https://newsapi.org/v2/top-headlines?country=in&sortBy=popularity&apiKey={configs['NEWSAPI_API_KEY']}&from={last_saturday_date}&category={configs['NEWS_CATEGORY']}"
            response = requests.get(newsapi_url)
            if response.status_code == 200:
                data = response.json()
                articles = data['articles']
                text_message = f"{configs['NEWS_CATEGORY'].capitalize()} Weekly News:\n\n"
                for article in articles:
                    text_message += f'<a href="{article["url"]}">{article["title"]}</a>\n\n'
                # print(text_message)
                telegram_send_msg(text_message, is_parse_html=True)

    def get_current_top_headlines_news(self):
        # NewsAPI service to get the news
        newsapi_url = f"https://newsapi.org/v2/top-headlines?country=in&sortBy=popularity&apiKey={configs['NEWSAPI_API_KEY']}"
        response = requests.get(newsapi_url)
        if response.status_code == 200:
            data = response.json()
            articles = data['articles']
            text_message = f"Top Headlines News:\n\n"
            for article in articles:
                text_message += f'<a href="{article["url"]}">{article["title"]}</a>\n\n'
            # print(text_message)
            telegram_send_msg(text_message, is_parse_html=True)
        return "News links are clicable to the source !!!"

    def run_command_bot(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message, "Howdy, how are you doing?")

        @self.bot.message_handler(commands=['help'])
        def help_command(message):
            markup = types.InlineKeyboardMarkup(row_width=2)
            button = types.InlineKeyboardButton(text="Click Me", callback_data="button_clicked")
            top_headlines = types.InlineKeyboardButton(text="Top Headlines News", callback_data="top_headlines")
            markup.add(button, top_headlines)
            self.bot.send_message(chat_id=message.chat.id, text="how are you doing?", reply_markup=markup)
        
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            if call.data == "button_clicked":
                self.bot.send_message(call.message.chat.id, "Button clicked!")
            elif call.data == "top_headlines":
                self.bot.send_message(call.message.chat.id, self.get_current_top_headlines_news())
        
        self.bot.polling()


if __name__ == "__main__":
    notify_obj = Notifier(configs)
    notify_obj.is_birthday_today()
    notify_obj.is_monthly_reminder_today()
    notify_obj.is_any_office_holiday_this_month()
    notify_obj.monthly_working_days_counts()
    notify_obj.weekly_news_notification()
    notify_obj.run_command_bot()
