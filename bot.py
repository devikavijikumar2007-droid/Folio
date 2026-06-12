# Pulse - Daily Summary Bot
# Fetches: weather (wttr.in) + a quote (zenquotes.io)
# Runs:    every day at 8 AM IST via GitHub Actions
# APIs:    both free, no API keys needed

import requests
from datetime import date
import smtplib
from email.mime.text import MIMEText
import os


# -- FUNCTION 1: Weather ----------------------------------------------------
def get_weather(city="Thiruvananthapuram"):
    """Fetch today's weather as a one-line text summary."""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()  # remove trailing whitespace/newlines
    except Exception as e:
        return f"Weather unavailable ({e})"


# -- FUNCTION 2: Quote -----------------------------------------------------
def get_quote():
    """Fetch a random motivational quote from ZenQuotes."""
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()         # converts JSON text to a Python list
        quote = data[0]["q"]           # the quote text
        author = data[0]["a"]          # the author name
        return f"'{quote}' - {author}"
    except Exception as e:
        return f"Quote unavailable ({e})"


# -- FUNCTION 3: Build the summary -----------------------------------------
def build_summary():
    """Assemble the full daily summary from all data sources."""
    today = date.today().strftime("%A, %d %B %Y")  # e.g. Monday, 09 June 2026
    weather = get_weather()
    quote = get_quote()

    # Triple-quoted strings span multiple lines - great for formatted output
    summary = f"""=====================================
PULSE - Daily Summary
{today}
=====================================

WEATHER
{weather}

TODAY'S QUOTE
{quote}

====================================="""

    return summary


# -- FUNCTION 4: Send Email ------------------------------------------------
def send_email(summary_text):
    """Send the completed summary to your email using GitHub Secrets."""
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD") # Gmail App Password
    receiver = os.environ.get("EMAIL_RECEIVER")
    
    msg = MIMEText(summary_text)
    msg['Subject'] = 'Pulse - Daily Summary'
    msg['From'] = sender
    msg['To'] = receiver
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
    print("Email sent.")


# -- FUNCTION 5: Run everything --------------------------------------------
def run():
    """Main entry point. Called by GitHub Actions."""
    summary = build_summary()

    # Print to the GitHub Actions log (visible in the Actions tab)
    print(summary)

    # Save to a file (uploaded as a downloadable artifact by the workflow)
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
        
    # Send the automated email summary
    send_email(summary)
    print("Pulse ran successfully.")


# -- Entry point guard ------------------------------------------------------
# Only runs when you execute: python bot.py
if __name__ == "__main__":
    run()