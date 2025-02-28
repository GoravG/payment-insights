from utils.helper import to_native


def get_transaction_insights(data):
    min_transaction = to_native(data["Amount"].min().round(2))
    max_transaction = to_native(data["Amount"].max().round(2))
    avg_transaction = to_native(data["Amount"].mean().round(2))
    total_sales = data["Amount"].agg(["sum"])

    transaction_insights = {
        "highest_transaction": max_transaction,
        "lowest_transaction": min_transaction,
        "average_transaction": avg_transaction,
        "total_sales": total_sales,
    }
    return transaction_insights
