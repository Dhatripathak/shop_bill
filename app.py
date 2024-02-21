from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['invoices']
collection = db['invoices']

@app.route('/push_invoice')
def push_invoice():

    # Tax details
    tax_type = "GST"
    tax_rate = 0.18  # 18%

    # Form data to be inserted into MongoDB
    data = {
        "date": datetime.now(),
        "invoice_details": {
            "invoice_number": "DEL5-5278371",
            "order_date": "18.12.2023",
            "invoice_details": "HR-DEL5-1014-2324",
            "invoice_date": "19.12.2023"
        },
        "seller_details": {
            "seller_address": "[*Rect/Killa Nos. 38//8/2 min, 192//22/1,196//2/1/1]",
            "gst_number": "[06AAPCA6346P1ZZ ]",
            "shipped_from_address": "[Village Binola, National Highway -8]"
        },
        "billing_address": "[pakshi vihar campus]",
        "shipping_address": "[pakshi vihar campus]",
        "materials": [
            {
                "serial_number": 1,
                "material": "name1",
                "quantity": 2,
                "price": 10.00,
                "tax_type": tax_type,
                "tax_rate": tax_rate,
                "tax_amount": round(2 * 10.00 * tax_rate, 2),
                "total_amount": round((2 * 10.00) + (2 * 10.00 * tax_rate), 2)
            },
            {
                "serial_number": 2,
                "material": "name2",
                "quantity": 1,
                "price": 15.00,
                "tax_type": tax_type,
                "tax_rate": tax_rate,
                "tax_amount": round(1 * 15.00 * tax_rate, 2),
                "total_amount": round((1 * 15.00) + (1 * 15.00 * tax_rate), 2)
            }
        ],
    }

    collection.insert_one(data)

    return "Invoice data with tax details pushed successfully!"

def calculate_totals(materials):
    total_tax = round(sum(item["tax_amount"] for item in materials), 2)
    total_amount = round(sum(item["total_amount"] for item in materials), 2)
    return total_tax, total_amount


# Route to fetch invoice data and render invoices.html
@app.route('/invoice')
def get_invoices():
    invoice = collection.find_one()
    if invoice:
        materials = invoice.get("materials", [])
        total_tax, total_amount = calculate_totals(materials)
        return render_template('invoice.html', invoices=invoice, total_tax=total_tax, total_amount=total_amount)
    else:
        return "No invoice found"

if __name__ == "__main__":
    app.run(debug=True)
