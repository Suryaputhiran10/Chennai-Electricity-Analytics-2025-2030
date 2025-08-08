
"""
Chennai Electricity Demand and Cost Analytics Program
====================================================
Complete Business Analytics Solution with Data Loading and Visualization
Author: Chennai Electricity Analytics Team
Date: August 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ChennaiElectricityAnalytics:
    """
    Main class for Chennai Electricity Demand and Cost Analytics
    """

    def __init__(self):
        """Initialize the analytics class"""
        self.data = {}
        self.figures = []
        print("Chennai Electricity Analytics Program Initialized")
        print("=" * 60)

    def load_all_data(self):
        """Load all CSV datasets"""
        try:
            # Dictionary mapping data types to file names
            data_files = {
                'historical': 'chennai_electricity_historical_2020_2024.csv',
                'monthly_detailed': 'chennai_electricity_monthly_detailed_2023_2025.csv',
                'projections': 'chennai_electricity_projections_2025_2030.csv',
                'sector_wise': 'chennai_electricity_sector_wise_2025_2030.csv',
                'daily_load': 'chennai_electricity_daily_load_profile.csv',
                'infrastructure': 'chennai_electricity_infrastructure_2025_2030.csv',
                'economic': 'chennai_economic_demographic_factors_2020_2030.csv',
                'weather': 'chennai_weather_data_2023_2025.csv',
                'tariff': 'chennai_electricity_tariff_structure_2025_2030.csv'
            }

            # Load each dataset
            for key, filename in data_files.items():
                try:
                    self.data[key] = pd.read_csv(filename)
                    print(f"✓ Loaded {filename} - Shape: {self.data[key].shape}")
                except FileNotFoundError:
                    print(f"⚠ Warning: {filename} not found, skipping...")
                    continue

            print(f"\n✅ Successfully loaded {len(self.data)} datasets")
            return True

        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return False

    def display_data_summary(self):
        """Display summary of all loaded datasets"""
        print("\n" + "=" * 60)
        print("DATA SUMMARY")
        print("=" * 60)

        for key, df in self.data.items():
            print(f"\n{key.upper().replace('_', ' ')} DATA:")
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            if len(df) <= 10:
                print("Sample Data:")
                print(df.to_string(index=False))
            else:
                print("First 3 rows:")
                print(df.head(3).to_string(index=False))

    def analyze_historical_trends(self):
        """Analyze historical electricity trends"""
        if 'historical' not in self.data:
            print("❌ Historical data not available")
            return

        df = self.data['historical']

        print("\n" + "=" * 60)
        print("HISTORICAL TRENDS ANALYSIS (2020-2024)")
        print("=" * 60)

        # Calculate growth rates
        df['Demand_Growth_%'] = df['Demand_MU'].pct_change() * 100
        df['Cost_Growth_%'] = df['Cost_Rs_per_unit'].pct_change() * 100

        # Calculate CAGR
        demand_cagr = ((df['Demand_MU'].iloc[-1] / df['Demand_MU'].iloc[0]) ** (1/4) - 1) * 100
        cost_cagr = ((df['Cost_Rs_per_unit'].iloc[-1] / df['Cost_Rs_per_unit'].iloc[0]) ** (1/4) - 1) * 100

        print(f"Demand CAGR (2020-2024): {demand_cagr:.2f}%")
        print(f"Cost CAGR (2020-2024): {cost_cagr:.2f}%")
        print(f"Peak Demand Growth: {df['Peak_Demand_MW'].iloc[-1] - df['Peak_Demand_MW'].iloc[0]:.0f} MW")

        return df

    def analyze_seasonal_patterns(self):
        """Analyze seasonal electricity consumption patterns"""
        if 'monthly_detailed' not in self.data:
            print("❌ Monthly detailed data not available")
            return

        df = self.data['monthly_detailed']

        print("\n" + "=" * 60)
        print("SEASONAL PATTERNS ANALYSIS")
        print("=" * 60)

        # Calculate average by month across years
        monthly_avg = df.groupby('Month')['Demand_MU'].mean().reset_index()
        monthly_avg['Seasonal_Index'] = monthly_avg['Demand_MU'] / monthly_avg['Demand_MU'].mean()

        # Identify peak and low months
        peak_months = monthly_avg.nlargest(3, 'Demand_MU')
        low_months = monthly_avg.nsmallest(3, 'Demand_MU')

        print("PEAK DEMAND MONTHS:")
        print(peak_months[['Month', 'Demand_MU', 'Seasonal_Index']].to_string(index=False))

        print("\nLOW DEMAND MONTHS:")
        print(low_months[['Month', 'Demand_MU', 'Seasonal_Index']].to_string(index=False))

        return monthly_avg

    def analyze_sector_wise_consumption(self):
        """Analyze sector-wise electricity consumption"""
        if 'sector_wise' not in self.data:
            print("❌ Sector-wise data not available")
            return

        df = self.data['sector_wise']

        print("\n" + "=" * 60)
        print("SECTOR-WISE CONSUMPTION ANALYSIS")
        print("=" * 60)

        # Analyze 2025 and 2030 data
        df_2025 = df[df['Year'] == 2025]
        df_2030 = df[df['Year'] == 2030]

        print("2025 SECTOR BREAKDOWN:")
        print(df_2025[['Sector', 'Demand_MU', 'Share_%']].to_string(index=False))

        print("\n2030 PROJECTED SECTOR BREAKDOWN:")
        print(df_2030[['Sector', 'Demand_MU', 'Share_%']].to_string(index=False))

        # Calculate sector growth
        sector_growth = df_2030.set_index('Sector')['Demand_MU'] / df_2025.set_index('Sector')['Demand_MU'] - 1
        sector_growth = sector_growth * 100

        print("\nSECTOR GROWTH (2025-2030):")
        for sector, growth in sector_growth.items():
            print(f"{sector}: {growth:.1f}%")

        return df_2025, df_2030

    def create_demand_projection_chart(self):
        """Create demand projection visualization"""
        if 'projections' not in self.data:
            print("❌ Projection data not available")
            return

        df = self.data['projections']

        # Create dual-axis chart
        fig, ax1 = plt.subplots(figsize=(12, 8))

        # Demand bars
        bars = ax1.bar(df['Year'], df['Demand_MU'], alpha=0.7, color='skyblue', 
                      label='Demand (MU)', width=0.6)
        ax1.set_xlabel('Year', fontsize=12)
        ax1.set_ylabel('Demand (Million Units)', fontsize=12, color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Add value labels on bars
        for bar, value in zip(bars, df['Demand_MU']):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'{value:,.0f}', ha='center', va='bottom', fontsize=10)

        # Cost line on secondary axis
        ax2 = ax1.twinx()
        line = ax2.plot(df['Year'], df['Cost_Rs_per_unit'], color='red', 
                       marker='o', linewidth=2, markersize=6, label='Cost (Rs/unit)')
        ax2.set_ylabel('Cost (Rs per unit)', fontsize=12, color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Add value labels on line
        for x, y in zip(df['Year'], df['Cost_Rs_per_unit']):
            ax2.annotate(f'Rs {y:.2f}', (x, y), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontsize=9)

        # Title and styling
        plt.title('Chennai Electricity: Demand Growth vs Cost Increase (2025-2030)', 
                 fontsize=14, fontweight='bold', pad=20)

        # Add grid
        ax1.grid(True, alpha=0.3)

        # Add legends
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        plt.tight_layout()
        plt.show()

        return fig

    def create_seasonal_heatmap(self):
        """Create seasonal demand heatmap"""
        if 'monthly_detailed' not in self.data:
            print("❌ Monthly detailed data not available")
            return

        df = self.data['monthly_detailed']

        # Pivot data for heatmap
        heatmap_data = df.pivot(index='Year', columns='Month_Num', values='Demand_MU')

        # Create heatmap
        plt.figure(figsize=(14, 6))
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Demand (MU)'})

        plt.title('Chennai Monthly Electricity Demand Heatmap (2023-2025)', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Year', fontsize=12)

        # Customize month labels
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        plt.xticks(range(12), month_labels)

        plt.tight_layout()
        plt.show()

    def create_sector_pie_chart(self):
        """Create sector-wise consumption pie chart"""
        if 'sector_wise' not in self.data:
            print("❌ Sector-wise data not available")
            return

        df = self.data['sector_wise']
        df_2025 = df[df['Year'] == 2025]

        # Create pie chart
        plt.figure(figsize=(10, 8))
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']

        wedges, texts, autotexts = plt.pie(df_2025['Demand_MU'], 
                                          labels=df_2025['Sector'],
                                          colors=colors,
                                          autopct='%1.1f%%',
                                          startangle=90,
                                          explode=(0.05, 0.05, 0.05, 0.05, 0.05))

        plt.title('Chennai Electricity Consumption by Sector (2025)', 
                 fontsize=14, fontweight='bold')

        # Add legend with values
        legend_labels = [f"{sector}: {demand:,.0f} MU" 
                        for sector, demand in zip(df_2025['Sector'], df_2025['Demand_MU'])]
        plt.legend(wedges, legend_labels, title="Sectors", loc="center left", 
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.tight_layout()
        plt.show()

    def create_daily_load_profile(self):
        """Create daily load profile visualization"""
        if 'daily_load' not in self.data:
            print("❌ Daily load data not available")
            return

        df = self.data['daily_load']

        # Create subplot for weekdays vs weekends
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Weekday profile
        weekday_data = df[~df['Day'].isin(['Saturday', 'Sunday'])]
        weekday_avg = weekday_data.groupby('Hour')['Demand_MW'].mean()

        ax1.plot(weekday_avg.index, weekday_avg.values, marker='o', linewidth=2, 
                color='blue', markersize=4)
        ax1.fill_between(weekday_avg.index, weekday_avg.values, alpha=0.3, color='blue')
        ax1.set_title('Weekday Load Profile', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Hour of Day')
        ax1.set_ylabel('Demand (MW)')
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(range(0, 24, 2))

        # Weekend profile
        weekend_data = df[df['Day'].isin(['Saturday', 'Sunday'])]
        weekend_avg = weekend_data.groupby('Hour')['Demand_MW'].mean()

        ax2.plot(weekend_avg.index, weekend_avg.values, marker='o', linewidth=2, 
                color='red', markersize=4)
        ax2.fill_between(weekend_avg.index, weekend_avg.values, alpha=0.3, color='red')
        ax2.set_title('Weekend Load Profile', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Hour of Day')
        ax2.set_ylabel('Demand (MW)')
        ax2.grid(True, alpha=0.3)
        ax2.set_xticks(range(0, 24, 2))

        plt.suptitle('Chennai Daily Electricity Load Profiles', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

    def create_infrastructure_dashboard(self):
        """Create infrastructure development dashboard"""
        if 'infrastructure' not in self.data:
            print("❌ Infrastructure data not available")
            return

        df = self.data['infrastructure']

        # Create 2x2 subplot dashboard
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        # Generation Capacity
        ax1.bar(df['Year'], df['Generation_Capacity_MW'], color='green', alpha=0.7)
        ax1.set_title('Generation Capacity Growth', fontweight='bold')
        ax1.set_ylabel('Capacity (MW)')
        ax1.grid(True, alpha=0.3)

        # Renewable vs Total Capacity
        ax2.plot(df['Year'], df['Generation_Capacity_MW'], marker='o', 
                label='Total Capacity', linewidth=2)
        ax2.plot(df['Year'], df['Renewable_Capacity_MW'], marker='s', 
                label='Renewable Capacity', linewidth=2)
        ax2.set_title('Renewable Energy Integration', fontweight='bold')
        ax2.set_ylabel('Capacity (MW)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Smart Meter Deployment
        ax3.bar(df['Year'], df['Smart_Meters_Deployed'], color='orange', alpha=0.7)
        ax3.set_title('Smart Meter Deployment', fontweight='bold')
        ax3.set_ylabel('Meters Deployed')
        ax3.grid(True, alpha=0.3)

        # T&D Losses Reduction
        ax4.plot(df['Year'], df['T_D_Losses_%'], marker='o', color='red', linewidth=2)
        ax4.set_title('Transmission & Distribution Losses', fontweight='bold')
        ax4.set_ylabel('T&D Losses (%)')
        ax4.grid(True, alpha=0.3)

        plt.suptitle('Chennai Electricity Infrastructure Dashboard (2025-2030)', 
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()

    def generate_comprehensive_report(self):
        """Generate comprehensive analytics report"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE CHENNAI ELECTRICITY ANALYTICS REPORT")
        print("=" * 80)

        # Load and analyze data
        self.load_all_data()
        self.display_data_summary()

        # Perform analyses
        print("\n🔍 Analyzing Historical Trends...")
        self.analyze_historical_trends()

        print("\n🔍 Analyzing Seasonal Patterns...")
        self.analyze_seasonal_patterns()

        print("\n🔍 Analyzing Sector-wise Consumption...")
        self.analyze_sector_wise_consumption()

        # Generate visualizations
        print("\n📊 Creating Visualizations...")
        print("\n1. Demand Projection Chart:")
        self.create_demand_projection_chart()

        print("\n2. Seasonal Heatmap:")
        self.create_seasonal_heatmap()

        print("\n3. Sector Pie Chart:")
        self.create_sector_pie_chart()

        print("\n4. Daily Load Profile:")
        self.create_daily_load_profile()

        print("\n5. Infrastructure Dashboard:")
        self.create_infrastructure_dashboard()

        print("\n✅ Comprehensive analysis completed!")
        print("✅ All visualizations generated successfully!")

def main():
    """Main function to run the analytics program"""
    try:
        # Create analytics instance
        analytics = ChennaiElectricityAnalytics()

        # Run comprehensive analysis
        analytics.generate_comprehensive_report()

    except Exception as e:
        print(f"❌ Error in main execution: {str(e)}")
        print("Please ensure all CSV files are in the same directory as this script.")

if __name__ == "__main__":
    # Install required packages if not available
    try:
        import plotly
    except ImportError:
        print("Installing required packages...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])

    # Run the main program
    main()
