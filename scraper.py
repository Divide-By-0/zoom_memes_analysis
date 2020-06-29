from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pytz import timezone
import datetime
import sys
import time
import argparse
import csv
import calendar

parser = argparse.ArgumentParser(description='Non API public FB miner')

parser.add_argument('-p', '--pages', nargs='+',
                    dest="pages",
                    help="List the pages you want to scrape for recent posts")

parser.add_argument("-g", '--groups', nargs='+',
                    dest="groups",
                    help="List the groups you want to scrape for recent posts")

parser.add_argument("-d", "--depth", action="store",
                    dest="depth", default=5, type=int,
                    help="How many recent posts you want to gather -- in multiples of (roughly) 8.")

args = parser.parse_args()

BROWSER_EXE = '/usr/bin/firefox'
GECKODRIVER = '/usr/local/bin/geckodriver'
GECKODRIVER = 'C:\\Users\\AayushGupta\\Downloads\\geckodriver-v0.26.0-win64\\geckodriver.exe'
BROWSER_EXE = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'

FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)

#  Code to disable notifications pop up of Chrome Browser

PROFILE = webdriver.FirefoxProfile()
# PROFILE.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = False
PROFILE.set_preference("dom.webnotifications.enabled", False)
PROFILE.set_preference("app.update.enabled", False)
PROFILE.update_preferences()

fmt = "%Y-%m-%d %H:%M:%S %Z%z"

