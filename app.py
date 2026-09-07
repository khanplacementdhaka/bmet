from flask import Flask, render_template_string
import pandas as pd
import requests
import os

app = Flask(__name__)

# ==============================
# GitHub Configuration
# ==============================
GITHUB_USERNAME = "khanplacementdhaka"
GITHUB_REPO = "bmet"
BRANCH = "main"

GITHUB_API_URL = (
    f"https://api.github.com/repos/"
    f"{GITHUB_USERNAME}/{GITHUB_REPO}/contents"
)

RAW_BASE_URL = (
    f"https://raw.githubusercontent.com/"
    f"{GITHUB_USERNAME}/{GITHUB_REPO}/{BRANCH}/"
)


# ==============================
# Format Excel Values
# ==============================
def format_val(val):
    if pd.isna(val) or str(val).strip().lower() in [
        'nan', 'none', 'nat', ''
    ]:
        return '-'

    # Date
    if isinstance(val, pd.Timestamp):
        return val.strftime('%Y-%m-%d')

    # Remove .0 from whole numbers
    # Example: 4215410293.0 -> 4215410293
    if isinstance(val, float) and val.is_integer():
        return str(int(val))

    return str(val).strip()


# ==============================
# Find Photo by Passport Number
# ==============================
def get_image_url_by_passport(passport_no):
    try:
        response = requests.get(
            GITHUB_API_URL,
            timeout=10
        )

        if response.status_code != 200:
            return None

        files = response.json()

        passport_no = str(passport_no).strip().upper()

        for file in files:
            if file.get("type") != "file":
                continue

            filename = file.get("name", "").upper()

            if passport_no in filename:
                return RAW_BASE_URL + file["path"]

    except Exception as e:
        print("GitHub image error:", e)

    return None


