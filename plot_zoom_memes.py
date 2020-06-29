import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas import read_csv
import pandas as pd

fn = lambda x : x.split(" ")[1]
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
day_names = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
time_cutoffs = [0, 12]
like_cutoff = 3000
# zoommemes,Muzzammil Shaikh,1592554543,2020-06-19 08:15:43 PDT-0700,08:15:43,One solution,,796

def months_to_days(months):
	ans = 0
	for i in range(months-1):
		ans += days[i]
	return ans

def date_to_day_of_week(date):
	return ((months_to_days(int(date.split("-")[1])) + int(date.split("-")[2]) + 3)  %7)

def format_time(t):
	if(t >= 12 and t < 24):
		return "{}pm".format((t-1)%12 + 1)
	else:
		return "{}am".format((t-1)%12 + 1)

def plot_dots(dates, likes)
	plt.scatter(dates, likes, c="blue", s=1)
	plt.title("Page likes on Zoom Memes")
	plt.ylabel("Page likes")
	plt.xlabel("Time (As DD:HHMMSS, scaled seconds)")
	plt.grid(True)
	plt.show()

def plot_bars(xlabels, data_labels, *data):
	x = np.arange(len(xlabels))  # the label locations
	width = 0.35  # the width of the bars
	space_avail = 0.8
	width = space_avail / len(data)
	offset = width * len(data) / 2

	fig, ax = plt.subplots()
	rects = [ax.bar(x - offset + i * width, arg, width, label=data_labels[i]) for i, arg in enumerate(data)] 

	# Add some text for xlabels, title and custom x-axis tick xlabels, etc.
	ax.set_ylabel('# of posts with likes in range')
	ax.set_title('Like ranges by day (July 11-26) (' + format_time(time_cutoffs[0]) + "-" + format_time(time_cutoffs[1]) + ')')
	ax.set_xticks(x)
	ax.set_xticklabels(xlabels)
	ax.legend()

	def autolabel(rects):
	    """Attach a text label above each bar in *rects*, displaying its height."""
	    for rect in rects:
	        height = rect.get_height()
	        ax.annotate('{}'.format(height),
	                    xy=(rect.get_x() + rect.get_width() / 2, height),
	                    xytext=(0, 3),  # 3 points vertical offset
	                    textcoords="offset points",
	                    ha='center', va='bottom')

	for rect in rects:
		autolabel(rect)

	fig.tight_layout()

	plt.show()

times = []
likes = []
dates = []

# Group,Author,uTime,Normal Time,HH:MM:SS,Text,Permalink,Likes
header = 0
day_8pm_proportions = [[0 for _ in range(7)], [0 for _ in range(7)]]
with open("posts.csv", 'r', encoding='utf8') as f:
	for line in f:
		if(not header):
			header += 1
			continue
		date = line.split(",")[3].split(" ")[0].strip()
		time = line.split(",")[4].strip()
		like = line.split(",")[-1].strip()
		time_val = (int(time.split(":")[0]) * 100.0 * 100 + 
			int(time.split(":")[1]) * 100.0 * 100 / 60 + 
			int(time.split(":")[2]) * 100.0 * 100 / (60 * 60))
		times.append(time_val)
		print(time_val)
		if(time_val >= time_cutoffs[0] * 10000 and time_val <= time_cutoffs[1] * 10000):
			like_in_range = int(int(like) >= like_cutoff)
			day_of = date_to_day_of_week(date)
			day_8pm_proportions[like_in_range][day_of] += 1

		print(date, date_to_day_of_week(date))
		dates.append(times[-1] + 1000000 * date_to_day_of_week(date))
		likes.append(int(like))
		if(likes[-1] > 4000):
			print(line.split(",")[-2])
print(likes[-1])
print(day_8pm_proportions)

if __name__ == "__main__":
	plot_bars(day_names, ["< " + str(like_cutoff), "> " + str(like_cutoff)], day_8pm_proportions[0], day_8pm_proportions[1])
	# plot_dots(days, likes)