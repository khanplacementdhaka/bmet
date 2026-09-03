from flask import Flask, render_template_string
import pandas as pd
import requests
import os

app = Flask(__name__)

# --- GitHub Repository Configuration ---
GITHUB_USERNAME = "khanplacementdhaka"
GITHUB_REPO = "bmet"
BRANCH = "main"

# GitHub API URL এবং Raw Base URL
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/{BRANCH}/"

def format_val(val):
    """খালি বা NaN ডাটা হ্যান্ডেল এবং তারিখ ফরম্যাট করার হেলপার ফাংশন"""
    if pd.isna(val) or str(val).strip().lower() in ['nan', 'none', 'nat', '']:
        return '-'
    if isinstance(val, pd.Timestamp):
        return val.strftime('%Y-%m-%d')
    return str(val).strip()

def get_image_url_by_passport(passport_number):
    """পাসপোর্ট নম্বর দিয়ে গিটহাব থেকে ছবি মেলাবার ফাংশন"""
    if not passport_number or passport_number == '-':
        return 'https://www.w3schools.com/howto/img_avatar.png'
    
    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        if response.status_code == 200:
            files = response.json()
            for file in files:
                filename = file.get('name', '')
                # পাসপোর্টের ছবি ম্যাচ করা (bmet.png বাদ দিয়ে)
                if passport_number.lower() in filename.lower() and filename.lower() != 'bmet.png':
                    return f"{RAW_BASE_URL}{filename}"
    except Exception as e:
        print(f"Error checking GitHub files: {e}")

    return 'https://www.w3schools.com/howto/img_avatar.png'


