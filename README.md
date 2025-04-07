# Date Converter Telegram Bot

A Telegram bot that converts dates between Gregorian and Jalali (Persian) calendars.

## Features

- Convert dates between Gregorian and Jalali calendars
- Automatic detection of input date format
- Detailed output including day names and month names
- Support for both Gregorian and Jalali date formats
- Simple and user-friendly interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sina.dehghanian/Date_Converter_bot.git
cd Date_Converter_bot
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root and add your Telegram bot token:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

## Usage

1. Start the bot:
```bash
python bot.py
```

2. In Telegram:
- Start a chat with your bot
- Send any date in either Gregorian or Jalali format
- The bot will automatically detect the format and convert it to the other calendar

## Examples

- Input: `1403-01-01` (Jalali)
- Output: Will show the corresponding Gregorian date

- Input: `2024-03-21` (Gregorian)
- Output: Will show the corresponding Jalali date

## Supported Date Formats

The bot supports various date formats:
- YYYY-MM-DD (e.g., 1403-01-01)
- YYYY/MM/DD (e.g., 1403/01/01)
- YYYY.MM.DD (e.g., 1403.01.01)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Here's how you can contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

This project uses the following libraries:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - For Telegram bot functionality
- [Khayyam](https://github.com/pylover/khayyam) - For Jalali date conversion
- [python-dateutil](https://github.com/dateutil/dateutil) - For date parsing

## Support

If you encounter any issues or have questions, please:
1. Check the [Issues](https://github.com/sina.dehghanian/Date_Converter_bot/issues) page
2. Create a new issue if your problem isn't listed
3. Contact the maintainer at [sina.dehghanian@gmail.com](mailto:sina.dehghanian@gmail.com)

## Author

- **sina.dehghanian** - *Initial work* - [GitHub](https://github.com/sina.dehghanian)
