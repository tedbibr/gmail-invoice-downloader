# Copy this file to config.py and fill in your own values.
# config.py is listed in .gitignore and will never be uploaded to GitHub.

# Only download invoices received after this date
START_DATE = "2026/01/01"

# List of invoice senders to search for in Gmail.
# Each entry: (display_name, Gmail_search_query, month_offset)
#
# month_offset:
#   0  = invoice is for the same month the email arrived
#  -1  = invoice is for the PREVIOUS month
#        (use this for senders who bill in arrears — e.g. Google sends
#         a February email for a January billing period)
#
# Tip: test your search query in Gmail's search bar first.
SEARCH_QUERIES = [
    ("Sender 1", f"from:billing@example.com has:attachment after:{START_DATE}", 0),
    ("Sender 2", f"from:invoices@example.com has:attachment after:{START_DATE}", -1),
]
