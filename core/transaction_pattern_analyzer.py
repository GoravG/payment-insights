import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import json
from datetime import datetime

class TransactionPatternAnalyzer:
    _instance = None
    _is_initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TransactionPatternAnalyzer, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not TransactionPatternAnalyzer._is_initialized:
            self.patterns = {}
            TransactionPatternAnalyzer._is_initialized = True
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TransactionPatternAnalyzer()
        return cls._instance
    
    def extract_features(self, json_data):
        """Extract relevant features from the JSON structure"""
        report = json_data['report']
        
        # Extract daily patterns
        daily_data = pd.DataFrame(report['daily_patterns']).T
        self.daily_features = {
            'daily_variation': daily_data['average_amount'].std(),
            'weekend_weekday_ratio': report['time_comparison']['weekend_average'] / 
                                   report['time_comparison']['weekday_average'],
            'busy_day_ratio': daily_data['transaction_count'].max() / 
                            daily_data['transaction_count'].min()
        }
        
        # Extract hourly patterns
        hourly_data = pd.DataFrame(report['hourly_transactions']['hourly_transactions']).T
        self.hourly_features = {
            'peak_hour_concentration': (hourly_data['total_amount'].max() / 
                                      hourly_data['total_amount'].sum()),
            'active_hours': (hourly_data['transaction_count'] > 0).sum(),
            'hourly_amount_std': hourly_data['average_amount'].std()
        }
        
        # Combine features
        self.features = {**self.daily_features, **self.hourly_features}
    
    def analyze_new_data(self, json_data):
        """Analyze new JSON data and provide insights without historical comparison"""
        self.extract_features(json_data)
        
        # Generate insights based on current data patterns
        insights = {
            'pattern_metrics': self.features,
            'business_insights': {
                'daily_consistency_score': round(1 / self.daily_features['daily_variation'], 2),
                'peak_hour_efficiency': round(self.hourly_features['peak_hour_concentration'], 2),
                'operational_hours_optimization': {
                    'active_hours': self.hourly_features['active_hours'],
                    'weekend_efficiency': round(self.daily_features['weekend_weekday_ratio'], 2)
                }
            },
            'recommendations': self._generate_recommendations()
        }
        
        return insights
    
    def _generate_recommendations(self):
        """Generate business recommendations based on current patterns"""
        recommendations = []
        
        # Analyze weekend efficiency
        if self.daily_features['weekend_weekday_ratio'] > 1.2:
            recommendations.append("Weekend operations are significantly busier than weekdays")
        elif self.daily_features['weekend_weekday_ratio'] < 0.8:
            recommendations.append("Weekend operations show lower activity than weekdays")
            
        # Analyze peak hour concentration
        if self.hourly_features['peak_hour_concentration'] > 0.3:
            recommendations.append("Business shows high concentration during peak hours")
            
        # Analyze operational hours
        if self.hourly_features['active_hours'] < 12:
            recommendations.append(f"Business is active for {self.hourly_features['active_hours']} hours")
            
        return recommendations

    # TODO: Future enhancement - Add historical data training
    def train_with_historical_data(self, historical_jsons):
        """
        Future enhancement: Train the analyzer with historical data
        This method will be implemented when historical data becomes available
        """
        pass