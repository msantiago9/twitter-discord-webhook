# twitter-discord-webhook

Webscraper that you can run locally on a Windows computer. Fetches tweets from your provided twitter account and sends them to your provided discord webhook. This application uses **[sntwitter](https://github.com/JustAnotherArchivist/snscrape/tree/master)** to scrape tweets instead of using the Twitter API. This eliminates the need for authentication with a Twitter account or API Token, and is also free. **[See here](https://discord.com/developers/docs/resources/webhook)** for Discord Webhook documentation.

## Prerequisites/Limitations:

1. Can only run in background on Windows Machine. a Bash script might come later.
2. Need to have Python 3 installed first. App is confirmed to work on 3.11.1. **[Go here](https://www.python.org/downloads/)**.

## How to run on `Windows`:

1. Edit config.txt
2. run start.bat

## How to stop on `Windows`:

1. run stop.bat

## How to run on `Linux/MacOS`:

1. run `py -m venv venv` to create a virtual environment.
2. run `./venv/Scripts/activate` to activate virtual environment.
3. run `pip install -r requirements.txt` to install python packages.
4. edit `config.txt` with your desired WEBHOOK_URL and TWITTER_HANDLE.
5. run `py twitter-discord-webhook.py` to run the application.
