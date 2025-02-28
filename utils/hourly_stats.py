from utils.helper import to_native


def get_hourly_stats(data):
    # Filter valid hours
    filtered_data = data[(data["Hour"] >= 0) & (data["Hour"] <= 24)]

    # Calculate hourly statistics
    hourly_stats = (
        filtered_data.groupby("Hour")["Amount"].agg(["mean", "count", "sum"]).round(2)
    )

    # Find peak and lowest hours
    peak_hour = hourly_stats["sum"].idxmax()
    lowest_hour = hourly_stats["sum"].idxmin()

    def format_hour_range(hour):
        # Convert to 12-hour format with AM/PM
        period1 = "AM" if hour < 12 else "PM"
        period2 = period1  # The period won't change within the same hour

        # Convert to 12-hour format
        hour_12 = hour if hour <= 12 else hour - 12
        # Handle midnight and noon special cases
        hour_12 = 12 if hour == 0 else hour_12
        hour_12 = 12 if hour == 12 else hour_12

        return f"{hour_12}{period1}-{hour_12}:59{period2}"

    # Create combined dictionary
    hourly_analysis = {
        "summary": {
            "peak_hour": format_hour_range(peak_hour),
            "lowest_hour": format_hour_range(lowest_hour),
            "peak_hour_amount": to_native(hourly_stats.loc[peak_hour, "sum"]),
            "lowest_hour_amount": to_native(hourly_stats.loc[lowest_hour, "sum"]),
        },
        "details": {
            format_hour_range(hour): {
                "total_amount": to_native(stats["sum"]),
                "transaction_count": to_native(stats["count"]),
                "average_amount": to_native(stats["mean"]),
            }
            for hour, stats in hourly_stats.iterrows()
        },
    }

    return hourly_analysis