# ==============================
# Verification Route
# ==============================
@app.route('/verify/<full_id>')
def verify(full_id):

    # Check Excel file
    if not os.path.exists("data.xlsx"):
        return "Database file not found.", 500

    # Read Excel
    df = pd.read_excel("data.xlsx")

    # Extract ID
    clean_id = str(full_id).strip()

    # ==============================
    # Find CLEARANCE_ID
    # ==============================
    if 'CLEARANCE_ID' not in df.columns:
        return "CLEARANCE_ID column not found in database.", 500

    user_data = df[
        df['CLEARANCE_ID']
        .astype(str)
        .str.replace(r'\.0$', '', regex=True)
        .str.strip()
        == clean_id
    ]

    if user_data.empty:
        return """
        <html>
        <head>
            <title>Verification Failed</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                }

                .box {
                    max-width: 500px;
                    margin: auto;
                    padding: 30px;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                }

                h2 {
                    color: red;
                }
            </style>
        </head>

        <body>
            <div class="box">
                <h2>Verification Failed</h2>
                <p>No record found for this verification ID.</p>
            </div>
        </body>
        </html>
        """, 404

    # First matching row
    row = user_data.iloc[0]

    # ==============================
    # Get Data
    # ==============================
    ec_no = format_val(row.get('CLEARANCE_ID'))
    ec_date = format_val(row.get('CLEARANCE_DATE'))

    name = format_val(row.get('NAME'))
    birth_date = format_val(row.get('DATE_OF_BIRTH'))
    blood_group = format_val(row.get('BLOOD_GROUP'))

    passport_no = format_val(row.get('PASSPORT_NO'))
    passport_issue = format_val(row.get('PASSPORT_ISSUE_DATE'))
    passport_expire = format_val(row.get('PASSPORT_EXPIRY_DATE'))

    visa_no = format_val(row.get('VISA_NO'))
    visa_issue = format_val(row.get('VISA_ISSUE_DATE'))
    visa_expire = format_val(row.get('VISA_EXPIRY_DATE'))

    referral_no = format_val(row.get('REFERRAL_NO'))

    employer = format_val(row.get('EMPLOYER'))
    country = format_val(row.get('COUNTRY'))

    recruiting_agency = format_val(
        row.get('RECRUITING_AGENCY')
    )

    bmet_registration = format_val(
        row.get('BMET_REGISTRATION')
    )

    permanent_address = format_val(
        row.get('PERMANENT_ADDRESS')
    )

    emergency_contact = format_val(
        row.get('EMERGENCY_CONTACT')
    )

    # ==============================
    # Passport Photo
    # ==============================
    photo_url = get_image_url_by_passport(passport_no)

    if not photo_url:
        photo_url = (
            "https://via.placeholder.com/180x220"
            "?text=No+Photo"
        )

    # ==============================
    # HTML
    # ==============================
    html = """
    <!DOCTYPE html>
    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>OEP RAIMS</title>

        <link
            href="https://fonts.googleapis.com/css2?family=Tiro+Bangla&display=swap"
            rel="stylesheet"
        >

        <style>

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 0;
                background: #f3f3f3;
                font-family: 'Tiro Bangla', Arial, sans-serif;
                color: #222;
            }

            .container {
                max-width: 1000px;
                margin: 25px auto;
                background: white;
                padding: 25px;
                box-shadow: 0 0 10px rgba(0,0,0,0.15);
            }

            .header {
                text-align: center;
                border-bottom: 3px solid #008000;
                padding-bottom: 15px;
                margin-bottom: 20px;
            }

            .header h1 {
                margin: 0;
                font-size: 28px;
                color: #008000;
                font-weight: bold;
            }

            .header h2 {
                margin: 5px 0;
                color: #c000c0;
                font-size: 20px;
            }

            .profile-section {
                display: flex;
                gap: 25px;
                margin-bottom: 20px;
                align-items: flex-start;
            }

            .photo {
                width: 160px;
                height: 190px;
                object-fit: cover;
                border: 1px solid #999;
                padding: 3px;
                background: white;
            }

            .profile-info {
                flex: 1;
            }

            .profile-info table {
                width: 100%;
                border-collapse: collapse;
            }

            .profile-info td {
                padding: 8px;
                border-bottom: 1px solid #ddd;
            }

            .profile-info td:first-child {
                width: 180px;
                font-weight: bold;
            }

            .section-title {
                background: #008000;
                color: white;
                padding: 10px;
                margin-top: 20px;
                font-size: 18px;
                font-weight: bold;
            }

            table.data-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 0;
            }

            table.data-table th,
            table.data-table td {
                border: 1px solid #ccc;
                padding: 9px;
                text-align: left;
            }

            table.data-table th {
                background: #f0f0f0;
                width: 25%;
            }

            .government {
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 2px solid #008000;
            }

            .government img {
                max-width: 100px;
                max-height: 100px;
            }

            .verified {
                text-align: center;
                margin-top: 20px;
                color: green;
                font-size: 20px;
                font-weight: bold;
            }

            @media (max-width: 700px) {

                .container {
                    margin: 0;
                    padding: 15px;
                }

                .profile-section {
                    flex-direction: column;
                    align-items: center;
                }

                .profile-info {
                    width: 100%;
                }

                .profile-info td:first-child {
                    width: 130px;
                }

                table.data-table th,
                table.data-table td {
                    padding: 6px;
                    font-size: 14px;
                }
            }

        </style>

    </head>

    <body>

        <div class="container">

            <div class="header">

                <h1>
                    Overseas Employment Platform
                </h1>

                <h2>
                    Recruitment Agency Information Management System
                </h2>

            </div>


            <div class="profile-section">

                <img
                    src="{{ photo_url }}"
                    class="photo"
                    alt="Profile Photo"
                >

                <div class="profile-info">

                    <table>

                        <tr>
                            <td>EC No</td>
                            <td>{{ ec_no }}</td>
                        </tr>

                        <tr>
                            <td>EC Date</td>
                            <td>{{ ec_date }}</td>
                        </tr>

                        <tr>
                            <td>Name</td>
                            <td>{{ name }}</td>
                        </tr>

                    </table>

                </div>

            </div>


            <div class="section-title">
                Personal Information
            </div>

            <table class="data-table">

                <tr>
                    <th>Birth Date</th>
                    <td>{{ birth_date }}</td>

                    <th>Blood Group</th>
                    <td>{{ blood_group }}</td>
                </tr>

                <tr>
                    <th>Passport No</th>
                    <td>{{ passport_no }}</td>

                    <th>Passport Issue Date</th>
                    <td>{{ passport_issue }}</td>
                </tr>

                <tr>
                    <th>Passport Expire Date</th>
                    <td>{{ passport_expire }}</td>

                    <th>Visa No</th>
                    <td>{{ visa_no }}</td>
                </tr>

                <tr>
                    <th>Visa Issue Date</th>
                    <td>{{ visa_issue }}</td>

                    <th>Visa Expire Date</th>
                    <td>{{ visa_expire }}</td>
                </tr>

                <tr>
                    <th>Referral No</th>
                    <td>{{ referral_no }}</td>

                    <th>Country</th>
                    <td>{{ country }}</td>
                </tr>

                <tr>
                    <th>Employer</th>
                    <td colspan="3">{{ employer }}</td>
                </tr>

            </table>


            <div class="section-title">
                Recruiting Agency
            </div>

            <table class="data-table">

                <tr>
                    <th>Recruiting Agency</th>
                    <td>{{ recruiting_agency }}</td>
                </tr>

                <tr>
                    <th>BMET Registration</th>
                    <td>{{ bmet_registration }}</td>
                </tr>

            </table>


            <div class="section-title">
                Passport Information
            </div>

            <table class="data-table">

                <tr>
                    <th>Passport No</th>
                    <td>{{ passport_no }}</td>
                </tr>

                <tr>
                    <th>Issue Date</th>
                    <td>{{ passport_issue }}</td>
                </tr>

                <tr>
                    <th>Expiry Date</th>
                    <td>{{ passport_expire }}</td>
                </tr>

            </table>


            <div class="section-title">
                Permanent Address
            </div>

            <table class="data-table">

                <tr>
                    <th>Address</th>
                    <td>{{ permanent_address }}</td>
                </tr>

            </table>


            <div class="section-title">
                Emergency Contact
            </div>

            <table class="data-table">

                <tr>
                    <th>Emergency Contact</th>
                    <td>{{ emergency_contact }}</td>
                </tr>

            </table>


            <div class="verified">
                ✓ Information Successfully Verified
            </div>


            <div class="government">

                <img
                    src="https://raw.githubusercontent.com/khanplacementdhaka/bmet/main/bmet_logo.png"
                    alt="BMET Logo"
                >

                <p>
                    Bureau of Manpower, Employment and Training (BMET)
                </p>

                <img
                    src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Seal_of_Bangladesh.svg/200px-Seal_of_Bangladesh.svg.png"
                    alt="Bangladesh Government Seal"
                >

            </div>

        </div>

    </body>

    </html>
    """

    return render_template_string(
        html,
        photo_url=photo_url,
        ec_no=ec_no,
        ec_date=ec_date,
        name=name,
        birth_date=birth_date,
        blood_group=blood_group,
        passport_no=passport_no,
        passport_issue=passport_issue,
        passport_expire=passport_expire,
        visa_no=visa_no,
        visa_issue=visa_issue,
        visa_expire=visa_expire,
        referral_no=referral_no,
        employer=employer,
        country=country,
        recruiting_agency=recruiting_agency,
        bmet_registration=bmet_registration,
        permanent_address=permanent_address,
        emergency_contact=emergency_contact
    )


# ==============================
# Run Application
# ==============================
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000
    )