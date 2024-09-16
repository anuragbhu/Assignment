import csv


# Load product data on startup
def load_product_data(filepath, product_data):
    with open(filepath, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        # next(reader, None)
        for row in reader:
            product_data[int(row['productId'])] = {
                'productId': int(row['productId']),
                'productName': row['productName'],
                'productManufacturingCity': row['productManufacturingCity']
            }
    return product_data
