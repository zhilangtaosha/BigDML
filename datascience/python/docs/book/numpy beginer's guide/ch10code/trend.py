from matplotlib.finance import quotes_historical_yahoo
from datetime import date
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter
from matplotlib.dates import DayLocator
from matplotlib.dates import MonthLocator


'''
today = date.today()
start = (today.year - 1, today.month, today.day)
quotes = quotes_historical_yahoo("QQQ", start, today)
quotes = np.array(quotes)
dates = quotes.T[0]
qqq = quotes.T[4]
'''

dates=np.array(['Jan 2016','Feb 2016','Mar 2016','Jan 2017','Feb 2017','Sat 2017'])
qqq=np.array([20,30,50,23,60,54])

y = signal.detrend(qqq)

alldays = DayLocator()              
months = MonthLocator()
month_formatter = DateFormatter("%b %Y")

fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(dates, qqq, 'o', dates, qqq - y, '-')
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(month_formatter)
fig.autofmt_xdate()
plt.show()
