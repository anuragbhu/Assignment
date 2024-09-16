from threading import Thread
from datetime import datetime, timedelta
from flask import Flask, jsonify
import time
from data_loaders.process_products import load_product_data
from data_loaders.process_transactions import load_existing_transactions

app = Flask(__name__)

# In-memory storage
# products
product_data = {}
product_file_path = '../products/Product.csv'

# Transactions
last_loaded_time = 0
transaction_data = {}
transactions_folder_path = '../Transactions'


def monitor_folder(folder_path, check_interval=2):
    global transaction_data, last_loaded_time
    while True:
        transaction_data, last_loaded_time = load_existing_transactions(folder_path, transaction_data, last_loaded_time)
        # Wait for the specified interval before checking again
        time.sleep(check_interval)


# REST API: Get transaction by transactionId
@app.route('/assignment/transaction/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    if transaction_id in transaction_data:
        transaction = transaction_data.get(transaction_id)
        product = product_data.get(int(transaction['productId']))
        return jsonify({
            'transactionId': transaction['transactionId'],
            'productName': product.get('productName', 'Unknown'),
            'transactionAmount': transaction['transactionAmount'],
            'transactionDatetime': transaction['transactionDatetime'].strftime('%Y-%m-%d %H:%M')
        })
    return jsonify({'error': 'Transaction not found'}), 404


# REST API: Transaction summary by product over the last N days
@app.route('/assignment/transactionSummaryByProducts/<int:last_n_days>', methods=['GET'])
def transaction_summary_by_products(last_n_days):
    cutoff_date = datetime.now() - timedelta(days=last_n_days)
    summary = {}

    for transaction, details in transaction_data.items():
        if details['transactionDatetime'] >= cutoff_date:
            product_id = details['productId']
            product_name = product_data.get(product_id, {}).get('productName', 'Unknown')
            summary[product_name] = summary.get(product_name, 0) + details['transactionAmount']

    summary_list = [{'productName': name, 'totalAmount': total} for name, total in summary.items()]
    return jsonify({'summary': summary_list})


# REST API: Transaction summary by manufacturing city over the last N days
@app.route('/assignment/transactionSummaryByManufacturingCity/<int:last_n_days>', methods=['GET'])
def transaction_summary_by_city(last_n_days):
    cutoff_date = datetime.now() - timedelta(days=last_n_days)
    summary = {}

    for transaction, details in transaction_data.items():
        if details['transactionDatetime'] >= cutoff_date:
            product_id = details['productId']
            city_name = product_data.get(product_id, {}).get('productManufacturingCity', 'Unknown')
            summary[city_name] = summary.get(city_name, 0) + details['transactionAmount']

    summary_list = [{'cityName': name, 'totalAmount': total} for name, total in summary.items()]
    return jsonify({'summary': summary_list})


# Application entry point
if __name__ == '__main__':
    # Load product data
    product_data = load_product_data(product_file_path, product_data)

    if not hasattr(app, 'monitor_thread_started'):
        monitor_thread = Thread(target=monitor_folder, args=(transactions_folder_path, ))
        monitor_thread.daemon = True  # This makes the thread exit when the main program exits
        monitor_thread.start()

    # Start Flask API server
    app.run(debug=False)
