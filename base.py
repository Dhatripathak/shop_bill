from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']  # Replace 'your_database_name' with your actual database name
collection = db['your_collection_name']  # Replace 'your_collection_name' with your actual collection name

# Define routes
@app.route('/invoice', methods=['GET'])
def get_invoice():
    # Fetch data from MongoDB
    invoice_data = collection.find_one()
    # Return the data as JSON
    return jsonify(invoice_data)

if __name__ == '__main__':
    app.run(debug=True)
    </style>
  </head>
  <body>
    <div class="invoice">
      <div class="invoice-header">
        <div>
          <p class="date">Date: {{ invoices.date }}</p>
        </div>
        <div class="top-right">
          Tax Invoice/Bill of Supply/Cash Memo<br />
          (Original for Recipient)
        </div>
      </div>
      <div class="seller-details">
        <p class="address">
          <strong>Seller Address:</strong> {{
          invoices.seller_details.seller_address }}
        </p>
        <p class="address">
          <strong>GST No:</strong> {{ invoices.seller_details.gst_number }}
        </p>
        <p class="address">
          <strong>Shipped From:</strong> {{
          invoices.seller_details.shipped_from_address }}
        </p>
        <p>
          <strong>Invoice Number:</strong> {{
          invoices.invoice_details.invoice_number }}
        </p>
        <p>
          <strong>Order Date:</strong> {{ invoices.invoice_details.order_date }}
        </p>
        <p>
          <strong>Invoice Details:</strong> {{
          invoices.invoice_details.invoice_details }}
        </p>
        <p>
          <strong>Invoice Date:</strong> {{
          invoices.invoice_details.invoice_date }}
        </p>
      </div>
      <div class="addresses right-align">
        <div class="billing-address">
          <h3>Billing Address:</h3>
          <p>{{ invoices.billing_address }}</p>
        </div>
        <div class="shipping-address">
          <h3>Shipping Address:</h3>
          <p>{{ invoices.shipping_address }}</p>
        </div>
      </div>
      <div class="table-container">
        <table>
          <thead>
              <tr>
                  <th><strong>S.No</strong></th>
                  <th><strong>Item</strong></th>
                  <th><strong>Quantity</strong></th>
                  <th><strong>Price</strong></th>
                  <th><strong>Tax Rate</strong></th>
                  <th><strong>Tax Type</strong></th>
                  <th><strong>Tax Amount</strong></th>
                  <th><strong>Total Amount</strong></th>
              </tr>
          </thead>
          <tbody>
              {% for item in invoice_data.items %}
              <tr>
                  <td>{{ item.serial_number }}</td>
                  <td>{{ item.item }}</td>
                  <td>{{ item.quantity }}</td>
                  <td>${{ item.price }}</td>
                  <td>{{ item.tax_rate }}</td>
                  <td>{{ item.tax_type }}</td>
                  <td>${{ item.tax_amount }}</td>
                  <td>${{ item.total_amount }}</td>
              </tr>
              {% endfor %}
                 </tbody>
      </table>
      </div>
    </div>
  </body>
</html>

