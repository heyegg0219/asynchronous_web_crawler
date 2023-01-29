from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import grequests
import time
import gspread

scopes = ["https://spreadsheets.google.com/feeds"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("google_sheet.json", scopes)

client = gspread.authorize(credentials)

sheet = client.open_by_key("YOUR GOOGLE SHEET KEY").sheet1

movie_title = ['movie_name', 'movie_english_name ', 'movie_released', 'movie_length', 'movie_rating',
               "movie_url", 'movie_img_url', "movie_timetable"]
sheet.insert_row(movie_title)

base_url = "https://www.venice-cinemas.com.tw/"
start_time = time.time()  # 開始時間

links = list()  # 請求網址清單(1-4頁的網址)
for page in range(1, 5):
    links.append("https://www.venice-cinemas.com.tw/showtime.php?movie_date=&page=" + str(page))

reqs = (grequests.get(link) for link in links)  # 建立請求集合
response = grequests.imap(reqs, grequests.Pool(4))  # 發送請求

for r in response:
    soup = BeautifulSoup(r.content, "lxml")  # 解析HTML原始碼

    movie_blocks = soup.find_all("div", {"class": "show-time-list"})  # 電影區塊

    for movie in movie_blocks:
        movie_name = movie.find("div", {"class": "col-md-10 col-sm-9"}).findAll("h2")  # 電影名稱
        a_1 = movie_name[0].text
        movie_english_name = movie.find("div", {"class": "col-md-10 col-sm-9"}).findAll("h4")  # 電影英文名稱
        a_2 = movie_english_name[0].text
        movie_content = movie.find("ul", {"class": "entry-meta clearfix"}).findAll("li")
        a_3 = movie_content[0].text  # 上映日期
        a_4 = movie_content[1].text  # 電影片長
        a_5 = movie_content[2].text[23:]  # 電影級數
        movie_url = movie.find("a", {"class": "button button-small tright"}).get('href')  # 電影介紹
        a_6 = base_url + movie_url
        movie_img_url = movie.find("img", {"class": "img-responsive"}).get("src")  # 電影圖片
        a_7 = base_url + movie_img_url
        movie_timetable = movie.find("a", {"class": "movie-thumb"}).get('href')  # 電影時刻表
        a_8 = base_url + movie_timetable

        movie_data = [a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8]
        sheet.append_row(movie_data)

print("花費：" + str(time.time() - start_time) + "秒")
