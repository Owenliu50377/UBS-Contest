# UBS-Contest

UBS-Contest-Financial Engineering (Risk Prediction for Range Accural Note)

## Brief Overview

There exist four different datasets in CSV form namely swap-rates, market volatilities, trade information and the vegas.
Our envision goal is to train a generalized model to predict the value of the Vegas, which is in the Vegas CSV file. The models can be splitted into different types including Generative models such as Fourier Series, the traditional machine learning model like XGboosting and random forest, the deep learning model such as LSTM which performs pretty well on the dataset.

## Notes

To reimplement the work:
+ Import the data into the data folder (4 CSV files)
+ Run the Data-Preprocessing file to form the Final_dataset.csv
+ Perform all the models on the Final_dataset.csv

# Reference docs

https://user42.tuxfamily.org/chart/manual/Exponential-Moving-Average.html