@app.route('/verify/<full_id>')
def verify(full_id):

    if not os.path.exists("data.xlsx"):
        return "Database file not found.", 500

    # Read Excel file
    df = pd.read_excel("data.xlsx")

    # Extract ID from URL
    clean_id = full_id.replace("RS-I-2026-", "").strip()

    if 'CLEARANCE_ID' not in df.columns:
        return "CLEARANCE_ID column not found in Excel file.", 500

    # Match Excel data
    user_data = df[
        df['CLEARANCE_ID'].astype(str).str.strip() == clean_id
    ]

    if user_data.empty:
        return "Invalid Card or Record Not Found", 404

    row = user_data.iloc[0]

    # Map dataset values
    data = {
        'SL_NO': format_val(row.get('SL NO')),
        'NAME': format_val(row.get('NAME')),
        'PASSPORT': format_val(row.get('PASSPORT')),
        'ISSUE_DATE': format_val(row.get('ISSUE_DATE')),
        'FATHERS_NAME': format_val(row.get('FATHERS_NAME')),
        'MOTHERS_NAME': format_val(row.get('MOTHERS_NAME')),
        'BMET_ID': format_val(row.get('BMET_ID')),
        'CLEARANCE_ID': format_val(row.get('CLEARANCE_ID')),
        'DATE': format_val(row.get('DATE')),
        'TIME': format_val(row.get('TIME')),
        'BIRTH_DATE': format_val(row.get('Birth Date')),
        'BLOOD_GROUP': format_val(row.get('Blood Group')),
        'PASSPORT_ISSUE': format_val(row.get('Passport Issue Date')),
        'PASSPORT_EXPIRE': format_val(row.get('Passport Expire Date')),
        'VISA_NO': format_val(row.get('Visa No')),
        'VISA_ISSUE': format_val(row.get('Visa Issue Date')),
        'VISA_EXPIRE': format_val(row.get('Visa Expiry Date')),
        'REFERRAL_NO': format_val(row.get('Referral No')),
        'EMPLOYER': format_val(row.get('Employer')),
        'COUNTRY': format_val(row.get('Country')),
        
        # Recruiting Agency
        'AGENCY_NAME': format_val(row.get('Name')),
        'LICENSE_NO': format_val(row.get('License No')),
        'AGENCY_PHONE': format_val(row.get('Phone')),
        
        # BMET Registration
        'BMET_NO': format_val(row.get('BMET No')),
        'BMET_REG_NAME': format_val(row.get('Name.1')),
        'BMET_BIRTH_DATE': format_val(row.get('Birth Date.1')),
        'GENDER': format_val(row.get('Gender')),
        'NID': format_val(row.get('NID')),
        
        # Passports
        'PP_NAME': format_val(row.get('Name.2')),
        'PASSPORT_NO_1': format_val(row.get('Passport No 1')),
        
        # Permanent Address
        'HOUSE_VILL': format_val(row.get('House/Vill/Road')),
        'POST_OFFICE': format_val(row.get('Post Office')),
        'POLICE_STATION': format_val(row.get('Police Station')),
        'UPAZILA': format_val(row.get('Upazila')),
        'DISTRICT': format_val(row.get('District')),
        'DIVISION': format_val(row.get('Division')),
        
        # Emergency Contact
        'EMERGENCY_NAME': format_val(row.get('Name.3')),
        'RELATION': format_val(row.get('Relation')),
        'MOBILE': format_val(row.get('Mobile')),
        'ADDRESS': format_val(row.get('Address')),
    }

    # Logos (GitHub direct link for BMET logo)
    BMET_LOGO = f"{RAW_BASE_URL}bmet.png"
    BD_LOGO = "https://upload.wikimedia.org/wikipedia/commons/8/84/Government_Seal_of_Bangladesh.svg"
    
    # User Photo from GitHub
    USER_PHOTO = get_image_url_by_passport(data['PASSPORT'])

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        
        <title>OEP RAIMS</title>
        <link rel="icon" type="image/png" href="{{ bmet_logo }}">

        <style>
            * { box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
                background-color: #f7fafc;
                margin: 0;
                padding: 12px 6px;
                color: #2d3748;
            }
            .card {
                max-width: 440px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 8px;
                padding: 16px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            }
            
            /* Top Header: Left = BMET Logo, Right = BD Logo */
            .top-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                text-align: center;
                padding-bottom: 10px;
                border-bottom: 1px dashed #e2e8f0;
            }
            .top-header img { width: 42px; height: 42px; object-fit: contain; }
            .header-text { flex-grow: 1; padding: 0 6px; }
            .gov-title { color: #22543d; font-weight: bold; font-size: 13px; line-height: 1.3; }
            .sub-title { color: #c53030; font-weight: 600; font-size: 11px; margin-top: 2px; }

            .clearance-heading {
                text-align: center;
                margin: 14px 0 10px;
            }
            .clearance-heading .bn { font-size: 13px; color: #4a5568; margin-bottom: 2px; }
            .clearance-heading .en { font-size: 17px; font-weight: bold; color: #1a202c; }

            /* Profile Photo */
            .profile-box { text-align: center; margin: 12px 0 16px; }
            .profile-img {
                width: 110px;
                height: 110px;
                object-fit: cover;
                border-radius: 50%;
                border: 2px solid #22543d;
                box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            }
            .user-name {
                font-size: 15px;
                font-weight: 700;
                color: #2d3748;
                margin-top: 8px;
            }
            .ec-detail { font-size: 12px; color: #718096; margin-top: 3px; }

            /* Table Formatting & Borders */
            .info-table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 12px;
                background: #fcfcfc;
                border: 1px solid #edf2f7;
                border-radius: 6px;
                overflow: hidden;
            }
            .info-table tr { border-bottom: 1px solid #edf2f7; }
            .info-table tr:last-child { border-bottom: none; }
            .info-table td {
                padding: 6px 10px;
                font-size: 11.5px;
                vertical-align: middle;
            }
            .info-table td.label { color: #718096; width: 44%; }
            .info-table td.value { color: #1a202c; font-weight: 600; width: 56%; word-break: break-word; }

            .section-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin: 14px 0 6px;
            }
            .section-title {
                font-size: 13px;
                font-weight: bold;
                color: #276749;
            }
            .mini-logos img {
                width: 18px;
                height: 18px;
                margin-left: 2px;
                vertical-align: middle;
            }
        </style>
    </head>
    <body>

        <div class="card">
            <!-- Header Section: Left = BMET Logo, Right = BD Seal -->
            <div class="top-header">
                <img src="{{ bmet_logo }}" alt="BMET Logo">
                <div class="header-text">
                    <div class="gov-title">গণপ্রজাতন্ত্রী বাংলাদেশ সরকার</div>
                    <div class="sub-title">জনশক্তি কর্মসংস্থান ও প্রশিক্ষন ব্যুরো</div>
                </div>
                <img src="{{ bd_logo }}" alt="BD Seal">
            </div>

            <!-- Main Heading -->
            <div class="clearance-heading">
                <div class="bn">বহির্গমন ছাড়পত্র</div>
                <div class="en">Emigration Clearance</div>
            </div>

            <!-- Profile Info -->
            <div class="profile-box">
                <img class="profile-img" 
                     src="{{ user_photo }}" 
                     onerror="this.onerror=null; this.src='https://www.w3schools.com/howto/img_avatar.png';" 
                     alt="User Photo">
                <div class="user-name">{{ data.NAME }}</div>
                <div class="ec-detail"><b>EC No:</b> RS-I-2026-{{ data.CLEARANCE_ID }}</div>
                <div class="ec-detail"><b>EC Date:</b> {{ data.DATE }}</div>
            </div>

            <!-- Main Info Table -->
            <table class="info-table">
                <tr><td class="label">Birth Date</td><td class="value">{{ data.BIRTH_DATE }}</td></tr>
                <tr><td class="label">Blood Group</td><td class="value">{{ data.BLOOD_GROUP }}</td></tr>
                <tr><td class="label">Passport No</td><td class="value">{{ data.PASSPORT }}</td></tr>
                <tr><td class="label">Passport Issue Date</td><td class="value">{{ data.PASSPORT_ISSUE }}</td></tr>
                <tr><td class="label">Passport Expire Date</td><td class="value">{{ data.PASSPORT_EXPIRE }}</td></tr>
                <tr><td class="label">Visa No</td><td class="value">{{ data.VISA_NO }}</td></tr>
                <tr><td class="label">Visa Issue Date</td><td class="value">{{ data.VISA_ISSUE }}</td></tr>
                <tr><td class="label">Visa Expire Date</td><td class="value">{{ data.VISA_EXPIRE }}</td></tr>
                <tr><td class="label">Referral No</td><td class="value">{{ data.REFERRAL_NO }}</td></tr>
                <tr><td class="label">Employer</td><td class="value">{{ data.EMPLOYER }}</td></tr>
                <tr><td class="label">Country</td><td class="value">{{ data.COUNTRY }}</td></tr>
            </table>

            <!-- Section 1: Recruiting Agency (Bottom order: Left = BD Logo, Right = BMET Logo) -->
            <div class="section-header">
                <span class="section-title">Recruiting Agency</span>
                <div class="mini-logos">
                    <img src="{{ bd_logo }}" alt="BD Seal">
                    <img src="{{ bmet_logo }}" alt="BMET Logo">
                </div>
            </div>
            <table class="info-table">
                <tr><td class="label">Name</td><td class="value">{{ data.AGENCY_NAME }}</td></tr>
                <tr><td class="label">License No</td><td class="value">{{ data.LICENSE_NO }}</td></tr>
                <tr><td class="label">Phone</td><td class="value">{{ data.AGENCY_PHONE }}</td></tr>
            </table>

            <!-- Section 2: BMET Registration -->
            <div class="section-header">
                <span class="section-title">BMET Registration</span>
                <div class="mini-logos">
                    <img src="{{ bd_logo }}" alt="BD Seal">
                    <img src="{{ bmet_logo }}" alt="BMET Logo">
                </div>
            </div>
            <table class="info-table">
                <tr><td class="label">BMET No</td><td class="value">{{ data.BMET_NO }}</td></tr>
                <tr><td class="label">Name</td><td class="value">{{ data.BMET_REG_NAME }}</td></tr>
                <tr><td class="label">Birth Date</td><td class="value">{{ data.BMET_BIRTH_DATE }}</td></tr>
                <tr><td class="label">Gender</td><td class="value">{{ data.GENDER }}</td></tr>
                <tr><td class="label">NID</td><td class="value">{{ data.NID }}</td></tr>
            </table>

            <!-- Section 3: Passports -->
            <div class="section-header">
                <span class="section-title">Passports</span>
                <div class="mini-logos">
                    <img src="{{ bd_logo }}" alt="BD Seal">
                    <img src="{{ bmet_logo }}" alt="BMET Logo">
                </div>
            </div>
            <table class="info-table">
                <tr><td class="label">Name</td><td class="value">{{ data.PP_NAME }}</td></tr>
                <tr><td class="label">Passport No 1</td><td class="value">{{ data.PASSPORT_NO_1 }}</td></tr>
            </table>

            <!-- Section 4: Permanent Address -->
            <div class="section-header">
                <span class="section-title">Permanent Address</span>
                <div class="mini-logos">
                    <img src="{{ bd_logo }}" alt="BD Seal">
                    <img src="{{ bmet_logo }}" alt="BMET Logo">
                </div>
            </div>
            <table class="info-table">
                <tr><td class="label">House/Vill/Road</td><td class="value">{{ data.HOUSE_VILL }}</td></tr>
                <tr><td class="label">Post Office</td><td class="value">{{ data.POST_OFFICE }}</td></tr>
                <tr><td class="label">Police Station</td><td class="value">{{ data.POLICE_STATION }}</td></tr>
                <tr><td class="label">Upazila</td><td class="value">{{ data.UPAZILA }}</td></tr>
                <tr><td class="label">District</td><td class="value">{{ data.DISTRICT }}</td></tr>
                <tr><td class="label">Division</td><td class="value">{{ data.DIVISION }}</td></tr>
            </table>

            <!-- Section 5: Emergency Contact -->
            <div class="section-header">
                <span class="section-title">Emergency Contact</span>
                <div class="mini-logos">
                    <img src="{{ bd_logo }}" alt="BD Seal">
                    <img src="{{ bmet_logo }}" alt="BMET Logo">
                </div>
            </div>
            <table class="info-table">
                <tr><td class="label">Name</td><td class="value">{{ data.EMERGENCY_NAME }}</td></tr>
                <tr><td class="label">Relation</td><td class="value">{{ data.RELATION }}</td></tr>
                <tr><td class="label">Mobile</td><td class="value">{{ data.MOBILE }}</td></tr>
                <tr><td class="label">Address</td><td class="value">{{ data.ADDRESS }}</td></tr>
            </table>

        </div>

    </body>
    </html>
    """, data=data, bd_logo=BD_LOGO, bmet_logo=BMET_LOGO, user_photo=USER_PHOTO)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)