import re
from dateutil import parser
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from khayyam import JalaliDatetime, JalaliDate as GregorianDatetime


def convert_date_text(input_date):
    try:
        # Extract year from the input using regex
        year_match = re.search(r'\b\d{2,4}\b', input_date)
        if year_match:
            year = int(year_match.group())
            
            # Determine likely era based on the year
            era = "Jalali" if 1200 <= year <= 1500 else "Gregorian" if 1900 <= year <= 2100 else None

            if era == "Jalali":
                # Try parsing as Jalali date using khayyam
                jalali_datetime = JalaliDatetime.strptime(input_date, '%Y/%m/%d')
                
                # Convert to Gregorian date
                gregorian_date = jalali_datetime.todate()
                gregorian_formatted = gregorian_date.strftime('%Y/%m/%d')

                return f'{input_date} ({era}) => {gregorian_formatted} (Gregorian)'
            
            elif era == "Gregorian":
                # Try parsing as Gregorian date
                parsed_gregorian_date = parser.parse(input_date)
                
                # Convert to Jalali date
                jalali_date = JalaliDatetime(parsed_gregorian_date)
                jalali_formatted = jalali_date.strftime('%Y/%m/%d')

                return f'{input_date} ({era}) => {jalali_formatted} (Jalali)'

        return "Invalid date format. Please use a valid date format."

    except ValueError:
        return "Invalid date format. Please use a valid date format."

def convert_date(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    converted_date = convert_date_text(user_input)
    update.message.reply_text(converted_date)

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
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, convert_date))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
