FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Long-polls Telegram and calls the Anthropic API - no inbound port needed.
CMD ["python", "run_telegram_bot.py"]
