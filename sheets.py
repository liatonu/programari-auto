import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---------------------------
# CONECTARE GOOGLE SHEETS
# -------------------python3 -m pip install flask--------

SHEET_NAME = "ProgramariAuto"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

spreadsheet = client.open(SHEET_NAME)

rezervari_sheet = spreadsheet.worksheet("Rezervari")
conturi_sheet = spreadsheet.worksheet("Conturi")

# ---------------------------
# ORE DISPONIBILE
# ---------------------------

ALL_HOURS = [
    "07:00",
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00"
]

# ---------------------------
# LOGIN INSTRUCTOR
# ---------------------------

def check_login(username, password):

    rows = conturi_sheet.get_all_values()

    for row in rows[1:]:
        if len(row) >= 2:
            if row[0] == username and row[1] == password:
                return True

    return False

# ---------------------------
# ORE LIBERE
# ---------------------------

def get_available_hours(date):

    bookings = rezervari_sheet.get_all_values()

    occupied = []

    for row in bookings[1:]:

        if len(row) >= 5:

            booking_date = row[3]
            booking_hour = row[4]

            if booking_date == date:
                occupied.append(booking_hour)

    available = []

    for hour in ALL_HOURS:

        if hour not in occupied:
            available.append(hour)

    return available

# ---------------------------
# ADAUGĂ REZERVARE
# ---------------------------

def add_booking(
    nume,
    prenume,
    telefon,
    data,
    ora
):

    rezervari_sheet.append_row([
        nume,
        prenume,
        telefon,
        data,
        ora
    ])

# ---------------------------
# TOATE REZERVĂRILE
# ---------------------------

def get_all_bookings():

    rows = rezervari_sheet.get_all_values()

    result = []

    index = 2

    for row in rows[1:]:

        if len(row) >= 5:

            result.append({
                "row": index,
                "nume": row[0],
                "prenume": row[1],
                "telefon": row[2],
                "data": row[3],
                "ora": row[4]
            })

        index += 1

    return result

# ---------------------------
# ȘTERGE REZERVARE
# ---------------------------

def delete_booking(row_number):

    rezervari_sheet.delete_rows(row_number)