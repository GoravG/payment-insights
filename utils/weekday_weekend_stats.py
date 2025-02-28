from utils.helper import to_native


def get_weekend_data(data):
    weekend_mask = data["Day_of_Week"].isin(["Saturday", "Sunday"])
    weekend_data = data[weekend_mask]
    return weekend_data


def get_weekday_data(data):
    weekend_mask = data["Day_of_Week"].isin(["Saturday", "Sunday"])
    weekday_data = data[~weekend_mask]
    return weekday_data


def calculate_summary(data):
    return {
        "average": to_native(data["Amount"].mean().round(2)),
        "total": to_native(data["Amount"].sum().round(2)),
        "count": to_native(len(data)),
        "max": to_native(data["Amount"].max().round(2)),
        "days_count": to_native(data["Date"].nunique()),
    }


def calculate_daily_average(total, days):
    return round(to_native(total / days), 2) if days > 0 else 0


def calculate_percentage(part, whole):
    return round(to_native(part / whole * 100), 2) if whole > 0 else 0


def compare_periods(weekend_avg, weekday_avg, weekend_daily_avg, weekday_daily_avg):
    return {
        "difference_in_average": round(abs(weekend_avg - weekday_avg), 2),
        "difference_in_daily_average": round(
            abs(weekend_daily_avg - weekday_daily_avg), 2
        ),
        "higher_average_period": "weekend" if weekend_avg > weekday_avg else "weekday",
        "higher_daily_period": (
            "weekend" if weekend_daily_avg > weekday_daily_avg else "weekday"
        ),
        "weekend_to_weekday_ratio": (
            round(to_native(weekend_avg / weekday_avg), 2) if weekday_avg > 0 else 0
        ),
    }


def get_weekend_weekday_stats(data):
    # Calculate weekend and weekday summaries
    weekend_data = get_weekend_data(data)
    weekday_data = get_weekday_data(data)

    weekend_summary = calculate_summary(weekend_data)
    weekday_summary = calculate_summary(weekday_data)

    # Daily averages
    weekend_daily_avg = calculate_daily_average(
        weekend_summary["total"], weekend_summary["days_count"]
    )
    weekday_daily_avg = calculate_daily_average(
        weekday_summary["total"], weekday_summary["days_count"]
    )

    # Percentage of total
    total_amount = weekend_summary["total"] + weekday_summary["total"]
    weekend_percentage = calculate_percentage(weekend_summary["total"], total_amount)
    weekday_percentage = calculate_percentage(weekday_summary["total"], total_amount)

    # Comparison
    comparison = compare_periods(
        weekend_summary["average"],
        weekday_summary["average"],
        weekend_daily_avg,
        weekday_daily_avg,
    )

    # Prepare final dictionary
    time_comparison = {
        "weekend": {
            "total_amount": weekend_summary["total"],
            "transaction_count": weekend_summary["count"],
            "average_per_transaction": weekend_summary["average"],
            "average_per_day": weekend_daily_avg,
            "percentage_of_total": weekend_percentage,
            "max_transaction": weekend_summary["max"],
            "days_count": weekend_summary["days_count"],
        },
        "weekday": {
            "total_amount": weekday_summary["total"],
            "transaction_count": weekday_summary["count"],
            "average_per_transaction": weekday_summary["average"],
            "average_per_day": weekday_daily_avg,
            "percentage_of_total": weekday_percentage,
            "max_transaction": weekday_summary["max"],
            "days_count": weekday_summary["days_count"],
        },
        "comparison": comparison,
    }

    return time_comparison
