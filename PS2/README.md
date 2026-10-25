Solar Radiation Analysis

Project Overview

This project explores a solar radiation dataset using Python. It analyses solar radiation over time and investigates its relationships with temperature, humidity, atmospheric pressure, and wind speed.

Objectives

- Explore and understand the dataset.
- Visualise solar radiation over time.
- Investigate relationships between solar radiation and weather variables.
- Calculate and visualise correlations between numerical variables.

Tools and Libraries

- Python
- Pandas
- Matplotlib
- Seaborn

Dataset

The dataset contains observations of solar radiation and associated weather measurements, including temperature, pressure, humidity, wind direction, wind speed, and timestamps.

Visualisations

1. Solar Radiation Over Time
2. Temperature vs Solar Radiation
3. Humidity vs Solar Radiation
4. Correlation Heatmap

Key Findings

- Temperature has a positive correlation with solar radiation (approximately 0.735).
- Humidity has a negative correlation with solar radiation (approximately -0.226).
- Atmospheric pressure has a weak positive correlation with solar radiation (approximately 0.119).
- Wind speed has a very weak positive correlation with solar radiation (approximately 0.074).

These are correlations observed in this dataset and do not establish causation.

How to Run

1. Install Python.
2. Install the required libraries:
   "pip install pandas matplotlib seaborn"
3. Place the dataset CSV file in the project folder.
4. Run:
   "python solar_analysis.py"

Limitations

The analysis identifies patterns and correlations but does not establish causal relationships or provide a validated predictive model.

Dataset Access

The dataset used for this analysis is not included in this repository because redistribution is restricted.

To run the project, obtain the dataset through its authorised source, subject to the applicable access and usage terms. Place the permitted CSV file in the project folder and run "solar_analysis.py".

The visualisations and findings included in this repository were generated from the dataset used during development.

Solar Radiation Prediction

A Random Forest Regressor was trained to estimate solar radiation using five weather features:

- Temperature
- Pressure
- Humidity
- Wind direction
- Wind speed

Evaluation Results

- Mean Absolute Error (MAE): 90.05
- R² Score: 0.743

The model explains approximately 74.3% of the variation in solar radiation on the test set. The MAE represents the average absolute difference between predicted and actual radiation measurements.

The model estimates radiation from supplied weather measurements; it does not forecast future radiation from future weather conditions.

Limitations

Performance may vary across weather conditions and datasets. Further testing and feature engineering could improve the model.
