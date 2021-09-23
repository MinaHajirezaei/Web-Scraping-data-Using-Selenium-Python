import json
import csv
import re
import time
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
driver = webdriver.Chrome(executable_path='/home/khorshidsoft/Downloads/chromedriver_linux64/chromedriver')

# url_films=["https://www.filimo.com/m/9vAeB"]
url_films=[]
sentence_list=[]

driver.get("https://www.filimo.com/movies/1/new-iran")
time.sleep(10)

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(6)
	new_height = driver.execute_script("return document.body.scrollHeight")
	if new_height == last_height:
        	break
	last_height = new_height
	
#for i in range(160):
#	url_film = driver.find_element_by_xpath('//*[@id="grid_5fe1b28e8b1c7"]/div/div[{:}]/div/div[2]/div/a'.format(i+1))
#	url_filmss = url_film.get_attribute("href")
#	film_text=url_film.text
#	print(film_text)
#	url_films.append(url_filmss)

film_elementt = driver.find_elements_by_class_name("ui-fs-small.truncate.ui-pt-4x.list_title")
for film_element in film_elementt:
	url_film = film_element.find_element_by_tag_name("a")
	film_text=url_film.text
	#print(film_text)
	x = re.search("مخصوص نابینایان", film_text)
	y = re.search("مخصوص ناشنوایان", film_text)
	z = re.search("پشت صحنه", film_text)
	w = re.search("نماهنگ", film_text)
	if x or y or z or w:	
		continue
	else:	
		url_filmss = url_film.get_attribute("href")
		url_films.append(url_filmss)


print(len(url_films))
print(url_films)

for urls_film in url_films:
	time.sleep(1)
	driver.get(urls_film)
	time.sleep(10)
	# driver.execute_script("return document.body.scrollHeight")
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(5)

	try:
		comingsoon = driver.find_element_by_xpath('//*[@id="login-to-watch"]')
		if comingsoon!=None:
			try:
				descriptionn = driver.find_element_by_xpath('//*[@id="movieContainer"]/div[2]/div/div/div/div/div[1]/p')
				description = descriptionn.text
				print(description)
			except:
				description=None


			try:
				titlee_fa = driver.find_element_by_xpath('//*[@id="movieToggleMobile"]/h1/span[1]/span[1]')
				title_fa = titlee_fa.text
				print(title_fa)
			except:
				title_fa=None	

			try:
				titlee_en = driver.find_element_by_xpath('//*[@id="movieToggleMobile"]/h1/span[2]')
				title_en = titlee_en.text
				print(title_en)
			except:
				title_en=title_fa	

			try:
				directorr = driver.find_element_by_xpath('//*[@id="js__fullpage"]/main/div/div[1]/div/div[2]/div/div/div[2]/div[3]/div[1]/div/a')
				director = directorr.text
				print(director)
			except:
				director=None

			try:
				element1 = driver.find_element_by_xpath('//*[@id="js__fullpage"]/main/div/div[1]/div/div[2]/div/div/div[2]/div[3]/div[1]')
				element2 = element1.text
				element3 = element2.replace('کارگردان:', '')
				element4 = element3.replace(director, '')
				duratiion = element4.split('-', 1)[0]
				duration = duratiion.replace("\n",'')
				print(duration)

				for years in element4.split() :
					if years.startswith('13'): 
					# year=re.findall(r'\b[13]\w+',element4)
						year=years
						print(year)
			except:
				year=None
				duration=None

			try:
				imdbs = driver.find_element_by_xpath('//*[@id="js__fullpage"]/main/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]/span')
				imdb = imdbs.text
				print(imdb)
			except:
				imdb=None

			try:
				ratingg = driver.find_element_by_xpath('//*[@id="percentNumber"]')
				rating = ratingg.text + "%"
				print(rating)
			except:
				rating=None
				
			try:
				image_urll = driver.find_element_by_xpath('//*[@id="js__fullpage"]/main/div/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/img')
				image_urrl = image_urll.get_attribute("src") 
				image_url="/data/filimo_images/{:}.jpg".format(title_en)
				print(image_url)
				with open("{}.jpg".format(title_en), 'wb') as f:
					r = requests.get(image_urrl)
					f.write(r.content)

			except:
				image_url=None
				
			try:
				genree = driver.find_element_by_xpath('//*[@id="js__fullpage"]/main/div/div[1]/div/div[2]/div/div/div[2]/div[3]/div[2]')
				genre = genree.text
				print(genre)
			except:
				genre=None
				
			try:
				actorsss = driver.find_element_by_xpath('//*[@id="movieContainer"]/div[4]/div/div/ul')
				actors = actorsss.text
				print(actors)
			except:
				actors=None

			try:
				
				elemennt = driver.find_element_by_xpath('//*[@id="movieContainer"]/div[2]/div/div/div/div[1]/div')
				elemennt.click()
				time.sleep(10)
				trailer_linkk = driver.find_element_by_xpath('/html/body/div[8]/div/div[1]/div[1]/div/div/video/source')
				trailer_link = trailer_linkk.get_attribute("src")
				print(trailer_link)
			except:
				trailer_link=None	
				

			sentence={"description":description,"title_fa":title_fa,"title_en":title_en,"director":director,"year":year,"imdb":imdb,"rating":rating,"duration":duration,"genre":genre,"actors":actors,"trailer_link":trailer_link}
			print(sentence)
			sentence_list.append(sentence)
	except:
		continue


json_object =json.dumps(sentence_list, indent=2, ensure_ascii=False, default=str)
with open("filimo.json", "a+") as outfile:
	outfile.write(json_object)

