# Gmail Invoice Downloader

A Python script that automatically downloads invoice PDFs from Gmail and organises them into monthly folders.

## What it does

- Searches Gmail for invoice emails from your configured senders
- Downloads PDF attachments
- Saves them into organised monthly folders like `invoices/2026-01/`
- Skips invoices already downloaded — safe to run every month
- Supports a month offset for senders who bill in arrears (e.g. Google sends a February email for a January billing period)

## Folder structure

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
    ("Google", "from:payments-noreply@google.com has:attachment after:2026/01/01", -1),
    ("My Host", "from:billing@myhost.com has:attachment after:2026/01/01", 0),
]
```

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

--- Searching for Google invoices ---
Found 2 email(s) from Google.
  Saved: invoices/2026-01/invoice_jan.pdf

--- Searching for My Host invoices ---
Found 1 email(s) from My Host.
  Saved: invoices/2026-02/invoice_feb.pdf

=== Done! Downloaded 2 invoice(s) total. ===
```

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
