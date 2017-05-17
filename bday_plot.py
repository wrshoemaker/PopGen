from __future__ import division
import pandas as pd
import os, math
import  matplotlib.pyplot as plt

mydir = os.path.expanduser("~/Desktop")


dates = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
datesStr = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']

values = [19, 28, 38, 60, 45, 29, 27, 24]
fig = plt.figure()
plt.scatter(dates,values)
plt.plot(dates, values)
plt.xticks(dates, datesStr, rotation='horizontal')
plt.ylabel('Number of wall posts')
plt.xlabel('Year')

plt.title('Birthday messages on Facebook over time')
fig.savefig(mydir + '/bday.png', bbox_inches='tight',  dpi = 600)
plt.close()