class CollectPosts(object):
    """Collector of recent FaceBook posts.
           Note: We bypass the FaceBook-Graph-API by using a 
           selenium FireFox instance! 
           This is against the FB guide lines and thus not allowed.

           USE THIS FOR EDUCATIONAL PURPOSES ONLY. DO NOT ACTAULLY RUN IT.
    """

    def __init__(self, ids=["oxfess"], corpus_file="posts_top.csv", depth=9, delay=2):
        self.ids = ids
        self.dump = corpus_file
        self.depth = depth + 1
        self.delay = delay
        # browser instance
        self.browser = webdriver.Firefox(executable_path=GECKODRIVER,
                                         firefox_binary=FIREFOX_BINARY,
                                         firefox_profile=PROFILE,)

        # creating CSV header

        self.tags =  [1106839036351172, 1106837419684667, 1260752974293110] 
        with open(self.dump, "w", newline='', encoding="utf-8") as save_file:
            writer = csv.writer(save_file)
            writer.writerow(["Group", "Author", "uTime", "Normal Time", "HH:MM:SS", "Text", "Permalink", "Likes"])

    def strip(self, string):
        """Helping function to remove all non alphanumeric characters"""
        words = string.split()
        words = [word for word in words if "#" not in word]
        string = " ".join(words)
        clean = ""
        for c in string:
            if str.isalnum(c) or (c in [" ", ".", ","]):
                clean += c
        return clean

    def collect_page(self, page):
        # navigate to page
        self.browser.get(
            'https://www.facebook.com/' + page + '/')

        # Scroll down depth-times and wait delay seconds to load
        # between scrolls
        for scroll in range(self.depth):

            # Scroll down to bottom
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(self.delay)

        # Once the full page is loaded, we can start scraping
        with open(self.dump, "a+", newline='', encoding="utf-8") as save_file:
            writer = csv.writer(save_file)
            links = self.browser.find_elements_by_link_text("See more")
            for link in links:
                link.click()
                print("Clicked a see more old")

            while self.safe_find_element_by_class_name('see_more_link') is not None:
                self.browser.find_element_by_class_name(
                    'see_more_link').click()
                print("Clicked a see more new")
                
            posts = self.browser.find_elements_by_class_name(
                "userContentWrapper")
            poster_names = self.browser.find_elements_by_xpath(
                "//a[@data-hovercard-referer]")

            for count, post in enumerate(posts):
                # Creating first CSV row entry with the poster name (eg. "Donald Trump")
                analysis = [poster_names[count].text]


                try:
                    # Creating a time entry.
                    time_element = post.find_element_by_css_selector("abbr")
                    utime = time_element.get_attribute("data-utime")
                    analysis.append(utime)

                    # Creating post text entry
                    text = post.find_element_by_class_name("userContent").text
                    status = self.strip(text)
                    analysis.append(status)

                    # Creating post reaccs entry
                    likes = post.find_element_by_class_name("_81hb").text
                    # status = self.strip(text)
                    print("Likes", likes)
                    analysis.append(likes)
                    

                    # Write row to csv
                    writer.writerow(analysis)
                except:
                    print("Failed!")
                    continue

    def collect_groups(self, group, setting = "TOP_POSTS"):
        # navigate to page
        # setting = "CHRONOLOGICAL"
        self.browser.get(
            'https://www.facebook.com/groups/' + group + '/?sorting_setting=' + setting)
        # self.browser.get('https://www.facebook.com/groups/725870897781323/post_tags/?post_tag_id=1260752974293110')

        # Scroll down depth-times and wait delay seconds to load
        # between scrolls
        for scroll in range(self.depth):

            # Scroll down to bottom
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(self.delay)

        # Once the full page is loaded, we can start scraping
        with open(self.dump, "a+", newline='', encoding="utf-8") as save_file:
            writer = csv.writer(save_file)
            # links = self.browser.find_elements_by_link_text("See more")
            # for link in links:
            #     link.click()
            #     print("Clicked a see more old 2")
            # while self.safe_find_element_by_class_name('see_more_link') is not None:
            #     print("Starting to wait for a see more new 2")
            #     elem = self.safe_find_element_by_class_name('see_more_link')

            #     # mySelectElement = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "see_more_link")))
            #     # mySelectElement.click()

            #     elem_scroll = ActionChains(self.browser).move_to_element(elem)
            #     elem_scroll.perform()
            #     elem.click()
            #     print("Clicked a see more new 2")

            posts = self.browser.find_elements_by_class_name(
                "userContentWrapper")
            poster_names = self.browser.find_elements_by_xpath(
                "//a[@data-hovercard-referer]")

            for count, post in enumerate(posts):
                # Creating first CSV row entry with the poster name (eg. "Donald Trump")
                analysis = [group, poster_names[count].text.replace(",", "<comma>")]

                # Creating a time entry.
                time_element = post.find_element_by_css_selector("abbr")
                utime = time_element.get_attribute("data-utime")

                dateTime = datetime.datetime.utcfromtimestamp(int(utime))
                datetime_obj_pacific = timezone('US/Pacific').localize(dateTime)
                print (dateTime, datetime_obj_pacific, datetime_obj_pacific.strftime(fmt))
                fmt_time = datetime_obj_pacific.strftime(fmt)
                analysis.append(utime)
                analysis.append(fmt_time)
                analysis.append(fmt_time.split(" ")[1]) #hour


                try:
                                    # Creating post text entry
                    text = post.find_element_by_class_name("userContent").text
                    status = self.strip(text).replace(",", "<comma>")
                    analysis.append(status)


                    see_more = self.safe_obj_find_see_more(post)
                    see_more_link = ""  
                    if(see_more is not None):
                        see_more_link = see_more.get_attribute('href')
                        print("See more link: ", see_more_link)
                    analysis.append(see_more_link)

                    # Creating post reaccs entry'
                    likes = 0
                    likes = post.find_element_by_class_name("_81hb").text
                    if likes[-1] == 'k' or likes[-1] == 'K':
                        if(len(likes) >= 3 and likes[-3] == '.'):
                            likes = likes[:-3] + likes[-2] + "00"
                        else:
                            likes = likes[:-1] + "000"
                    print("Likes 2", likes)
                    analysis.append(likes)

                    # Write row to csv
                    writer.writerow(analysis)
                except:
                    print("Failed")
                    continue
                    # status = self.strip(text)


    def collect(self, typ):
        if typ == "groups":
            for iden in self.ids:
                if(str(iden)[0] == '7' and int(iden) == 725870897781323):
                    for tag in self.tags:
                        self.collect_groups(iden + "/post_tags/?post_tag_id=" + str(tag))  
                else:
                    self.collect_groups(iden)      
        elif typ == "pages":
            for iden in self.ids:
                self.collect_page(iden)
        self.browser.close()

    def safe_find_element_by_id(self, elem_id):
        try:
            return self.browser.find_element_by_id(elem_id)
        except NoSuchElementException:
            return None

    def safe_find_element_by_class_name(self, class_id):
        try:
            return self.browser.find_element_by_class_name(class_id)
        except NoSuchElementException:
            return None

    def safe_obj_find_see_more(self, obj):
        try:
            return obj.find_element_by_class_name("see_more_link")
        except NoSuchElementException:
            try:
                return obj.find_elements_by_link_text("Continue Reading")[0]
            except: #IndexError, NoSuchElementException
                return None
            # except IndexError:
            #     return None

    def login(self, email, password):
        try:

            self.browser.get("https://www.facebook.com")
            self.browser.maximize_window()

            # filling the form
            self.browser.find_element_by_name('email').send_keys(email)
            self.browser.find_element_by_name('pass').send_keys(password)

            # clicking on login button
            self.browser.find_element_by_id('u_0_b').click()
            # if your account uses multi factor authentication
            mfa_code_input = self.safe_find_element_by_id('approvals_code')

            if mfa_code_input is None:
                return

            mfa_code_input.send_keys(input("Enter MFA code: "))
            self.browser.find_element_by_id('checkpointSubmitButton').click()

            # there are so many screens asking you to verify things. Just skip them all
            while self.safe_find_element_by_id('checkpointSubmitButton') is not None:
                dont_save_browser_radio = self.safe_find_element_by_id('u_0_3')
                if dont_save_browser_radio is not None:
                    dont_save_browser_radio.click()

                self.browser.find_element_by_id(
                    'checkpointSubmitButton').click()

        except Exception as e:
            print("There's some error in log in.")
            print(sys.exc_info()[0])
            exit()


if __name__ == "__main__":

    with open('credentials.txt') as f:
        email = f.readline().split('"')[1]
        password = f.readline().split('"')[1]

        if email == "" or password == "":
            print(
                "Your email or password is missing. Kindly write them in credentials.txt")
            exit()

    if args.groups:
        C = CollectPosts(ids=args.groups, depth=args.depth)
        C.login(email, password)
        C.collect("groups")
    elif args.pages:
        C = CollectPosts(ids=args.pages, depth=args.depth)
        C.login(email, password)
        C.collect("pages")
