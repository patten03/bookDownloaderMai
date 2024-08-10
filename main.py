import requests
from bs4 import BeautifulSoup
from pathlib import Path
import random

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
    ]

    session.get(spareBooks[random.randint(0, len(spareBooks) - 1)],headers=headers, timeout=9000, allow_redirects=True)

# format user input
def inputBookLink() -> str:
    done = False
    while done == False:
        try:
            url = input("Введите ссылку на книгу или ее номер из elibrary.mai.ru: ")

            correctLink = "https://elibrary.mai.ru/ProtectedView/Book/ViewBook/"
            if(url.rfind("idb=NewMAI2014") != -1):
                url = url.replace('?idb=NewMAI2014', '')
                url = url.replace('http://elibrary.mai.ru/MegaPro/Download/ToView/', '')
                url = correctLink + url
            elif(url.isnumeric() and url != ""):
                url = correctLink + url
            elif(url.rfind("ProtectedView/Book/ViewBook/") != -1):
                pass
            else:
                raise Exception("Book does not exist or incorrect input")
            done = True
        except:
            print("Некорректный ввод, попробуйте ввести другую ссылку на книгу")
    
    return url


# intention of this function is reaction to redirection and getting data to extract last link and count of pages
def firstEnter(session: requests.Session, url: str) -> tuple[BeautifulSoup, requests.Response]:
    response = session.get(url, headers=headers, timeout=9000, allow_redirects=True)
    soup = BeautifulSoup(response.text, "html.parser")

    return soup, response

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
def downloadImage(imageUrl: str, pageNum: int, session: requests.Session, folder: str):
    numLen = 5
    filename = str(pageNum).zfill(numLen)                # add name to file
    filename = filename + imageUrl[imageUrl.rfind("."):] # get and add extension to file

    fullpath = "./" + folder + "/" + filename            # make path to save image

    # download image
    with open(fullpath, "wb") as f:
        response = session.get(imageUrl, headers=headers, allow_redirects=True)
        # exceptional situation which I found on 2134's book
        f.write(response.content)

# process of downloading page with last redirected link and count of pages
def downloadBook(session: requests.Session, url: str, pageCount: int):
    # make folder
    folder = url[url.rfind('/') + 1:]
    Path("./" + folder).mkdir(parents = True, exist_ok = True)

    #define domain
    domain = url.split("/")[0] + "//" + url.split("/")[2]

    # download all pages
    for page in range(1, pageCount + 1):
        urlWithImage = url + f"?page={page}&pps=1"

        # get soup of page
        response = session.get(urlWithImage, headers = headers)
        soup = BeautifulSoup(response.text, "html.parser")

        imageUlr = getRefToPageImage(soup, domain)
        downloadImage(imageUlr, page, session, folder)
        print(f"{page} из {pageCount} страниц скачано")
    
def main():
    session = requests.Session()
    fakeDirection(session)
    url = inputBookLink()
    soup, response = firstEnter(session, url)
    pageCount = getPageCount(soup)
    downloadBook(session, response.url, pageCount)
    

if __name__ == "__main__":
    main()
