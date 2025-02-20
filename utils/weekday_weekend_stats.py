from utils.helper import convert_numpy_type

def get_weekend_weekday_stats(data):
	weekend_mask = data['Day_of_Week'].isin(['Saturday', 'Sunday'])
	weekend_avg = convert_numpy_type(data[weekend_mask]['Amount'].mean())
	weekday_avg = convert_numpy_type(data[~weekend_mask]['Amount'].mean())
	time_comparison = {
			"weekend_average": weekend_avg,
			"weekday_average": weekday_avg,
			"difference": abs(weekend_avg - weekday_avg),
			"higher_period": "weekend" if weekend_avg > weekday_avg else "weekday"
		}
	return time_comparison