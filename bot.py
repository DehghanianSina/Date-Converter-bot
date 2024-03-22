import re
from dateutil import parser
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

import datetime 
from khayyam import JalaliDatetime, JalaliDate as GregorianDatetime

LRM = '\u200E'
RLM = '\u200F'
footer = '''
\-\-\-
@myDateConverterBot
'''

def convert_date_text(input_date):
    try:
        # Extract year, month, and day using regex
        matches = re.findall(r'\b\d{1,4}\b', input_date)
        if len(matches) != 3:
            raise ValueError("Invalid date format")

        year, month, day = map(int, matches)

        # Determine likely era based on the year
        era = "Jalali" if 1200 <= year <= 1500 else "Gregorian" if 1900 <= year <= 2100 else None

        if era == "Jalali":
            # Try parsing as Jalali date using khayyam
            jalali_datetime = JalaliDatetime(year, month, day)

            # Convert to Gregorian date
            gregorian_date = jalali_datetime.todate()
            gregorian_formatted = gregorian_date.strftime('%Y-%m-%d')
            
            output = f'''*input* \({era}\):\n`{jalali_datetime.strftime('%Y-%m-%d')}`\n\n*output* \(Gregorian\):\n`{gregorian_formatted}`\n{gregorian_date.strftime("%B")}

            `{jalali_datetime.strftime("%A")}, {jalali_datetime.strftime("%d")} {jalali_datetime.strftime("%B")} {jalali_datetime.strftime("%Y")}`

`{gregorian_date.strftime("%A")}, {gregorian_date.strftime("%d")} {gregorian_date.strftime("%B")} {gregorian_date.strftime("%Y")}`
            
            {footer}
            '''

            return output

        elif era == "Gregorian":
            # Try parsing as Gregorian date
            gregorian_date = datetime.datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')
            #parser.parse(input_date)

            # Convert to Jalali date
            jalali_date = JalaliDatetime(gregorian_date)
            jalali_formatted = jalali_date.strftime('%Y/%m/%d')

            #return f'''*input* \({era}\):\n`{gregorian_date.strftime('%Y-%m-%d')}`\n\n*output* \(Jalali\):\n`{jalali_formatted}`\n{jalali_date.strftime("%B")}'''
        
            output = f'''*input* \({era}\):\n`{gregorian_date.strftime('%Y-%m-%d')}`\n\n*output* \(Jalali\):\n`{jalali_formatted}`\n{jalali_date.strftime("%B")}
            
            `{gregorian_date.strftime("%A")}, {gregorian_date.strftime("%d")} {gregorian_date.strftime("%B")} {gregorian_date.strftime("%Y")}`
            
`{jalali_date.strftime("%A")}, {jalali_date.strftime("%d")} {jalali_date.strftime("%B")} {jalali_date.strftime("%Y")}`
            
            {footer}
            '''

            return output

        return "Invalid date format. Please use a valid date format."

    except ValueError:
        return "Invalid date format. Please use a valid date format."

def convert_date(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    converted_date = convert_date_text(user_input)
    update.message.reply_text(converted_date,parse_mode='MarkdownV2')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Send me a date, and I'll convert it for you.")

def main() -> None:
    # Set your Telegram Bot Token here
    token = '6914421890:AAHgHbqvEGJ6Qs6YWoDw3ubi1yVi9PHtFUA'
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))

    # Message handler for non-command text
    dp.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, convert_date))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
