# Gmail Invoice Downloader

> Stop hunting through your inbox for invoice PDFs. This script does it for you.

Automatically searches Gmail for invoice emails from your configured senders, downloads the PDF attachments, and saves them into organised monthly folders.

## What it does

- Searches Gmail for invoice emails from your configured senders
- Downloads PDF attachments
- Saves them into organised monthly folders like `invoices/2026-01/`
- Skips invoices already downloaded — safe to run every month
- Supports a month offset for senders who bill in arrears (e.g. a February email for a January billing period)

```
invoices/
├── 2026-01/
│   ├── invoice_a.pdf
│   └── invoice_b.pdf
└── 2026-02/
    └── invoice_c.pdf
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/tedbibr/gmail-invoice-downloader.git
cd gmail-invoice-downloader
```

### 2. Install dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Set up Gmail API credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (e.g. "Invoice Downloader")
3. Enable the **Gmail API**
4. Go to **APIs & Services → Credentials**
5. Create an **OAuth 2.0 Client ID** (Desktop app)
6. Download the JSON file and save it as `credentials/credentials.json`

### 4. Configure your senders

```bash
cp config.example.py config.py
```

Open `config.py` and fill in your senders:

```python
START_DATE = "2026/01/01"

SEARCH_QUERIES = [
    ("Sender 1", f"from:billing@example.com has:attachment after:{START_DATE}", 0),
    ("Sender 2", f"from:invoices@example.com has:attachment after:{START_DATE}", -1),
]
```

The third value in each entry is the `month_offset`:
- `0` — invoice is for the same month the email arrived
- `-1` — invoice is for the previous month (for senders who bill in arrears)

> **Tip:** Test your search query in Gmail's search bar first to confirm it finds the right emails.

> **Note:** `config.py` is listed in `.gitignore` — your personal configuration is never uploaded to GitHub.

## Usage

```bash
python3 main.py
```

The first time you run it, a browser window opens asking you to grant Gmail read-only access. After that it runs silently.

## Example output

```
Connecting to Gmail...

--- Searching for Sender 1 invoices ---
Found 2 email(s) from Sender 1.
  Saved: invoices/2026-01/invoice_jan.pdf

--- Searching for Sender 2 invoices ---
Found 1 email(s) from Sender 2.
  Saved: invoices/2026-02/invoice_feb.pdf

=== Done! Downloaded 2 invoice(s) total. ===
```

## Scheduling

The script runs on macOS, Linux, and Windows. To run it automatically every month, use your OS's built-in scheduler:

- **macOS** — `launchd` (via a `.plist` file in `~/Library/LaunchAgents/`)
- **Linux** — `cron` (`crontab -e`)
- **Windows** — Task Scheduler

## Security

- Gmail credentials are stored **only on your computer** in `credentials/`
- Your sender config is stored **only on your computer** in `config.py`
- The script requests **read-only** Gmail access — it cannot send, delete, or modify anything
- `credentials/`, `invoices/`, and `config.py` are excluded from Git via `.gitignore`

## Requirements

- Python 3.8+
- A Gmail account
- A Google Cloud project with the Gmail API enabled

## Contributing

Pull requests welcome!
