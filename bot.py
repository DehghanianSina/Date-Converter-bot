import re
import os
import logging
from typing import Optional, Tuple
from dateutil import parser
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

import datetime 
from khayyam import JalaliDatetime, JalaliDate as GregorianDatetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Constants
LRM = '\u200E'
RLM = '\u200F'
footer = '''
\-\-\-
@myDateConverterBot
'''

def extract_date_components(input_date: str) -> Tuple[int, int, int]:
    """
    Extract year, month, and day from a date string.
    
    Args:
        input_date (str): The input date string
        
    Returns:
        Tuple[int, int, int]: A tuple containing (year, month, day)
        
    Raises:
        ValueError: If the date format is invalid
    """
    matches = re.findall(r'\b\d{1,4}\b', input_date)
    if len(matches) != 3:
        raise ValueError("Invalid date format")
    return tuple(map(int, matches))

def determine_date_era(year: int) -> Optional[str]:
    """
    Determine the calendar era based on the year.
    
    Args:
        year (int): The year to check
        
    Returns:
        Optional[str]: 'Jalali', 'Gregorian', or None
    """
    if 1200 <= year <= 1500:
        return "Jalali"
    elif 1900 <= year <= 2100:
        return "Gregorian"
    return None

def convert_date_text(input_date: str) -> str:
    """
    Convert a date between Gregorian and Jalali calendars.
    
    Args:
        input_date (str): The input date string
        
    Returns:
        str: The converted date in a formatted string
        
    Raises:
        ValueError: If the date format is invalid
    """
    try:
        year, month, day = extract_date_components(input_date)
        era = determine_date_era(year)

        if era == "Jalali":
            return convert_jalali_to_gregorian(year, month, day)
        elif era == "Gregorian":
            return convert_gregorian_to_jalali(year, month, day)

        return "Invalid date format. Please use a valid date format."

    except ValueError as e:
        logger.error(f"Error converting date: {str(e)}")
        return f"Error: {str(e)}. Please use a valid date format."

def convert_jalali_to_gregorian(year: int, month: int, day: int) -> str:
    """
    Convert a Jalali date to Gregorian.
    
    Args:
        year (int): Jalali year
        month (int): Jalali month
        day (int): Jalali day
        
    Returns:
        str: Formatted output string
    """
    jalali_datetime = JalaliDatetime(year, month, day)
    gregorian_date = jalali_datetime.todate()
    gregorian_formatted = gregorian_date.strftime('%Y-%m-%d')
    
    return f'''*input* \(Jalali\):\n`{jalali_datetime.strftime('%Y-%m-%d')}`\n\n*output* \(Gregorian\):\n`{gregorian_formatted}`\n{gregorian_date.strftime("%B")}

            `{jalali_datetime.strftime("%A")}, {jalali_datetime.strftime("%d")} {jalali_datetime.strftime("%B")} {jalali_datetime.strftime("%Y")}`

`{gregorian_date.strftime("%A")}, {gregorian_date.strftime("%d")} {gregorian_date.strftime("%B")} {gregorian_date.strftime("%Y")}`
            
            {footer}
            '''

def convert_gregorian_to_jalali(year: int, month: int, day: int) -> str:
    """
    Convert a Gregorian date to Jalali.
    
    Args:
        year (int): Gregorian year
        month (int): Gregorian month
        day (int): Gregorian day
        
    Returns:
        str: Formatted output string
    """
    gregorian_date = datetime.datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')
    jalali_date = JalaliDatetime(gregorian_date)
    jalali_formatted = jalali_date.strftime('%Y/%m/%d')

    return f'''*input* \(Gregorian\):\n`{gregorian_date.strftime('%Y-%m-%d')}`\n\n*output* \(Jalali\):\n`{jalali_formatted}`\n{jalali_date.strftime("%B")}
            
            `{gregorian_date.strftime("%A")}, {gregorian_date.strftime("%d")} {gregorian_date.strftime("%B")} {gregorian_date.strftime("%Y")}`
            
`{jalali_date.strftime("%A")}, {jalali_date.strftime("%d")} {jalali_date.strftime("%B")} {jalali_date.strftime("%Y")}`
            
            {footer}
            '''

def convert_date(update: Update, context: CallbackContext) -> None:
    """
    Handle incoming date conversion requests.
    
    Args:
        update (Update): The update object from Telegram
        context (CallbackContext): The context object from Telegram
    """
    user_input = update.message.text
    logger.info(f"Received date conversion request: {user_input}")
    converted_date = convert_date_text(user_input)
    update.message.reply_text(converted_date, parse_mode='MarkdownV2')

def start(update: Update, context: CallbackContext) -> None:
    """
    Handle the /start command.
    
    Args:
        update (Update): The update object from Telegram
        context (CallbackContext): The context object from Telegram
    """
    welcome_message = """
Welcome to the Date Converter Bot! 🗓️

I can convert dates between Gregorian and Jalali (Persian) calendars.

Just send me a date in either format, and I'll convert it for you!

Examples:
- 1403-01-01 (Jalali)
- 2024-03-21 (Gregorian)
"""
    update.message.reply_text(welcome_message)
    logger.info("Bot started by user")

def main() -> None:
    """
    Main function to start the bot.
    """
    # Get the Telegram Bot Token from environment variables
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set!")
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set!")

    logger.info("Starting bot...")
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))

    # Message handler for non-command text
    dp.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, convert_date))

    # Start the Bot
    updater.start_polling()
    logger.info("Bot started successfully")

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
