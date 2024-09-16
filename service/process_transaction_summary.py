from datetime import datetime, timedelta


def process_summary(last_n_days, transaction_data, product_data, summary_for):
    cutoff_date = datetime.now() - timedelta(days=last_n_days)
    summary = {}

    for transaction, details in transaction_data.items():
        if details['transactionDatetime'] >= cutoff_date:
            product_id = details['productId']
            summary_name = product_data.get(product_id, {}).get(summary_for, 'Unknown')
            summary[summary_name] = summary.get(summary_name, 0) + details['transactionAmount']

    return summary
