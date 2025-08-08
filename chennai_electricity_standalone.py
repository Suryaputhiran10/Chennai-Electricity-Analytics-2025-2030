
"""
Chennai Electricity Analytics - Standalone Execution Program
===========================================================
Complete analytics with data generation and visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')

class ChennaiElectricityStandalone:
    def __init__(self):
        self.data = {}
        print("Chennai Electricity Analytics - Standalone Version")
        print("=" * 55)

    def generate_and_analyze_data(self):
        """Generate data and perform complete analysis"""

        # 1. Generate projection data
        years = list(range(2025, 2031))
        projections = []

        base_demand = 21361
        base_cost = 4.80
        demand_cagr = 0.0414
        cost_cagr = 0.035

        for year in years:
            years_from_base = year - 2025
            demand = base_demand * ((1 + demand_cagr) ** years_from_base)
            cost = base_cost * ((1 + cost_cagr) ** years_from_base)

            projections.append({
                'Year': year,
                'Demand_MU': round(demand, 2),
                'Cost_Rs_per_unit': round(cost, 2),
                'Market_Value_Cr': round(demand * cost * 10, 2),
                'Peak_MW': round(demand * 1000 / (365 * 24 * 0.75), 2)
            })

        self.data['projections'] = pd.DataFrame(projections)

        # 2. Generate sector-wise data
        sectors = ['Domestic', 'Commercial', 'Industrial', 'Agriculture', 'Others']
        sector_shares = [0.35, 0.25, 0.30, 0.05, 0.05]
        sector_data = []

        for year in years:
            total_demand = self.data['projections'][self.data['projections']['Year'] == year]['Demand_MU'].iloc[0]
            for i, sector in enumerate(sectors):
                sector_data.append({
                    'Year': year,
                    'Sector': sector,
                    'Demand_MU': round(total_demand * sector_shares[i], 2),
                    'Share_%': round(sector_shares[i] * 100, 1)
                })

        self.data['sector'] = pd.DataFrame(sector_data)

        # 3. Generate monthly pattern data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        seasonal_factors = [0.85, 0.82, 0.95, 1.15, 1.25, 1.20, 1.10, 1.05, 1.00, 0.95, 0.88, 0.90]

        monthly_data = []
        annual_demand = 21361  # 2025 base

        for i, month in enumerate(months):
            monthly_demand = (annual_demand / 12) * seasonal_factors[i]
            monthly_data.append({
                'Month': month,
                'Month_Num': i + 1,
                'Demand_MU': round(monthly_demand, 2),
                'Seasonal_Factor': seasonal_factors[i]
            })

        self.data['monthly'] = pd.DataFrame(monthly_data)

        # 4. Generate scenario data
        scenarios = {
            'Conservative': {'demand': 25370, 'cost': 5.43},
            'Base Case': {'demand': 26164, 'cost': 5.70},
            'Aggressive': {'demand': 27263, 'cost': 5.98}
        }

        scenario_data = []
        for scenario, values in scenarios.items():
            scenario_data.append({
                'Scenario': scenario,
                'Demand_MU_2030': values['demand'],
                'Cost_Rs_per_unit_2030': values['cost']
            })

        self.data['scenarios'] = pd.DataFrame(scenario_data)

        print("✅ Data generation completed successfully!")

    def create_comprehensive_visualizations(self):
        """Create all visualizations"""

        # Set up the plotting area
        fig = plt.figure(figsize=(20, 24))

        # 1. Demand and Cost Projection (Top Left)
        ax1 = plt.subplot(3, 3, 1)
        df_proj = self.data['projections']

        bars = ax1.bar(df_proj['Year'], df_proj['Demand_MU'], alpha=0.7, color='skyblue', label='Demand (MU)')
        ax1.set_ylabel('Demand (Million Units)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Add value labels
        for bar, value in zip(bars, df_proj['Demand_MU']):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 50,
                    f'{value:,.0f}', ha='center', va='bottom', fontsize=9)

        ax1_twin = ax1.twinx()
        line = ax1_twin.plot(df_proj['Year'], df_proj['Cost_Rs_per_unit'], 'ro-', label='Cost (Rs/unit)')
        ax1_twin.set_ylabel('Cost (Rs per unit)', color='red')
        ax1_twin.tick_params(axis='y', labelcolor='red')

        ax1.set_title('Chennai Electricity: Demand vs Cost (2025-2030)', fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # 2. Sector-wise Pie Chart (Top Center)
        ax2 = plt.subplot(3, 3, 2)
        df_sector_2025 = self.data['sector'][self.data['sector']['Year'] == 2025]
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']

        wedges, texts, autotexts = ax2.pie(df_sector_2025['Demand_MU'], 
                                          labels=df_sector_2025['Sector'],
                                          colors=colors,
                                          autopct='%1.1f%%',
                                          startangle=90)
        ax2.set_title('Sector-wise Consumption (2025)', fontweight='bold')

        # 3. Monthly Seasonal Pattern (Top Right)
        ax3 = plt.subplot(3, 3, 3)
        df_monthly = self.data['monthly']

        bars = ax3.bar(df_monthly['Month'], df_monthly['Demand_MU'], 
                      color=['lightcoral' if x > 2000 else 'lightblue' for x in df_monthly['Demand_MU']])
        ax3.set_title('Monthly Demand Pattern (2025)', fontweight='bold')
        ax3.set_ylabel('Demand (MU)')
        plt.setp(ax3.get_xticklabels(), rotation=45)

        # Add value labels
        for bar, value in zip(bars, df_monthly['Demand_MU']):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 20,
                    f'{value:.0f}', ha='center', va='bottom', fontsize=8)

        # 4. Market Value Growth (Middle Left)
        ax4 = plt.subplot(3, 3, 4)
        ax4.plot(df_proj['Year'], df_proj['Market_Value_Cr'], marker='o', linewidth=3, markersize=8, color='green')
        ax4.fill_between(df_proj['Year'], df_proj['Market_Value_Cr'], alpha=0.3, color='green')
        ax4.set_title('Market Value Growth', fontweight='bold')
        ax4.set_ylabel('Market Value (Crores)')
        ax4.grid(True, alpha=0.3)

        # Add value labels
        for x, y in zip(df_proj['Year'], df_proj['Market_Value_Cr']):
            ax4.annotate(f'₹{y:,.0f}', (x, y), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontsize=9)

        # 5. Peak Demand Projection (Middle Center)
        ax5 = plt.subplot(3, 3, 5)
        ax5.bar(df_proj['Year'], df_proj['Peak_MW'], color='orange', alpha=0.7)
        ax5.set_title('Peak Demand Growth', fontweight='bold')
        ax5.set_ylabel('Peak Demand (MW)')
        ax5.grid(True, alpha=0.3)

        # Add value labels
        for i, (year, peak) in enumerate(zip(df_proj['Year'], df_proj['Peak_MW'])):
            ax5.text(i, peak + 30, f'{peak:.0f}', ha='center', va='bottom', fontsize=9)

        # 6. Scenario Analysis (Middle Right)
        ax6 = plt.subplot(3, 3, 6)
        df_scenarios = self.data['scenarios']

        x_pos = range(len(df_scenarios))
        bars = ax6.bar(x_pos, df_scenarios['Demand_MU_2030'], alpha=0.7, 
                      color=['lightgreen', 'skyblue', 'lightcoral'])
        ax6.set_ylabel('2030 Demand (MU)', color='blue')
        ax6.set_xticks(x_pos)
        ax6.set_xticklabels(df_scenarios['Scenario'])
        ax6.tick_params(axis='y', labelcolor='blue')

        # Add cost line
        ax6_twin = ax6.twinx()
        ax6_twin.plot(x_pos, df_scenarios['Cost_Rs_per_unit_2030'], 'ro-', markersize=8, linewidth=2)
        ax6_twin.set_ylabel('2030 Cost (Rs/unit)', color='red')
        ax6_twin.tick_params(axis='y', labelcolor='red')

        ax6.set_title('2030 Scenario Analysis', fontweight='bold')

        # Add value labels
        for i, (demand, cost) in enumerate(zip(df_scenarios['Demand_MU_2030'], df_scenarios['Cost_Rs_per_unit_2030'])):
            ax6.text(i, demand + 200, f'{demand:,}', ha='center', va='bottom', fontsize=9)
            ax6_twin.text(i, cost + 0.05, f'₹{cost:.2f}', ha='center', va='bottom', fontsize=9)

        # 7. Demand Growth Trend (Bottom Left)
        ax7 = plt.subplot(3, 3, 7)
        growth_rates = df_proj['Demand_MU'].pct_change() * 100
        growth_rates = growth_rates.dropna()

        ax7.bar(df_proj['Year'].iloc[1:], growth_rates, color='purple', alpha=0.7)
        ax7.axhline(y=4.14, color='red', linestyle='--', label='Target CAGR (4.14%)')
        ax7.set_title('Year-over-Year Demand Growth', fontweight='bold')
        ax7.set_ylabel('Growth Rate (%)')
        ax7.legend()
        ax7.grid(True, alpha=0.3)

        # 8. Cost Inflation Trend (Bottom Center)
        ax8 = plt.subplot(3, 3, 8)
        cost_growth_rates = df_proj['Cost_Rs_per_unit'].pct_change() * 100
        cost_growth_rates = cost_growth_rates.dropna()

        ax8.bar(df_proj['Year'].iloc[1:], cost_growth_rates, color='brown', alpha=0.7)
        ax8.axhline(y=3.5, color='red', linestyle='--', label='Target CAGR (3.5%)')
        ax8.set_title('Year-over-Year Cost Inflation', fontweight='bold')
        ax8.set_ylabel('Inflation Rate (%)')
        ax8.legend()
        ax8.grid(True, alpha=0.3)

        # 9. Cumulative Growth Index (Bottom Right)
        ax9 = plt.subplot(3, 3, 9)

        demand_index = df_proj['Demand_MU'] / df_proj['Demand_MU'].iloc[0] * 100
        cost_index = df_proj['Cost_Rs_per_unit'] / df_proj['Cost_Rs_per_unit'].iloc[0] * 100

        ax9.plot(df_proj['Year'], demand_index, marker='o', label='Demand Index', linewidth=2)
        ax9.plot(df_proj['Year'], cost_index, marker='s', label='Cost Index', linewidth=2)
        ax9.axhline(y=100, color='gray', linestyle=':', alpha=0.5)

        ax9.set_title('Cumulative Growth Index (2025=100)', fontweight='bold')
        ax9.set_ylabel('Index (2025=100)')
        ax9.legend()
        ax9.grid(True, alpha=0.3)

        plt.suptitle('Chennai Electricity Demand & Cost Analytics Dashboard (2025-2030)', 
                     fontsize=20, fontweight='bold', y=0.98)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

    def display_key_metrics(self):
        """Display key performance indicators"""
        print("\n" + "=" * 60)
        print("KEY PERFORMANCE INDICATORS")
        print("=" * 60)

        df_proj = self.data['projections']

        # Calculate metrics
        total_demand_growth = ((df_proj['Demand_MU'].iloc[-1] / df_proj['Demand_MU'].iloc[0]) - 1) * 100
        total_cost_increase = ((df_proj['Cost_Rs_per_unit'].iloc[-1] / df_proj['Cost_Rs_per_unit'].iloc[0]) - 1) * 100
        market_value_cagr = ((df_proj['Market_Value_Cr'].iloc[-1] / df_proj['Market_Value_Cr'].iloc[0]) ** (1/5) - 1) * 100

        print(f"📊 Total Demand Growth (2025-2030): {total_demand_growth:.2f}%")
        print(f"📊 Total Cost Increase (2025-2030): {total_cost_increase:.2f}%")
        print(f"📊 Market Value CAGR: {market_value_cagr:.2f}%")
        print(f"📊 2025 Market Value: ₹{df_proj['Market_Value_Cr'].iloc[0]:,.0f} Crores")
        print(f"📊 2030 Market Value: ₹{df_proj['Market_Value_Cr'].iloc[-1]:,.0f} Crores")
        print(f"📊 Peak Demand Growth: {df_proj['Peak_MW'].iloc[-1] - df_proj['Peak_MW'].iloc[0]:.0f} MW")

        # Seasonal insights
        df_monthly = self.data['monthly']
        peak_month = df_monthly.loc[df_monthly['Demand_MU'].idxmax()]
        low_month = df_monthly.loc[df_monthly['Demand_MU'].idxmin()]

        print(f"📊 Peak Demand Month: {peak_month['Month']} ({peak_month['Demand_MU']:.0f} MU)")
        print(f"📊 Low Demand Month: {low_month['Month']} ({low_month['Demand_MU']:.0f} MU)")
        print(f"📊 Seasonal Variation: {((peak_month['Demand_MU'] / low_month['Demand_MU']) - 1) * 100:.1f}%")

        # Sector insights
        df_sector = self.data['sector']
        df_sector_2025 = df_sector[df_sector['Year'] == 2025]
        top_sector = df_sector_2025.loc[df_sector_2025['Demand_MU'].idxmax()]

        print(f"📊 Largest Consumer Sector: {top_sector['Sector']} ({top_sector['Share_%']:.1f}%)")

    def save_data_to_csv(self):
        """Save all generated data to CSV files"""
        print("\n" + "=" * 60)
        print("SAVING DATA TO CSV FILES")
        print("=" * 60)

        # Save all datasets
        self.data['projections'].to_csv('generated_projections.csv', index=False)
        self.data['sector'].to_csv('generated_sector_data.csv', index=False)
        self.data['monthly'].to_csv('generated_monthly_data.csv', index=False)
        self.data['scenarios'].to_csv('generated_scenarios.csv', index=False)

        print("✅ generated_projections.csv")
        print("✅ generated_sector_data.csv")
        print("✅ generated_monthly_data.csv")
        print("✅ generated_scenarios.csv")

    def run_complete_analysis(self):
        """Run the complete analysis workflow"""
        try:
            print("🚀 Starting Chennai Electricity Analytics...")

            # Step 1: Generate data
            print("\n📊 Step 1: Generating analytical data...")
            self.generate_and_analyze_data()

            # Step 2: Display metrics
            print("\n📊 Step 2: Calculating key metrics...")
            self.display_key_metrics()

            # Step 3: Create visualizations
            print("\n📊 Step 3: Creating comprehensive visualizations...")
            self.create_comprehensive_visualizations()

            # Step 4: Save data
            print("\n📊 Step 4: Saving data for future analysis...")
            self.save_data_to_csv()

            print("\n" + "=" * 60)
            print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
            print("✅ All visualizations have been generated!")
            print("✅ CSV files saved for future reference!")
            print("=" * 60)

        except Exception as e:
            print(f"❌ Error during analysis: {str(e)}")

# Execute the analysis
if __name__ == "__main__":
    analyzer = ChennaiElectricityStandalone()
    analyzer.run_complete_analysis()
