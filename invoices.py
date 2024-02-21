from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['invoices']
collection = db['invoices']

@app.route('/')
def index():
    return render_template('invoiceform.html')

@app.route('/push_invoice', methods=['POST'])
def push_invoice():
    # Parse form data
    invoice_number = request.form['invoice_number']
    order_date = request.form['order_date']
    invoice_details = request.form['invoice_details']
    invoice_date = request.form['invoice_date']
    seller_address = request.form['seller_address']
    gst_number = request.form['gst_number']
    shipped_from_address = request.form['shipped_from_address']
    billing_address = request.form['billing_address']
    shipping_address = request.form['shipping_address']
    item_1 = request.form['item_1']
    quantity_1 = int(request.form['quantity_1'])
    price_1 = float(request.form['price_1'])

    # Calculate tax amount
    tax_rate = 0.18
    tax_amount = tax_rate * price_1 * quantity_1

    # Calculate total amount
    total_amount = price_1 * quantity_1 + tax_amount

    # Prepare data to be inserted into MongoDB
    data = {
        "date": datetime.now(),
        "invoice_details": {
            "invoice_number": invoice_number,
            "order_date": order_date,
            "invoice_details": invoice_details,
            "invoice_date": invoice_date
        },
        "seller_details": {
            "seller_address": seller_address,
            "gst_number": gst_number,
            "shipped_from_address": shipped_from_address
        },
        "billing_address": billing_address,
        "shipping_address": shipping_address,
        "items": [
            {
                "item": item_1,
                "quantity": quantity_1,
                "price": price_1,
                "tax_rate": tax_rate,
                "tax_type": "VAT",
                "tax_amount": tax_amount,
                "total_amount": total_amount
            }
        ]
    }

    # Insert data into MongoDB
    collection.insert_one(data)

    return "Invoice data inserted into MongoDB successfully!"

if __name__ == "__main__":
    app.run(debug=True)
