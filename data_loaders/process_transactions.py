import csv
from datetime import datetime
import os


# Process incoming transaction files
def process_transaction_file(filepath, transaction_data):
    print(f"Processing file: {filepath}")
    with open(filepath, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            transaction = {
                'transactionId': int(row[0]),
                'productId': int(row[1]),
                'transactionAmount': float(row[2]),
                'transactionDatetime': datetime.strptime(row[3], '%d-%m-%Y %H:%M')
            }
            # Store the transaction with transactionId as the key
            transaction_data[int(row[0])] = transaction
    return transaction_data


# Load existing transactions on startup
# Assuming last_loaded_time is a UNIX timestamp (seconds since epoch)
def load_existing_transactions(folder_path, transaction_data, last_loaded_time):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # Get the file's modification time
        file_mod_time = os.path.getmtime(filepath)

        # Only process if the file is newer than the last loaded timestamp
        if file_mod_time > last_loaded_time:
            transaction_data = process_transaction_file(filepath, transaction_data)
            # Update the last_loaded_time to the current file's timestamp
            last_loaded_time = file_mod_time
    return transaction_data, last_loaded_time
