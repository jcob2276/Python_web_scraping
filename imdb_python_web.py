from bs4 import BeautifulSoup
import requests

try:
    source = requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
    source.raise_for_status()

    soup = BeautifulSoup(source.text, 'html.parser')

    movies = soup.find('tbody', class_='lister-list').find_all('tr')

    year_stats = {}
    rating_stats = {}
    director_stats = {}
    actor_stats = {}

    for movie in movies:
        name = movie.find('td', class_='titleColumn').a.text
        rank = movie.find('td', class_='titleColumn').get_text(strip=True).split('.')[0]
        year = int(movie.find('td', class_='titleColumn').span.text.strip('()'))
        rating = float(movie.find('td', class_='ratingColumn imdbRating').strong.text)
        actors = movie.find('td', class_='titleColumn').find('a')['title'].split(', ')[1:]
        

        # Grouping movies by decade
        decade = year // 10 * 10
        decade_str = f'{decade}s'

        if decade_str in year_stats:
            year_stats[decade_str] += 1
        else:
            year_stats[decade_str] = 1

        # Counting movies by rating
        rating_str = f'{rating:.1f}'
        if rating_str in rating_stats:
            rating_stats[rating_str] += 1
        else:
            rating_stats[rating_str] = 1
        
        # Counting movies by director
        director = movie.find('td', class_='titleColumn').a['title'].split(',')[0]
        if director in director_stats:
            director_stats[director] += 1
        else:
            director_stats[director] = 1

        for actor in actors:
            if actor in actor_stats:
                actor_stats[actor] += 1
            else:
                actor_stats[actor] = 1


    # Printing movie counts by decade
    for decade, count in sorted(year_stats.items()):
        print(f'{decade}: {count}')

    # Printing movie counts by rating
    for rating, count in sorted(rating_stats.items()):
        print(f'{rating}: {count}')

    # Printing movie counts by director
    sorted_directors = sorted(director_stats.items(), key=lambda x: x[1], reverse=True)
    for director, count in sorted_directors:
        print(f'{director}: {count}')

    sorted_actors = sorted(actor_stats.items(), key=lambda x: x[1], reverse=True)

    for actor, count in sorted_actors:
        print(f'{actor}: {count}')



except Exception as e:
    print(e)


