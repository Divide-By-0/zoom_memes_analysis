# Like-Plotter based on FaceBook-Scraper [2020]

Updated for June 2020 changes by Divide-By-0, along with plots added.

_Scrape posts from any group or user into a .csv file without needing to register for any API access_

---

### How to use it?

Firstly, make sure you have selenium >= 3.141.0, GeckoDriver and FireFox installed.

Store your email and password for Facebook login in credentials.txt. Make sure to login and set your preferences for the old UI.

Use `scraper.py` to collect the data.

```
usage: scrape.py [-h] [--pages PAGES [PAGES ...]] [--groups GROUPS [GROUPS ...]][-d DEPTH]
Data Collection
arguments:
  -h, --help            show this help message and exit
  -p, --pages PAGES [PAGES ...]
                        List the pages you want to scrape
                        for recent posts

  -g, --groups GROUPS [GROUPS ...]
                        List the groups you want to scrape
                        for recent posts

  -d DEPTH, --depth DEPTH
                        How many recent posts you want to gather in
                        multiples of (roughly) 8.
```

Example: `python scraper.py --pages feelzesty -d 20`

---

The output is `posts.csv` inside the script folder.

Output is columns: Group,Author,uTime,Normal Time,HH:MM:SS,Preview Text,See More Permalink,Likes

Can then run `python plot_zoom_memes.py` to plot the data by like count by day/time. Change the parameters defined at the top of the python file to change the like cutoff or date range. Note the days of the week are only accurate for 2020. Scatter plots are shown with DD:HH:MM:SS so only hours 0-24 out of 100 are shown in the plot.
