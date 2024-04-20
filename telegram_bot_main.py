# Simple Python Script - Birthday Notification Reminder Telegram Bot
# Authored by - Vinay Kumar Sahu | Email: vinaykumar.sahu093@gmail.com | Insta ID: me_vinay_sahu
'''
This is simple Python script bot to get birthday reminder on Telegram of your beloved ones.
Easy to configure & deploy.
------- Follow the Guidelines below ----------

1. No Installation required
2. Create your Telegram API KEY with "BotFather"
3. Get your CHAT ID with this link: https://api.telegram.org/bot<API_KEY>/getUpdates
4. Add these two values to the script
5. Add the birthdates in form of dictionary to the script
6. Visit here to Host for free: https://www.pythonanywhere.com/
7. Upload the script in "Files" section
8. Schedule the script in "Tasks" section

You are good to go now !!! (Reachout if case of any queries)
'''

import pytz, requests, traceback, math
import numpy as np
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

configs = {
    'TELEGRAM_API_KEY': '',
    'TELEGRAM_CHAT_ID': '',
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
        '03-03-1993': 'Daddy & Mummy Anniversary',
        '30-04-1993': 'Bhaiya & Bhabi Anniversary',
        '27-01-2022': 'Vinay & Lipika Anniversary',
        '22-01-2023': 'Jai Shree Ram',
        '10-05-1995': 'Basuki',
        '03-03-2023': 'Prahalad ADP',
        '14-04-1997': 'Abhinav ADP',
        '25-11-2023': 'Bhakti ADP',
        '12-05-2024': 'Mother day',
    },
    'REMIND_DATES': {
        '04-01-2023': 'Upcoming payments for:\n'
                      '- House Rent - GPay\n'
                      '- House Maintenance - PhonePe\n'
                      '- Electricity Payment - Cred/PhonePe\n'
                      '- Internet Bill - Cred/AirtelApp\n'
                      '- Credit Card Bills Payment - Cred\n'
                      '- Do Investments\n'
    },
    'every_month_remind_date': '02-01-2023',
}

consts = {
    'timezone': 'Asia/kolkata',
}


# https://api.telegram.org/bot6649388608:AAGUSudo-eCJy1_iV4mrTk5UfkYuV_7gQNo/getUpdates
def telegram_send_msg(text_message=''):
    try:
        url = f"https://api.telegram.org/bot{configs['TELEGRAM_API_KEY']}/sendMessage?chat_id={configs['TELEGRAM_CHAT_ID']}&text={text_message}"
        print(requests.get(url).json())  # this sends the message

    except Exception as e:
        print('Exception while sending msg', e)
        print(traceback.format_exc())


class Notifier:

    def __init__(self, configs):
        self.prior_reminder_flag = False
        self.no_of_days_before_reminder = 1
        self.today_date = datetime.now(pytz.timezone(consts['timezone'])).strftime("%d-%m")
        self.today_date_dd_only = datetime.now(pytz.timezone(consts['timezone'])).strftime("%d")
        self.today_date_mm_only = datetime.now(pytz.timezone(consts['timezone'])).strftime("%m")
        self.today_date_yyyy_only = datetime.now(pytz.timezone(consts['timezone'])).strftime("%Y")
        self.birthdates = configs['BIRTHDATES']
        self.remind_dates = configs['REMIND_DATES']

    def calculate_age(self, dob_str):
        dob = datetime.strptime(dob_str, '%d-%m-%Y')
        age = relativedelta(date.today(), dob)
        return age.years

    def trigger_birthday_notification(self, birthdate, birthday_person):
        print(f"Today's Date: {self.today_date}")
        text_message = (
            f"Birthday Reminder of {birthday_person}\n"
            f"Birthdate: {birthdate}\n"
            f"Age: {self.calculate_age(birthdate)}"
        )
        print(text_message)
        telegram_send_msg(text_message)

    def trigger_reminder_notification(self, remind_date, remind_thing):
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
        for birthdate, birthday_person in self.birthdates.items():
            if self.prior_reminder_flag and self.remind_before_birthdate(birthdate, self.no_of_days_before_reminder):
                self.trigger_birthday_notification(birthdate, birthday_person)
            # Get only the day and month part of the date
            if self.today_date == birthdate[:-5]:
                self.trigger_birthday_notification(birthdate, birthday_person)

    def is_monthly_reminder_today(self):
        for remind_date, remind_thing in self.remind_dates.items():
            # Get only the day part of the date
            if self.today_date_dd_only == remind_date[:-8]:
                self.trigger_reminder_notification(remind_date, remind_thing)

    def monthly_working_days_counts(self):
        if self.today_date_dd_only == configs['every_month_remind_date'][:-8]:
            # Get number of working days in a month (excludes Saturdays & Sundays)
            month_working_days = np.busday_count(self.today_date_yyyy_only + '-' + self.today_date_mm_only,
                                                 self.today_date_yyyy_only + '-' + f'{int(self.today_date_mm_only)+1:02d}')
            sixty_percent_days = math.ceil(month_working_days * 0.6)
            text_message = (
                f"Month: {self.today_date_mm_only}, {self.today_date_yyyy_only}\n"
                f"Working days for this month: {month_working_days} days\n"
                f"Sixty percent attendance: {sixty_percent_days} days"
            )
            print(text_message)
            telegram_send_msg(text_message)


if __name__ == "__main__":
    notify_obj = Notifier(configs)
    notify_obj.is_birthday_today()
    notify_obj.is_monthly_reminder_today()
    notify_obj.monthly_working_days_counts()
