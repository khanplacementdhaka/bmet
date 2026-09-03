from flask import Flask, render_template_string, abort
import pandas as pd
import os

app = Flask(__name__)

# Route to handle verification link
@app.route('/verify/<full_id>')
def verify(full_id):
    if not os.path.exists("data.xlsx"):
        return "Database file not found.", 500

    df = pd.read_excel("data.xlsx")
    
    # Extracting the ID from the full URL string (Removing prefix)
    clean_id = full_id.replace("RS-I-2026-", "")
    
    # Matching with Excel data
    user_data = df[df['CLEARANCE_ID'].astype(str) == clean_id]
    
    if not user_data.empty:
        data = user_data.iloc[0].to_dict()
        # Simple HTML Interface
        return render_template_string("""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial; background: #f4f4f4; padding: 20px; }
                .card { background: white; max-width: 400px; margin: auto; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                .header { text-align: center; color: green; }
                .info { border-bottom: 1px solid #eee; padding: 10px 0; }
                .label { font-weight: bold; color: #555; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2 class="header">Emigration Clearance Verified</h2>
                <div class="info"><span class="label">Name:</span> {{ d['NAME'] }}</div>
                <div class="info"><span class="label">BMET ID:</span> {{ d['BMET_ID'] }}</div>
                <div class="info"><span class="label">Passport:</span> {{ d['PASSPORT'] }}</div>
                <div class="info"><span class="label">Clearance ID:</span> RS-I-2026-{{ d['CLEARANCE_ID'] }}</div>
                <div class="info"><span class="label">Destination:</span> Serbia</div>
                <p style="text-align:center; color:gray;">Status: Active</p>
            </div>
        </body>
        </html>
        """, d=data)
    else:
        return "Invalid Card or Record Not Found", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)