""" Trying someshit"""

import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 10, 6
PATH = 'C:/Users/ludoz/Downloads/predict-energy-behavior-of-prosumers/'

train=pd.read_csv(PATH+'train.csv')
client=pd.read_csv(PATH+'client.csv')
gas=pd.read_csv(PATH+'gas_prices.csv')
electricity=pd.read_csv(PATH+'electricity_prices.csv')
forecast_w=pd.read_csv(PATH+'forecast_weather.csv')
hist_w=pd.read_csv(PATH+'historical_weather.csv')
w_s_c=pd.read_csv(PATH+'weather_station_to_county_mapping.csv')

# filling out missing values
train['target'] = train['target'].interpolate(method='linear')
# dummies for the categorical variables in train
train_encoded = pd.get_dummies(train, columns=['county', 'product_type'])

# Convert 'datetime' columns to pandas datetime objects where applicable
train['datetime'] = pd.to_datetime(train['datetime'])
client['date'] = pd.to_datetime(client['date'])
gas['origin_date'] = pd.to_datetime(gas['origin_date'])
gas['forecast_date'] = pd.to_datetime(gas['forecast_date'])
electricity['origin_date'] = pd.to_datetime(electricity['origin_date'])
electricity['forecast_date'] = pd.to_datetime(electricity['forecast_date'])
forecast_w['origin_datetime'] = pd.to_datetime(forecast_w['origin_datetime'])
forecast_w['forecast_datetime'] = pd.to_datetime(forecast_w['forecast_datetime'])
hist_w['datetime'] = pd.to_datetime(hist_w['datetime'])

# Set the 'datetime' column as the index for the relevant DataFrames
train = train.set_index('datetime').sort_index()
hist_w = hist_w.set_index('datetime').sort_index()

# Let's visualize the target variable over time quickly
train['target'].plot(title='Target Variable Over Time')
result = adfuller(train['target'][:100000], autolag='AIC')
dfoutput = pd.Series(result[0:4], index=['Test Statistic','p-value',
                                         '#Lags Used','Number of Observations Used'])
for key,value in result[4].items():
    dfoutput['Critical Value (%s)'%key] = value
print(dfoutput)

print(f'ADF Statistic: {result[0]}')
print(f'p-value: {result[1]}')
if result[1] <= 0.05:
    print("The series is stationary.")
else:
    print("The series is not stationary.")

# Decompose the series to observe trend and seasonality
decomposition = seasonal_decompose(train['target'][:100000].dropna(),
                                   model='additive', period=24)
# assuming hourly data has a daily seasonality
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Plotting the decomposed components of the time series
plt.figure(figsize=(12,8))
plt.subplot(411)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()


# applying ACF and PACF
acf_result = acf(train['target'], nlags=72)
pacf_result = pacf(train['target'], nlags=72)
# ACF and PACF plots
plt.figure(figsize=(15, 5))
plt.subplot(121)
plt.plot(acf_result)
plt.xticks(np.arange(0, 71, 1))

plt.subplot(122)
plt.plot(pacf_result)
plt.xticks(np.arange(0, 71, 1))
plt.title('Partial Autocorrelation Function')
plt.tight_layout()
plt.show()

#Determine rolling statistics
rolmean = train['target'].rolling(window=201835).mean()
rolstd = train['target'].rolling(window=201835).std()

#Plot rolling statistics
orig = plt.plot(train['target'], color='blue', label='Original')
mean = plt.plot(rolmean, color='red', label='Rolling Mean')
plt.show(block=False)

# AR model
model = ARIMA(train['target'][:100000], order=(1,0,0))
results_AR = model.fit()
plt.plot(train['target'][:100000])
plt.plot(results_AR.fittedvalues, color='red')
plt.title(f'RSS: {sum((results_AR.fittedvalues - train["target"][:100000])**2):.4f}')
print('Plotting AR model')

# MA model
model = ARIMA(train['target'][:100000], order=(0,0,1))
results_MA = model.fit()
plt.plot(train['target'][:100000])
plt.plot(results_MA.fittedvalues, color='red')
plt.title(f'RSS: {sum((results_MA.fittedvalues - train["target"][:100000])**2):.4f}')
print('Plotting MA model')
