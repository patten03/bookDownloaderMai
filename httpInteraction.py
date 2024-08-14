import requests
from bs4 import BeautifulSoup
from pathlib import Path
import random
import sys

headers = {
    'authority': 'www.nytimes.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'if-modified-since': 'Mon, 28 Nov 2022 00:06:21 GMT',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac macOS 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

def fakeDirection(session: requests.Session):
    spareBooks = [
        "http://elibrary.mai.ru/MegaPro/Download/ToView/71259?idb=NewMAI2014",
        "http://elibrary.mai.ru/MegaPro/Download/ToView/59863?idb=NewMAI2014",
        "http://elibrary.mai.ru/MegaPro/Download/ToView/68696?idb=NewMAI2014",
        "http://elibrary.mai.ru/MegaPro/Download/ToView/71003?idb=NewMAI2014",
        "http://elibrary.mai.ru/MegaPro/Download/ToView/67065?idb=NewMAI2014",
        "http://elibrary.mai.ru/MegaPro/Download/ToView/66949?idb=NewMAI2014",
        "http://elibrary.mai.ru/MegaPro/Download/ToView/67646?idb=NewMAI2014",
        "http://elibrary.mai.ru/MegaPro/Download/ToView/69820?idb=NewMAI2014",
        "http://elibrary.mai.ru/MegaPro/Download/ToView/71722?idb=NewMAI2014",
        "http://elibrary.mai.ru/MegaPro/Download/ToView/68696?idb=NewMAI2014",
        "http://elibrary.mai.ru/MegaPro/Download/ToView/67580?idb=NewMAI2014",
        "http://elibrary.mai.ru/MegaPro/Download/ToView/65147?idb=NewMAI2014",

    ]

    session.get(spareBooks[random.randint(0, len(spareBooks) - 1)], headers=headers, timeout=9000, allow_redirects=True)

# format user input, changes all input to a such format https://elibrary.mai.ru/ProtectedView/Book/ViewBook/*****
def inputBookLink() -> str:
    done = False
    # endless input, while we don't get right information
    while done == False:
        try:
            url = input("Введите ссылку на книгу или ее номер из elibrary.mai.ru: ")

            correctLink = "https://elibrary.mai.ru/ProtectedView/Book/ViewBook/"
            # changes url in order to not to get redirect (otherwise we can't download book with authorization requirements)
            if(url.rfind("idb=NewMAI2014") != -1):
                url = url.replace('?idb=NewMAI2014', '')
                url = url.replace('http://elibrary.mai.ru/MegaPro/Download/ToView/', '')
                url = correctLink + url
            # changes given number to url
            elif(url.isnumeric() and url != ""):
                url = correctLink + url
            # pass clear input
            elif(url.rfind("ProtectedView/Book/ViewBook/") != -1):
                pass
            # if we can't change format, throw exception
            else:
                raise Exception("Book does not exist or incorrect input")
            done = True
        # if user decided quit using ctrl+C
        except KeyboardInterrupt:
            sys.exit()
        except:
            print("Некорректный ввод, попробуйте ввести другую ссылку на книгу")
    
    return url


# intention of this function is reaction to redirection and getting data to extract last link and count of pages
def firstEnter(session: requests.Session, url: str) -> tuple[BeautifulSoup, requests.Response]:
    response = session.get(url, headers=headers, timeout=9000, allow_redirects=True)
    soup = BeautifulSoup(response.text, "html.parser")

    return soup, response

# check existence of book
def doesExist(soup: BeautifulSoup) -> bool:
    # data = soup.find(["h2"], string = ["Не могу найти запись в базе данных", "Неправильный формат записи!"])
    # if data == None:
    #     return True
    # else:
    #     return False

    # I've made a strange, but working solution
    try:
        getPageCount(soup)
        return True
    except:
        return False


# get count of pages in html
def getPageCount(soup: BeautifulSoup) -> int:
    pageCount = soup.find("span", id="bmkpagetotalnum")
    pageCount = int(pageCount.text)

    return pageCount

# get main image that shows on display from site
def getRefToPageImage(soup: BeautifulSoup, domain: str) -> str:
    imageSubRef = soup.find('img', id="pgimg")
    imageSubRef = imageSubRef['src']

    return domain + imageSubRef

# download image to specific folder with numerated name
def downloadImage(imageUrl: str, pageNum: int, donwloadingSession: requests.Session, folder: str):
    numLen = 5
    filename = str(pageNum).zfill(numLen)                # add name to file
    filename = filename + imageUrl[imageUrl.rfind("."):] # get and add extension to file

    fullpath = "./" + folder + "/" + filename            # make path to save image

    # download image
    response = donwloadingSession.get(imageUrl, allow_redirects=True)
    # in case if something goes wrong
    if (response.status_code != 200):
        print(f"Не удалось скачать страницу, поробуйте скачать ее вручную {imageUrl}")
    else:
        with open(fullpath, "wb") as f:
            f.write(response.content)
            print(f"Страница {pageNum} скачана")
        

# process of downloading page with last redirected link and count of pages
# return folder where all images were made
def downloadPages(session: requests.Session, url: str, pageCount: int) -> str:
    # print count of pages
    print(f"Книга содержит {pageCount} страниц")
    
    # make folder
    folder = url[url.rfind('/') + 1:]
    Path("./" + folder).mkdir(parents = True, exist_ok = True)
    print(f"Создание временной папки под названием \"{folder}\" для сохранения страниц")

    #define domain
    domain = url.split("/")[0] + "//" + url.split("/")[2]

    # download all pages
    downloadingSession = requests.Session()
    for page in range(1, pageCount + 1):
        # get soup of page
        urlParam = {"page": page, "pps": 1}
        response = session.get(url, headers = headers, params = urlParam)
        soup = BeautifulSoup(response.text, "html.parser")

        # download page
        imageUlr = getRefToPageImage(soup, domain)
        downloadImage(imageUlr, page, downloadingSession, folder)

    return folder

# main function of downloading books, responsible for getting from user url to book and downloading its pages
# return folder where all downloaded pages are saved, if something goes wrong it returns None
def downloadBook() -> str:
    session = requests.Session()     # make session to bypass authorization
    fakeDirection(session)           # actual bypassing authorization

    # loop until we get existing book
    folder = None
    found = False
    while (not(found)):
        url = inputBookLink()                     # getting url from user
        soup, response = firstEnter(session, url) # getting first site page with information like count of pages or non-existence of book

        # check existence of book
        if(doesExist(soup)):
            pageCount = getPageCount(soup)
            folder = downloadPages(session, response.url, pageCount)
            print("Все страницы загруженны")
            found = True
            
        else:
            print("Книга не найдена")
            fakeDirection(session)
            found = False
    
    return folder