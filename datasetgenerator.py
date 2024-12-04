#python dataset genrator 
import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)

# Define parameters
num_campaigns = 100

# Generate campaign data
data = {
    "Campaign_ID": [f"CID_{i+1}" for i in range(num_campaigns)],
    "Campaign_Name": [f"Campaign_{random.choice(['A', 'B', 'C'])}_{i+1}" for i in range(num_campaigns)],
    "Channel": random.choices(["Google Ads", "Facebook Ads", "Email Marketing", "LinkedIn Ads"], k=num_campaigns),
    "Impressions": np.random.randint(10000, 500000, num_campaigns),
    "Clicks": np.random.randint(100, 20000, num_campaigns),
    "CTR": lambda x: round(x['Clicks'] / x['Impressions'], 4) if x['Impressions'] > 0 else 0,
    "Conversions": np.random.randint(10, 500, num_campaigns),
    "CPA": np.random.uniform(50, 500, num_campaigns),  # Cost per acquisition
    "Spend": lambda x: x['CPA'] * x['Conversions'],
    "Revenue": np.random.uniform(1000, 100000, num_campaigns),
    "ROI": lambda x: round((x['Revenue'] - x['Spend']) / x['Spend'], 2),
    "Status": random.choices(["Active", "Paused", "Completed"], k=num_campaigns)
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Apply calculated fields
df['CTR'] = df.apply(lambda x: round(x['Clicks'] / x['Impressions'], 4) if x['Impressions'] > 0 else 0, axis=1)
df['Spend'] = df.apply(lambda x: round(x['CPA'] * x['Conversions'], 2), axis=1)
df['ROI'] = df.apply(lambda x: round((x['Revenue'] - x['Spend']) / x['Spend'], 2) if x['Spend'] > 0 else 0, axis=1)

# Export dataset to CSV
dataset_path = "campaign_performance.csv"
df.to_csv(dataset_path, index=False)

print(f"Dataset generated and saved to {dataset_path}. Here's a preview:")
print(df.head())
