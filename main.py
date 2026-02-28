import os
import base64
from datetime import datetime
from email.utils import parsedate_to_datetime
from auth import get_gmail_service
from config import SEARCH_QUERIES

# Where to save the downloaded invoices
INVOICES_DIR = "invoices"


def get_email_date(message, month_offset=0):
    """
    Looks at an email and figures out when it was sent.
    Applies month_offset to adjust for billing periods.
    Returns the date as a string like "2025-01" (year-month).
    """
    headers = message["payload"]["headers"]

    date = None
    for header in headers:
        if header["name"] == "Date":
            date = parsedate_to_datetime(header["value"])
            break

    # If no date found, use today's date as fallback
    if date is None:
        date = datetime.now()

    # Apply the month offset (e.g., -1 means "previous month")
    if month_offset != 0:
        # Calculate new month and year, handling year boundaries
        new_month = date.month + month_offset
        new_year = date.year
        while new_month < 1:
            new_month += 12
            new_year -= 1
        while new_month > 12:
            new_month -= 12
            new_year += 1
        date = date.replace(year=new_year, month=new_month, day=1)

    return date.strftime("%Y-%m")


def download_attachments(service, message_id, folder, month_offset=0):
    """
    Takes one email, finds all PDF attachments, and saves them to a folder.
    Returns how many PDFs were downloaded.
    """
    # Get the full email details
    message = service.users().messages().get(
        userId="me", id=message_id
    ).execute()

    # Figure out which month this invoice belongs to
    month_folder = get_email_date(message, month_offset)
    save_path = os.path.join(folder, month_folder)

    # Create the month folder if it doesn't exist (e.g., invoices/2025-01/)
    os.makedirs(save_path, exist_ok=True)

    downloaded = 0

    # Look through all parts of the email for attachments
    parts = message["payload"].get("parts", [])
    for part in parts:
        filename = part.get("filename", "")

        # Only download PDF files
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(save_path, filename)

            # Skip if we already have this file
            if os.path.exists(file_path):
                print(f"  Already exists, skipping: {file_path}")
                continue

            attachment_id = part["body"].get("attachmentId")

            if attachment_id:
                # Download the attachment data from Gmail
                attachment = service.users().messages().attachments().get(
                    userId="me",
                    messageId=message_id,
                    id=attachment_id
                ).execute()

                # Decode the attachment (Gmail sends it as encoded text)
                file_data = base64.urlsafe_b64decode(attachment["data"])

                # Save the PDF file
                with open(file_path, "wb") as f:
                    f.write(file_data)

                print(f"  Saved: {file_path}")
                downloaded += 1

    return downloaded


def main():
    """
    Main function that ties everything together:
    1. Connect to Gmail
    2. Search for invoice emails
    3. Download PDF attachments
    4. Save them to monthly folders
    """
    print("Connecting to Gmail...")
    service = get_gmail_service()

    total_downloaded = 0

    for sender_name, query, month_offset in SEARCH_QUERIES:
        print(f"\n--- Searching for {sender_name} invoices ---")
        print(f"Query: {query}")
        if month_offset != 0:
            print(f"(Filing invoices {abs(month_offset)} month(s) back from email date)")

        results = service.users().messages().list(
            userId="me", q=query
        ).execute()

        messages = results.get("messages", [])

        if not messages:
            print(f"No invoices found from {sender_name}.")
            continue

        print(f"Found {len(messages)} email(s) from {sender_name}.\n")

        for i, msg in enumerate(messages, 1):
            print(f"Processing email {i}/{len(messages)}...")
            count = download_attachments(service, msg["id"], INVOICES_DIR, month_offset)
            total_downloaded += count

    print(f"\n=== Done! Downloaded {total_downloaded} invoice(s) total. ===")
    print(f"Check the '{INVOICES_DIR}/' folder for your invoices.")


# This runs the main function when you execute the script
if __name__ == "__main__":
    main()
