from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# Route to handle verification link
@app.route('/verify/<full_id>')
def verify(full_id):

    if not os.path.exists("data.xlsx"):
        return "Database file not found.", 500

    # Read Excel file
    df = pd.read_excel("data.xlsx")

    # Extract ID from URL
    clean_id = full_id.replace("RS-I-2026-", "")

    # Check CLEARANCE_ID column exists
    if 'CLEARANCE_ID' not in df.columns:
        return "CLEARANCE_ID column not found in Excel file.", 500

    # Match Excel data
    user_data = df[
        df['CLEARANCE_ID'].astype(str).str.strip() == clean_id.strip()
    ]

    if user_data.empty:
        return "Invalid Card or Record Not Found", 404

    # Get first matching row
    data = user_data.iloc[0].to_dict()

    # Create list of all Excel columns
    columns = df.columns.tolist()

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Emigration Clearance Verification</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                padding: 20px;
                margin: 0;
            }

            .card {
                background: white;
                max-width: 600px;
                margin: 20px auto;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 0 15px rgba(0,0,0,0.12);
            }

            .header {
                text-align: center;
                color: green;
                margin-bottom: 25px;
            }

            .info {
                border-bottom: 1px solid #eee;
                padding: 12px 0;
                display: flex;
                flex-wrap: wrap;
            }

            .label {
                font-weight: bold;
                color: #555;
                width: 40%;
            }

            .value {
                color: #222;
                width: 60%;
                word-break: break-word;
            }

            .status {
                text-align: center;
                color: green;
                font-weight: bold;
                margin-top: 25px;
                padding: 12px;
                background: #f0fff0;
                border-radius: 8px;
            }

            @media (max-width: 600px) {
                body {
                    padding: 10px;
                }

                .card {
                    padding: 18px;
                }

                .label,
                .value {
                    width: 100%;
                }

                .value {
                    margin-top: 5px;
                }
            }
        </style>
    </head>

    <body>

        <div class="card">

            <h2 class="header">
                ✓ Emigration Clearance Verified
            </h2>

            {% for column in columns %}

                <div class="info">

                    <span class="label">
                        {{ column }}
                    </span>

                    <span class="value">

                        {% if column == 'CLEARANCE_ID' %}
                            RS-I-2026-{{ data[column] }}

                        {% else %}
                            {{ data[column] }}

                        {% endif %}

                    </span>

                </div>

            {% endfor %}

            <div class="status">
                Status: Active
            </div>

        </div>

    </body>
    </html>
    """, data=data, columns=columns)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)