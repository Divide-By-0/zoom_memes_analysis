import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas import read_csv
import pandas as pd

fn = lambda x : x.split(" ")[1]
#
# zoommemes,Muzzammil Shaikh,1592554543,2020-06-19 08:15:43 PDT-0700,08:15:43,One solution,,796

times = []
likes = []
dates = []
# Group,Author,uTime,Normal Time,HH:MM:SS,Text,Permalink,Likes
header = 0
with open("posts.csv", 'r', encoding='utf8') as f:
	for line in f:
		if(not header):
			header += 1
			continue
		date = line.split(",")[3].split(" ")[0].strip()
		time = line.split(",")[4].strip()
		like = line.split(",")[-1].strip()
		times.append(int(time.split(":")[0]) * 100.0 * 100 + 
			int(time.split(":")[1]) * 100.0 * 100 / 60 + 
			int(time.split(":")[2]) * 100.0 * 100 / (60 * 60))
		dates.append(times[-1] + 1000000 * int(date.split("-")[2]))
		likes.append(int(like))
		if(likes[-1] > 4000):
			print(line.split(",")[-2])
		# print(time)
print(likes[-1])
# csv = read_csv("posts.csv", header = 0, parse_dates=[3])
	
# # Set it to None to display all columns in the dataframe
# pd.set_option('display.max_columns', None)
# # csv = csv.apply(lambda x: x.split(" ")[1] if x.name == 'Likes' else x)
# print(csv.head(2))
# # group, name, utime, times, post, link, likes = np.loadtxt("posts.csv", unpack=True,
# # 	dtype={'names': ("Group","Author","uTime","Reg Time","Text","Permalink","Likes"),
# # 	 'formats': ('S1', 'S1', 'S1', 'S1', 'S1', 'S1', 'S1')})

# times = []

# for i, time in enumerate(times):
# 	times[i] = fn(time)
# 	print(time, times[i])
# 	print(likes[i])

plt.plot(times, likes, "bo")
plt.title("Page likes on SAD")
plt.ylabel("Page likes")
plt.xlabel("Time (As HHMMSS, scaled)")
plt.grid(True)
plt.show()