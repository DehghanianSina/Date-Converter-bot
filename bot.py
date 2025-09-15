import re
import os
import logging
import datetime
from typing import Optional, Tuple

# Use jdatetime library as a replacement for khayyam
import jdatetime
from telegram import Update
# Imports compatible with python-telegram-bot v13.x
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Constants
footer = '''
\-\-\-
@myDateConverterBot
'''

def escape_markdown_v2(text: str) -> str:
    """Escapes characters for Telegram's MarkdownV2."""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def extract_date_components(input_date: str) -> Optional[Tuple[int, int, int]]:
    """
    Extract year, month, and day from a date string.
    Returns None if the format is invalid.
    """
    try:
        # Find all sequences of digits in the input string
        matches = re.findall(r'\d+', input_date)
        if len(matches) >= 3:
            # Assume the first three numbers are year, month, day
            return int(matches[0]), int(matches[1]), int(matches[2])
    except (ValueError, IndexError):
        return None
    return None

def determine_date_era(year: int) -> str:
    """
    Determines the calendar system based on the year.
    This is a heuristic: years below 1600 are assumed to be Jalali,
    and years above are assumed to be Gregorian in user inputs.
    """
    if year < 1600:
        return "Jalali"
    else:
        return "Gregorian"

def convert_date_text(input_date: str) -> str:
    """
    Convert a date between Gregorian and Jalali calendars.
    """
    date_components = extract_date_components(input_date)
    
    if not date_components:
        return escape_markdown_v2("Invalid date format. Please use a format like YYYY-MM-DD.")

    year, month, day = date_components
    
    try:
        era = determine_date_era(year)

        if era == "Jalali":
            return convert_jalali_to_gregorian(year, month, day)
        elif era == "Gregorian":
            return convert_gregorian_to_jalali(year, month, day)
            
    except ValueError as e:
        logger.error(f"Error converting date '{input_date}': {str(e)}")
        return escape_markdown_v2(f"Error: The date you entered seems to be invalid. Please check it and try again.")

def convert_jalali_to_gregorian(year: int, month: int, day: int) -> str:
    """
    Convert a Jalali date to Gregorian using jdatetime.
    """
    # Set locale for jdatetime to get Persian month/day names
    jdatetime.set_locale('fa_IR')
    jalali_date = jdatetime.date(year, month, day)
    gregorian_date = jalali_date.togregorian()
    
    jalali_ymd = jalali_date.strftime('%Y-%m-%d')
    gregorian_ymd = gregorian_date.strftime('%Y-%m-%d')

    # Full-text date formats
    jalali_full = jalali_date.strftime("%A, %d %B %Y")
    gregorian_full = gregorian_date.strftime("%A, %d %B %Y")
    gregorian_month_name = gregorian_date.strftime("%B")
    
    return f'''*Input* \(Jalali\):\n`{escape_markdown_v2(jalali_ymd)}`\n\n*Output* \(Gregorian\):\n`{escape_markdown_v2(gregorian_ymd)}`\n{escape_markdown_v2(gregorian_month_name)}
            
`{escape_markdown_v2(jalali_full)}`

`{escape_markdown_v2(gregorian_full)}`
            
{footer}
            '''

def convert_gregorian_to_jalali(year: int, month: int, day: int) -> str:
    """
    Convert a Gregorian date to Jalali using jdatetime.
    """
    # Set locale for jdatetime to get Persian month/day names
    jdatetime.set_locale('fa_IR')
    gregorian_date = datetime.date(year, month, day)
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
    
    gregorian_ymd = gregorian_date.strftime('%Y-%m-%d')
    jalali_ymd = jalali_date.strftime('%Y/%m/%d')
    
    # Full-text date formats
    gregorian_full = gregorian_date.strftime("%A, %d %B %Y")
    jalali_full = jalali_date.strftime("%A, %d %B %Y")
    jalali_month_name = jalali_date.strftime("%B")

    return f'''*Input* \(Gregorian\):\n`{escape_markdown_v2(gregorian_ymd)}`\n\n*Output* \(Jalali\):\n`{escape_markdown_v2(jalali_ymd)}`\n{escape_markdown_v2(jalali_month_name)}
            
`{escape_markdown_v2(gregorian_full)}`

`{escape_markdown_v2(jalali_full)}`
            
{footer}
            '''

def convert_date_handler(update: Update, context: CallbackContext) -> None:
    """
    Handle incoming date conversion requests.
    """
    if not update.message or not update.message.text:
        return
        
    user_input = update.message.text
    logger.info(f"Received date conversion request: {user_input}")
    converted_date = convert_date_text(user_input)
    update.message.reply_text(converted_date, parse_mode='MarkdownV2')

def start(update: Update, context: CallbackContext) -> None:
    """
    Handle the /start command.
    """
    welcome_message = """
Welcome to the Date Converter Bot! 🗓️

I can convert dates between Gregorian and Jalali (Persian) calendars.

Just send me a date in either format with any arbitrary separator, and I'll convert it for you.

Examples:
- 1404-04-04 (Jalali)
- 2025-06-25 (Gregorian)
"""
    update.message.reply_text(welcome_message)
    logger.info("Bot started by user")

def main() -> None:
    """
    Main function to start the bot using Updater class for v13.x.
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set!")
        return

    logger.info("Starting bot...")
    # Use Updater and dispatcher for v13.x
    updater = Updater(token)
    dp = updater.dispatcher

    # Add handlers to the dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, convert_date_handler))

    # Start the Bot
    updater.start_polling()
    logger.info("Bot started successfully")

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
