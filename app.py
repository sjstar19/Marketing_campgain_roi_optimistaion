import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Function to load the dataset
@st.cache_data  # Cache data for performance
def load_data():
    csv_file_path = 'campaign_performance.csv'  # Update this path if necessary
    return pd.read_csv(csv_file_path)

# Load the dataset from CSV file
data = load_data()

# Calculate additional metrics for insights
data['CTR'] = data['Clicks'] / data['Impressions']
data['ROI'] = (data['Revenue'] - data['Spend']) / data['Spend']

# Insights Calculations
insights = {
    'Total Campaigns': data['Campaign_ID'].nunique(),
    'Total Impressions': data['Impressions'].sum(),
    'Total Clicks': data['Clicks'].sum(),
    'Total Conversions': data['Conversions'].sum(),
    'Total Spend': data['Spend'].sum(),
    'Total Revenue': data['Revenue'].sum(),
    'Average CTR': round(data['CTR'].mean(), 4),
    'Average CPA': round(data['CPA'].mean(), 2),
    'Average ROI': round(data['ROI'].mean(), 2),
    'Active Campaigns': data[data['Status'] == 'Active'].shape[0]
}

# Streamlit app title and description
st.title("📊 Marketing Campaign Dashboard")
st.write("This dashboard provides insights into marketing campaign performance.")

# Display raw data in the app (optional)
if st.checkbox("Show raw data"):
    st.write(data)

# Display insights in cards format using columns for horizontal layout
st.header("Key Performance Indicators (KPIs)")
row1, row2 = st.columns(2)

with row1:
    st.metric(label="Total Campaigns", value=insights['Total Campaigns'])
    st.metric(label="Total Impressions", value=f"{insights['Total Impressions']:,}")
    st.metric(label="Total Clicks", value=f"{insights['Total Clicks']:,}")
    st.metric(label="Total Conversions", value=f"{insights['Total Conversions']:,}")

with row2:
    st.metric(label="Total Spend ($)", value=f"${insights['Total Spend']:,.2f}")
    st.metric(label="Total Revenue ($)", value=f"${insights['Total Revenue']:,.2f}")
    st.metric(label="Average CTR", value=f"{insights['Average CTR']:.2%}")
    st.metric(label="Average CPA ($)", value=f"${insights['Average CPA']:.2f}")

# Filters and Slicers using checkboxes and sliders
st.sidebar.header("Filters")
selected_channels = st.sidebar.multiselect("Select Channel:", options=data["Channel"].unique(), default=data["Channel"].unique())
selected_statuses = st.sidebar.multiselect("Select Status:", options=data["Status"].unique(), default=data["Status"].unique())

# Slider for Spend Range
spend_range = st.sidebar.slider("Select Spend Range:", min_value=int(data["Spend"].min()), max_value=int(data["Spend"].max()), value=(int(data["Spend"].min()), int(data["Spend"].max())))

# Filter Data Based on Selections
filtered_data = data[
    (data["Channel"].isin(selected_channels)) &
    (data["Status"].isin(selected_statuses)) &
    (data["Spend"].between(spend_range[0], spend_range[1]))
]

# Visualization: Average ROI by Channel using Streamlit and Matplotlib
st.subheader('Average ROI by Channel')
average_roi = filtered_data.groupby('Channel')['ROI'].mean().reset_index()
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=average_roi, x='Channel', y='ROI', palette='viridis', ax=ax1)
ax1.set_title('Average ROI by Channel', fontsize=16)
ax1.set_xlabel('Channel', fontsize=12)
ax1.set_ylabel('Average ROI', fontsize=12)
plt.xticks(rotation=45)

# Adding tooltips to bar chart
for p in ax1.patches:
    ax1.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')

st.pyplot(fig1)

