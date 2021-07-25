import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
warnings.filterwarnings('ignore')

# load data
data_file_path = '/home/gerardo/Documents/Trading/Data/OriginalData/SPY.csv'
df = pd.read_csv(data_file_path)

# set index to be date

df = df.set_index(pd.DatetimeIndex(df['Date'].values))

##Show chart
#plt.figure(figsize=(12.2, 4.5))
#plt.plot(df['Close'], label='Close Price')
#plt.title('SPY Close Price')
#plt.xlabel('Date')
#plt.ylabel('Close Price USD')
#plt.legend(df.columns.values, loc='upper left')
#plt.show()

# Calculate typical price
typical_price = (df['Close'] +df['High'] + df['Low'])/3

# Get the period. Typically 14 days
period = 20

# Calculate money flow
money_flow = typical_price * df['Volume']

# Get all positive and negative money flows

positive_flow = []
negative_flow = []

#loop through typical price
for i in range(1, len(typical_price)):
    if typical_price[i] > typical_price[i-1]:
        positive_flow.append(money_flow[i-1])
        negative_flow.append(0)
    elif typical_price[i] < typical_price[i-1]:
        negative_flow.append(money_flow[i-1])
        positive_flow.append(0)
    else:
        positive_flow.append(0)
        negative_flow.append(0)

# Get all positive and negative money flows within the time period
positive_mf = []
negative_mf = []

for i in range(period-1, len(positive_flow)):
    positive_mf.append(sum(positive_flow[i+1-period:i+1]))

for i in range(period-1, len(negative_flow)):
    negative_mf.append(sum(negative_flow[i+1-period:i+1]))

# Calculate the money flow index
mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf)+np.array(negative_mf)))

# visualize show mfi

df2 = pd.DataFrame()
df2['MFI'] = mfi

##create the plot
#plt.figure(figsize=(12.2, 4.5))
#plt.plot(df2['MFI'], label='MFI')
#plt.title('MFI')
#plt.ylabel('MFI Values')
#plt.axhline(10, linestyle='--', color='orange')
#plt.axhline(20, linestyle='--', color='blue')
#plt.axhline(80, linestyle='--', color='blue')
#plt.axhline(90, linestyle='--', color='orange')
#plt.show()

# Create a new DF
new_df = pd.DataFrame()
new_df = df[period:]
new_df['MFI'] = mfi

# Show new data frame
print(new_df)

# Create a function to get the buy and sell signals
def get_signal(data, high, low):
    buy_signal = []
    sell_signal = []
    for i in range(len(data['MFI'])):
        if data['MFI'][i] > high:
            buy_signal.append(np.nan)
            sell_signal.append(data['Close'][i])
        elif data['MFI'][i] < low:
            buy_signal.append(data['Close'][i])
            sell_signal.append(np.nan)
        else:
            sell_signal.append(np.nan)
            buy_signal.append(np.nan)
    return(buy_signal, sell_signal)

# add new cols to df (buy and sell)
new_df['Buy'] = get_signal(new_df, 80, 20)[0]
new_df['Sell'] = get_signal(new_df, 80, 20)[1]

# plot the data
plt.figure(figsize=(12.2, 4.5))
plt.plot(new_df['Close'], label='Close Price', alpha=0.5)
plt.scatter(new_df.index, new_df['Buy'],
            color='green', label='Buy Signal', marker='^', alpha=1)
plt.scatter(new_df.index, new_df['Sell'],
            color='red', label='Sell Signal', marker='v', alpha=1)
plt.title('SPY Close Price')
plt.xlabel('Date')
plt.ylabel('Close Price USD')
plt.legend(new_df.columns.values, loc='upper left')
plt.show()
