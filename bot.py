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
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text.strip()  # remove trailing whitespace/newlines
    except Exception as e:
        return f"Weather unavailable ({e})"


# -- FUNCTION 2: Quote -----------------------------------------------------
def get_quote():
    """Fetch a random motivational quote from ZenQuotes."""
    url = "https://zenquotes.io/api/random"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()         # converts JSON text to a Python list
        quote = data[0]["q"]           # the quote text
        author = data[0]["a"]          # the author name
        return f"'{quote}' - {author}"
    except Exception as e:
        return f"Quote unavailable ({e})"


# -- FUNCTION 3: Build the summary -----------------------------------------
def build_summary():
    """Assemble the full daily summary and wrap it in HTML/CSS styling."""
    today = date.today().strftime("%A, %d %B %Y")
    weather = get_weather()
    quote = get_quote()

    # We use HTML and inline CSS to add layout, backgrounds, fonts, and colors!
    html_summary = f"""
    <html>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; padding: 20px; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); overflow: hidden; border: 1px solid #e1e8ed;">
            
            <!-- Header Section -->
            <div style="background: linear-gradient(135deg, #4A00E0, #8E2DE2); padding: 30px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 28px; letter-spacing: 1px; font-weight: 600;">PULSE</h1>
                <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 14px;">{today}</p>
            </div>
            
            <!-- Content Container -->
            <div style="padding: 30px;">
                
                <!-- Weather Section -->
                <div style="margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #f0f0f0;">
                    <h3 style="margin: 0 0 10px 0; color: #4A00E0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">🌤️ Current Weather</h3>
                    <div style="font-size: 18px; color: #2c3e50; font-weight: 500; background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #4A00E0;">
                        {weather}
                    </div>
                </div>
                
                <!-- Quote Section -->
                <div>
                    <h3 style="margin: 0 0 10px 0; color: #8E2DE2; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">✨ Daily Inspiration</h3>
                    <div style="background-color: #fdf8ff; padding: 20px; border-radius: 8px; border-left: 4px solid #8E2DE2; font-style: italic;">
                        <p style="margin: 0; font-size: 16px; line-height: 1.6; color: #444;">{quote}</p>
                    </div>
                </div>
                
            </div>
            
            <!-- Footer Section -->
            <div style="background-color: #fafafa; text-align: center; padding: 15px; font-size: 11px; color: #999; border-top: 1px solid #f0f0f0;">
                Automated daily brief generated via GitHub Actions.
            </div>
            
        </div>
    </body>
    </html>
    """
    return html_summary


# -- FUNCTION 4: Send Email ------------------------------------------------
def send_email(summary_html):
    """Send the completed summary as an HTML email using GitHub Secrets."""
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD") 
    receiver = os.environ.get("EMAIL_RECEIVER")
    
    if not all([sender, password, receiver]):
        print("Error: Missing one or more email environment variables. Skipping email step.")
        return

    # CRITICAL CHANGE: Changed 'plain' to 'html' so email clients render the code's colors/designs
    msg = MIMEText(summary_html, 'html', 'utf-8')
    msg['Subject'] = '✨ Pulse - Your Daily Summary'
    msg['From'] = sender
    msg['To'] = receiver
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

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