# Update KPI based on selected channels
if selected_channels:
    channel_data = filtered_data.groupby('Channel').agg(
        Total_Impressions=('Impressions', 'sum'),
        Total_Clicks=('Clicks', 'sum'),
        Total_Conversions=('Conversions', 'sum'),
        Total_Spend=('Spend', 'sum'),
        Total_Revenue=('Revenue', 'sum')
    ).reset_index()
    
    # Update KPI cards dynamically based on selection
    for channel in selected_channels:
        channel_metrics = channel_data[channel_data['Channel'] == channel].iloc[0]
        st.write(f"Metrics for {channel}:")
        st.metric(label="Total Impressions", value=f"{channel_metrics.Total_Impressions:,}")
        st.metric(label="Total Clicks", value=f"{channel_metrics.Total_Clicks:,}")
        st.metric(label="Total Conversions", value=f"{channel_metrics.Total_Conversions:,}")
        st.metric(label="Total Spend ($)", value=f"${channel_metrics.Total_Spend:,.2f}")
        st.metric(label="Total Revenue ($)", value=f"${channel_metrics.Total_Revenue:,.2f}")

# Visualization: Total Spend by Status (Pie Chart)
st.subheader('Total Spend by Campaign Status')
total_spend_status = filtered_data.groupby('Status')['Spend'].sum().reset_index()
fig2, ax2 = plt.subplots(figsize=(8, 8))
ax2.pie(total_spend_status['Spend'], labels=total_spend_status['Status'], autopct='%1.1f%%', startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Total Spend by Campaign Status', fontsize=16)
st.pyplot(fig2)

# Visualization: Click-Through Rate (CTR) Distribution (Histogram)
st.subheader('Click-Through Rate (CTR) Distribution')
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_data['CTR'], bins=20, kde=True, color='blue', ax=ax3)
ax3.set_title('Distribution of Click-Through Rate (CTR)', fontsize=16)
ax3.set_xlabel('CTR', fontsize=12)
ax3.set_ylabel('Frequency', fontsize=12)
st.pyplot(fig3)

# Visualization: Total Revenue vs. Spend (Scatter Plot)
st.subheader('Total Revenue vs. Spend by Channel')
fig4, ax4 = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=filtered_data, x='Spend', y='Revenue', hue='Channel', alpha=0.7, ax=ax4)
ax4.set_title('Total Revenue vs. Spend by Channel', fontsize=16)
ax4.set_xlabel('Spend ($)', fontsize=12)
ax4.set_ylabel('Revenue ($)', fontsize=12)
plt.legend(loc='upper left')
st.pyplot(fig4)

# Visualization: Total Conversions by Campaign Status (Bar Chart)
st.subheader('Total Conversions by Campaign Status')
conversions_by_status = filtered_data.groupby('Status')['Conversions'].sum().reset_index()
fig5, ax5 = plt.subplots(figsize=(10, 5))
sns.barplot(data=conversions_by_status, x='Status', y='Conversions', palette='pastel', ax=ax5)
ax5.set_title('Total Conversions by Campaign Status', fontsize=16)
ax5.set_xlabel('Status', fontsize=12)
ax5.set_ylabel('Total Conversions', fontsize=12)
st.pyplot(fig5)

# Visualization: Average CPA by Channel (Box Plot)
st.subheader('Average CPA by Channel')
fig6, ax6 = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_data, x='Channel', y='CPA', palette='Set2', ax=ax6)
ax6.set_title('Average CPA by Channel', fontsize=16)
ax6.set_xlabel('Channel', fontsize=12)
ax6.set_ylabel('Cost Per Acquisition (CPA)', fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig6)

# Button to print report
if st.button("Generate Report"):
    report_df = filtered_data[['Campaign_ID', 'Campaign_Name', 'Channel',
                                'Impressions', 'Clicks', 'CTR',
                                'Conversions', 'CPA','Spend',
                                'Revenue','ROI','Status']]
    
    # Save report to CSV
    report_df.to_csv("campaign_performance_report.csv", index=False)

    # Provide download link for the report
    with open("campaign_performance_report.csv", "rb") as file:
        btn = st.download_button(
            label="Download Report",
            data=file,
            file_name="campaign_performance_report.csv",
            mime="text/csv"
        )

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Dashboard is ready!")