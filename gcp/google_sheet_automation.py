import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import sqlite3
import pytz
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from random import randint

# Load environment variables
load_dotenv()

# Path to the service account key file
SERVICE_ACCOUNT_FILE = 'xxxxx.json'

# Define the scope for Google Sheets and Google Drive
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Authenticate using the service account
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Sheets API service
service_sheets = build('sheets', 'v4', credentials=creds)

# Define New York timezone and UTC
ny_tz = pytz.timezone('America/New_York')
utc_tz = pytz.utc

# Get the current time in New York timezone and calculate yesterday's date
now_ny = datetime.now(ny_tz)
yesterday = now_ny - timedelta(days=1)
yesterday_date_str = yesterday.strftime('%Y-%m-%d')

# Define the start and end of yesterday in New York time (00:00:00 to 23:59:59)
yesterday_start_str = yesterday_date_str + " 00:00:00"
yesterday_end_str = yesterday_date_str + " 23:59:59"

# Mapping store_id to store names
store_id_map = {

    7: "Demo Store 1",
    8: "Demo Store 2",
    9: "Demo Store 3",

}

# Permanent color mapping for store names
store_colors = {
    "Amish-Store": {"red": 0.93, "green": 0.84, "blue": 0.77},
    "Okka-Foods": {"red": 0.8, "green": 0.93, "blue": 0.77},
    "Green Valley Store": {"red": 0.77, "green": 0.87, "blue": 0.93},
    "Demo Store 1": {"red": 0.93, "green": 0.77, "blue": 0.87},
    "Demo Store 2": {"red": 0.77, "green": 0.93, "blue": 0.8},
    "Demo Store 3": {"red": 0.87, "green": 0.77, "blue": 0.93},
    "Foodcellar Court Square": {"red": 0.93, "green": 0.93, "blue": 0.77},
    "Foodcellar Market": {"red": 0.77, "green": 0.93, "blue": 0.93},
    "Sheepshead Store": {"red": 0.93, "green": 0.87, "blue": 0.77},
    "Ideal Food Basket Store": {"red": 0.87, "green": 0.93, "blue": 0.77},
    "Key Food - Rosedale": {"red": 0.77, "green": 0.93, "blue": 0.87},
    "Key Food - Ave N": {"red": 0.93, "green": 0.77, "blue": 0.93},
    "King Fruit": {"red": 0.77, "green": 0.87, "blue": 0.93},
    "Tashkent Store": {"red": 0.93, "green": 0.77, "blue": 0.87},
    "Hatzlatchakosher": {"red": 0.87, "green": 0.77, "blue": 0.93},
    "Fine Fare Market": {"red": 0.77, "green": 0.93, "blue": 0.93},
    "Cove Country Store": {"red": 0.93, "green": 0.87, "blue": 0.93}
}

# Permanent color mapping for poll answers
poll_answer_colors = {
    "eating": {"red": 1.0, "green": 1.0, "blue": 0.6},  # Yellow
    "shoplifting": {"red": 1.0, "green": 0.6, "blue": 0.6}  # Red
}

# Connect to the SQLite database
conn = sqlite3.connect("backend.db")
cursor = conn.cursor()

# Filter data from the previous day where poll_answer is 'shoplifting' or 'eating'
cursor.execute('''SELECT store_id, video_path, created_at, poll_answer_time, poll_answer, labeler, poll_id
                  FROM shoplifting_backend
                  WHERE created_at >= ? AND created_at <= ? AND (poll_answer = 'shoplifting' OR poll_answer = 'eating')''', 
                  (yesterday_start_str, yesterday_end_str))
rows = cursor.fetchall()

# Process rows to replace store_id with store_name and convert UTC times to New York time
processed_rows = []
labeler_colors = {}

for row in rows:
    store_id, video_path, created_at, poll_answer_time, poll_answer, labelers, poll_id = row
    store_name = store_id_map.get(store_id, "Unknown Store")
    video_path = os.path.basename(video_path)
    if not labelers:
        labelers = "No_username"

    # Assign random colors to each labeler if not already assigned
    if labelers not in labeler_colors:
        labeler_colors[labelers] = {
            'red': randint(0, 255) / 255.0,
            'green': randint(0, 255) / 255.0,
            'blue': randint(0, 255) / 255.0
        }

    # Convert times from UTC to New York time
    created_at_utc = datetime.fromisoformat(created_at) if isinstance(created_at, str) else created_at
    created_at_ny = created_at_utc.replace(tzinfo=utc_tz).astimezone(ny_tz)

    poll_answer_time_utc = datetime.fromisoformat(poll_answer_time) if isinstance(poll_answer_time, str) else poll_answer_time
    poll_answer_time_ny = poll_answer_time_utc.replace(tzinfo=utc_tz).astimezone(ny_tz)

    latency = poll_answer_time_ny - created_at_ny

    processed_rows.append([
        labelers,
        store_name,
        latency,
        poll_answer,
        created_at_ny.strftime('%Y-%m-%d %H:%M:%S'),
        poll_answer_time_ny.strftime('%Y-%m-%d %H:%M:%S'),
        poll_id,
        video_path
    ])

