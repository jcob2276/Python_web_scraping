from bs4 import BeautifulSoup
import requests

try:
    source = requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
    source.raise_for_status()

    soup = BeautifulSoup(source.text,'html.parser')

    movies = soup.find('tbody', class_='lister-list').find_all('tr')
   # print(len(movies))

    for movie in movies:

        name = movie.find('td', class_="titleColumn").a.text

        #title = name.text.strip()

        rank = movie.find('td',class_="titleColumn").get_text(strip=True).split('.')[0]
                                                                                
        year = movie.find('td', class_="titleColumn").span.text.strip('()')
        
        rating = movie.find('td', class_="ratingColumn imdbRating").strong.text

        print(rank, name, year, rating)
        
except Exception as e:
    print(e)
