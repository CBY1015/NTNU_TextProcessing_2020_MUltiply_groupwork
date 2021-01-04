import requests , time , bs4 , os , math

def grab(url:str):
	page = requests.get(url)
	if page.status_code != 200:
		return None
	soup = bs4.BeautifulSoup(page.text , "lxml")
	return soup

def write_Pansci(soup:bs4.BeautifulSoup , filename:str):
	with open("articles/Pansci/" + filename + ".txt" , "w+" , encoding = "utf-8") as f:
		print(soup.title.get_text()[:-13] + "\n" , file = f)
		article_time = soup.find("span" , class_ = "post-text-light")
		print(article_time.get_text()[1:] , file = f)
		article = soup.find("div" , class_ = "post-content-container").find_all(["p" , "li" , "h3" , "h2"])
		li_count = 1
		for e in article:
			if e.get_text()[:4] == "延伸閱讀":
				pass
			elif e.get_text() == "參考資料":
				li_count = 1
				print("\n" + e.get_text() , file = f)
			elif e.name == "li":
				if e.parent.name == "ul":
					li_count = 0
					print("＞" , e.get_text() , file = f , sep = "")
				else:
					print(li_count , "." , e.get_text() , sep = "" , file = f)
					li_count += 1
			elif e.parent.name[0] not in ["p" , "h"]:
				li_count = 1
				print(e.get_text() , file = f)

def get_Pansci_list(page_num:int):
	page = requests.get("https://pansci.asia/news/page/" + str(page_num))
	soup = bs4.BeautifulSoup(page.text , "lxml")
	soup_list = soup.find_all("div" , class_ = "col-md-8")
	#soup_list = soup.find_all("a" , class_ = "post-title")
	article_list = []
	for e in soup_list:
		try:
			article_list.append(e.find("a" , class_ = "post-title").get("href"))
		except:
			pass
	return article_list

def progress_bar(now:int , total:int):
	print("\r" , end = "")
	print("[" , end = "")
	for e in range(15):
		current = now * 15 // total
		if e < current:
			print("=" , end = "")
		elif e == current:
			print(">" , end = "")
		else:
			print(" " , end = "")
	percent = "%3.2f" % (now * 100 / total)
	print("]%3d" % int(float(percent)) , end = "")
	print(str(percent)[-3:] , end = "")
	print("%" , end = "")

if __name__ == "__main__":
	if not os.path.exists("articles/Pansci"):
		os.mkdir("articles/Pansci")
	pages = 50
	for e in range(pages):
		num = e + 1
		progress_bar(num , pages)
		article_list = get_Pansci_list(num)
		for url in article_list:
			try:
				soup = grab(url)
				write_Pansci(soup , url[-6:])
			except Exception as e:
				pass