# Sort the processed rows by store_name alphabetically
processed_rows.sort(key=lambda x: x[1])

# Define the spreadsheet ID (update this with your existing spreadsheet ID)
spreadsheet_id = 'API-KEY'

# Define the title for the new sheet (tab) based on the date
sheet_title = yesterday_date_str

# Create a new sheet (tab) in the existing spreadsheet
try:
    add_sheet_request = {
        "requests": [
            {
                "addSheet": {
                    "properties": {
                        "title": sheet_title
                    }
                }
            }
        ]
    }
    response = service_sheets.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=add_sheet_request
    ).execute()
    print(f"Sheet '{sheet_title}' created in spreadsheet ID: {spreadsheet_id}")
except HttpError as error:
    print(f"An error occurred while creating the sheet: {error}")
    conn.close()
    exit(1)

# Get the sheet ID for the newly created sheet
sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']

# Create the request body for the data to be appended
values = [['Labelers', 'Store Name', 'Latency', 'Poll Answer', 'Created At', 'Poll Answer Time', 'Poll ID', 'Video Path']] + [
    [
        row[0],  # Labelers
        row[1],  # Store Name
        str(row[2]),  # Latency (converted to string for Google Sheets)
        row[3],  # Poll Answer
        row[4],  # Created At
        row[5],  # Poll Answer Time
        row[6],  # Poll ID
        row[7]   # Video Path
    ] for row in processed_rows
]
body = {
    'values': values
}

# Append the data to the newly created sheet
try:
    result = service_sheets.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_title}!A1",
        valueInputOption="RAW",
        body=body
    ).execute()
    print(f'{result.get("updates").get("updatedCells")} cells appended to sheet "{sheet_title}".')
except HttpError as error:
    print(f"An error occurred while appending data: {error}")

# Apply conditional formatting based on the labeler, store name, poll answer, and latency
requests = []

# Formatting for Labelers (Column A)
for i, row in enumerate(processed_rows, start=2):  # Start from row 2 (considering row 1 is the header)
    labeler = row[0]
    color = labeler_colors[labeler]
    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': i - 1,
                'endRowIndex': i,
                'startColumnIndex': 0,
                'endColumnIndex': 1  # Column A (Labelers)
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': color
                }
            },
            'fields': 'userEnteredFormat.backgroundColor'
        }
    })

# Formatting for Store Name (Column B)
for i, row in enumerate(processed_rows, start=2):  # Start from row 2 (considering row 1 is the header)
    store_name = row[1]
    
    if store_name in store_colors:
        color = store_colors[store_name]
    else:
        color = {"red": 0.9, "green": 0.9, "blue": 0.9}  # Default light gray if store name not found

    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': i - 1,
                'endRowIndex': i,
                'startColumnIndex': 1,
                'endColumnIndex': 2  # Column B (Store Name)
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': color
                }
            },
            'fields': 'userEnteredFormat.backgroundColor'
        }
    })

# Formatting for Poll Answer (Column D)
for i, row in enumerate(processed_rows, start=2):  # Start from row 2 (considering row 1 is the header)
    poll_answer = row[3]
    color = poll_answer_colors.get(poll_answer, {"red": 0.9, "green": 0.9, "blue": 0.9})  # Default light gray if not found
    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': i - 1,
                'endRowIndex': i,
                'startColumnIndex': 3,
                'endColumnIndex': 4  # Column D (Poll Answer)
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': color
                }
            },
            'fields': 'userEnteredFormat.backgroundColor'
        }
    })

# Conditional formatting for Latency (Column C)
for i, row in enumerate(processed_rows, start=2):  # Start from row 2 (considering row 1 is the header)
    latency = row[2].total_seconds()
    
    # Green for latency < 2 minutes
    if latency < 120:
        color = {"red": 0.6, "green": 0.9, "blue": 0.6}
    # Orange for latency between 2 and 5 minutes
    elif 120 <= latency <= 300:
        color = {"red": 1.0, "green": 0.8, "blue": 0.6}
    # Red for latency > 5 minutes
    else:
        color = {"red": 1.0, "green": 0.6, "blue": 0.6}

    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': i - 1,
                'endRowIndex': i,
                'startColumnIndex': 2,
                'endColumnIndex': 3  # Column C (Latency)
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': color
                }
            },
            'fields': 'userEnteredFormat.backgroundColor'
        }
    })

# Send the batchUpdate request to apply formatting
try:
    service_sheets.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()
    print("Conditional formatting applied based on labelers, store names, poll answers, and latency.")
except HttpError as error:
    print(f"An error occurred while applying conditional formatting: {error}")

# Close the database connection
conn.close()
