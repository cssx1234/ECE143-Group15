# F1 Driver Performance vs. Weather Conditions Data Analysis

## Introduction

This analysis investigates the impact of weather conditions on the performance of Formula 1 drivers. The hypothesis suggests that varying weather conditions may influence driver performance. The correlation between weather parameters (air temperature, air pressure, humidity, and windspeed) and the number of points earned by drivers was examined.

## Methods

### Data Collection
Data from the 2018-2022 F1 seasons was collected using the FastF1 API. Correlation and histogram plots were generated to visualize potential relationships.

### Data Cleaning
1. **Handling Missing Values:** Rows with missing values were dropped.
2. **Filtering Outliers:** Rows with points exceeding 26 were removed.
3. **Rounding Numeric Values:** Numeric columns were rounded for clarity.
4. **Validating Points Values:** Rows with points not in the allowed range were excluded.
5. **Saving Cleaned Data:** The final dataset was saved as 'cleaned_f1_merged_data.csv.'

## Findings

Contrary to the initial hypothesis, there was little to no significant correlation between weather variables and driver performance. Possible explanations include driver adaptability, advanced technology, and strategic decision-making.

### Possible Explanations

1. **Driver Adaptability:**
   - Skill and Expertise: Drivers quickly adapt to changing conditions.
   - Heat Endurance Training: Drivers train for high cockpit temperatures.

2. **Advanced Technology:**
   - Aerodynamics and Handling: F1 cars feature advanced technologies for optimal performance.
   - Cooling: Various technologies combat high cockpit temperatures.

3. **Strategic Decision-Making:**
   - Tire Selection Strategies: Teams optimize grip based on anticipated conditions.
   - Pit Stop Timing: Weather forecasts influence pit stop decisions.
   - Risk Management: Teams balance performance and risk.

4. **Equal Exposure:**
   - Level Playing Field: All drivers experience the same conditions.
   - Competitive Environment: Driver skill and team strategies play vital roles.

## Conclusion

The complexity of Formula 1 dynamics, including driver skill, technology, and strategic decision-making, seemed to overshadow the influence of weather on race outcomes. Further research, considering specific tracks or exceptional weather events, could provide additional insights.

## Limitations and Future Research

This analysis provides a broad overview and does not explore microclimates or specific events. Future research could delve deeper into these factors for a more nuanced understanding.

## Data Analysis Scripts

In the "data gathering script" folder, find the 'f1_weather_data_analysis.py' script for data collection. The "plots scripts" folder contains scripts to generate correlation and histogram plots.

## Dataset Statistics

- **Maximum Values:**
  - AirTemp: 36.60°C
  - WindSpeed: 5.49 knots
  - Humidity: 96.00%
  - Pressure: 1023.13 mbar

- **Minimum Values:**
  - AirTemp: 13.00°C
  - WindSpeed: 0.28 knots
  - Humidity: 7.00%
  - Pressure: 780.51 mbar

- **Average Values:**
  - AirTemp: 24.13°C
  - WindSpeed: 1.69 knots
  - Humidity: 50.73%
  - Pressure: 991.11 mbar

- **Number of Rows/Races:** 4109

- **F1 Cockpit Temperatures:** Up to 60°C (140°F)

*Note: The 'f1_weather_data_analysis.py' script requires an internet connection for FastF1 / Ergast's online datasets.*

---

*Author: Glenn Sivila*