from bs4 import BeautifulSoup
import requests, json, django, os,time, random, re
from django.db.models import Q
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Week_3.settings")
django.setup()
from engine.models import *

def getIndex():
    try:
        url = 'https://movie.douban.com/j/new_search_subjects?sort=T&tags=%E6%AC%A7%E7%BE%8E&start=0&limit=1000'
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        json_data = json.loads(r.text)
        movie_list = []
        for json_item in json_data['data']:
            movie_list.append(Movie(url=json_item['url'], rate=float(json_item['rate']), title=json_item['title']))
        Movie.objects.bulk_create(movie_list)
    except:
        print('get index failed')
def getMovie():
    idx = 643
    try:
        movies = Movie.objects.filter(id__gt=642)
        for movie in movies:
            idx += 1
            with open('movies/' + str(movie.id) + '.txt', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                info = soup.find(id='info').contents
                i = 0
                diretors = []
                scriptwriters = []
                actors = []
                categories = []
                dates = []
                length = []
                while (i < len(info)):
                    if info[i].name == 'span':
                        if info[i].find('span'):
                            tmp = info[i].find_all('span')
                            if tmp[0].string == '导演':
                                tmp2 = info[i].find_all('a')
                                for j in tmp2:
                                    diretors.append(j.string)
                            elif tmp[0].string == '编剧':
                                tmp2 = info[i].find_all('a')
                                for j in tmp2:
                                    scriptwriters.append(j.string)
                            elif tmp[0].string == '主演':
                                tmp2 = info[i].find_all('a')
                                for j in tmp2[:10]:
                                    try:
                                        actor = Actor.objects.get(url=j['href'])
                                    except Actor.DoesNotExist:
                                        actor = Actor(name=j.string, url='https://movie.douban.com' + j['href'])
                                    actor.save()
                                    actor.movies.add(movie)
                        elif info[i].string == '语言:':
                            movie.language = info[i+1].replace(' ', '')
                            i += 1
                        elif info[i].string == '制片国家/地区:':
                            movie.country = info[i+1].replace(' ', '')
                            i += 1
                        elif info[i].string == '又名:':
                            movie.other_names = info[i + 1].replace(' ', '')
                            i += 1
                        elif info[i].string == 'IMDb链接:':
                            movie.IMDb = info[i + 2]['href']
                            i += 2
                        elif 'property' in info[i].attrs:
                            if (info[i]['property'] == 'v:genre'):
                                categories.append(info[i].string)
                            elif (info[i]['property'] == 'v:initialReleaseDate'):
                                dates.append(info[i].string)
                            elif (info[i]['property'] == 'v:runtime'):
                                length.append(info[i].string)
                    i += 1
                movie.diretors = ','.join(diretors)
                movie.scriptwriters = ','.join(scriptwriters)
                movie.categories = ','.join(categories)
                movie.dates = ','.join(dates)
                movie.length = ','.join(length)
                summary = ''
                summary_list = soup.find('span' , property="v:summary").contents
                for item in summary_list:
                    summary += str(item).replace(' ','').replace('\n','')
                movie.summary = summary
                movie.image_url = soup.find('img', rel='v:image')['src']
                comment_list = soup.find_all(class_='comment-item')
                for item in comment_list:
                    tmp = item.find(class_="hide-item full")
                    if tmp == None:
                        tmp = item.find(class_="short")
                    if tmp != None:
                        comment = Comment(description=tmp.string, movie=movie)
                        comment.save()
                        movie.comments.add(comment)
            movie.save()
            print(movie.id)
    except Exception as e:
        print(e)
        return idx

def getActor():
    r = re.compile(':|\n| ')
    r1 = re.compile(':|\n')
    try:
        actors = Actor.objects.all()
        for actor in actors:
            with open('actors/' + str(actor.id) + '.txt', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                name = soup.find('h1')
                if re.match('[A-Za-z ]*', actor.name):
                    actor.eng_name = actor.name
                else:
                    r2 = re.compile(actor.name + ' (.+)')
                    eng_name = re.match(r2, name.string)
                    if eng_name is not None:
                        actor.eng_name = eng_name.group(1)
                    else:
                        actor.eng_name = ''
                info = soup.find(class_='info').find_all('li')
                for item in info:
                    item2 = item.contents
                    if (item2[1].string == '性别'):
                        actor.gender = re.sub(r,'', item2[2])
                    elif (item2[1].string == '星座'):
                        actor.star_sign = re.sub(r,'', item2[2])
                    elif (item2[1].string == '出生日期'):
                        actor.birth_date = re.sub(r, '', item2[2])
                    elif (item2[1].string == '出生地'):
                        actor.birth_place = re.sub(r, '', item2[2])
                    elif (item2[1].string == '职业'):
                        actor.occupation = re.sub(r, '', item2[2]).replace('/', ',')
                    elif (item2[1].string == '更多中文名'):
                        actor.other_names = re.sub(r, '', item2[2]).replace('/', ',')
                    elif (item2[1].string == '家庭成员'):
                        actor.families = re.sub(r1, '', item2[2]).strip().replace(' / ', ',')
                    elif (item2[1].string == 'imdb编号'):
                        actor.IMDb = item2[3]['href']
                summary_list = soup.find(id='intro')
                if summary_list.find(class_='all hidden'):
                    summary_list = summary_list.find(class_='all hidden')
                else:
                    summary_list = summary_list.find(class_='short')
                summary = ''
                if summary_list is not None:
                    for item in summary_list.contents:
                        summary += str(item)
                actor.summary = summary
                actor.imag_url = soup.find(class_='nbg')['href']
                actor.save()
                print(actor.id)
    except Exception as e:
        print(e)
        return actor.id

def crawlMovie():
    idx = 0
    try:
        movies = Movie.objects.all()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        for movie in movies:
            movie_url = movie.url
            r = requests.get(movie_url, headers=headers)
            r.raise_for_status()
            r.encoding = 'utf-8'
            if r.text == '':
                return idx
            f = open('movies/' + str(movie.id) + '.txt', 'w', encoding='utf-8')
            f.write(r.text)
            idx += 1
            print(idx)
            time.sleep(2 + random.randint(1, 10) / 10.0)
    except Exception as e:
        print(e)
        print('get movie failed')
        return idx

def crawlActor():
    try:
        actors = Actor.objects.all()
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        for actor in actors:
            actor_url = actor.url
            r = requests.get(actor_url, headers=headers)
            r.raise_for_status()
            r.encoding = 'utf-8'
            if r.text == '' or not (r.text[1] == '!' or r.text[2] == '!'):
                print(r.text)
                return actor.id
            f = open('actors/' + str(actor.id) + '.txt', 'w', encoding='utf-8')
            f.write(r.text)
            f.close()
            #time.sleep(1 + random.randint(1, 10) / 10.0)
            print(actor.id)
    except Exception as e:
        print(e)
        print('get movie failed')
        return actor.id

def movie_changes():
    movies = Movie.objects.all()
    for movie in movies:
        with open('movies/' + str(movie.id) + '.txt', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            summary = ''
            summary_list = soup.find('div', id='link-report')
            if summary_list.find('span', class_='all hidden'):
                summary_list = summary_list.find('span', class_='all hidden').contents
            else:
                summary_list = summary_list.find('span', property="v:summary").contents
            for item in summary_list:
                item = str(item).strip()
                if (item != '' and item[0] != '<'):
                    summary += '　　'
                summary += item
            movie.summary = summary
        print(movie.id)
    Movie.objects.bulk_update(movies,['summary'])

def actor_changes():
    actors = Actor.objects.filter(id=1312)
    for actor in actors:
        with open('actors/' + str(actor.id) + '.txt', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            name = soup.find('h1')
            if actor.name.replace(' ', '').isalpha():
                actor.eng_name = actor.name
            else:
                r2 = re.compile(actor.name + ' (.+)')
                eng_name = re.match(r2, name.string)
                if eng_name is not None:
                    actor.eng_name = eng_name.group(1)
                else:
                    actor.eng_name = ''
            print(actor.eng_name)
def duplicate():
    actors = Actor.objects.order_by('url')
    refer = actors[0]
    for i in range(1, len(actors)):
        if (actors[i].url == refer.url):
            movies = actors[i].movies.all()
            for movie in movies:
                movie.actors.add(refer)
                movie.save()
            actors[i].delete()
            print(actors[i].name)
        else:
            refer = actors[i]
def crawlMoviePic():
    try:
        movies = Movie.objects.filter(id__gt=621)
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        for movie in movies:
            r = requests.get(movie.image_url, headers=headers)
            r.raise_for_status()
            with open('movie_pics/' + str(movie.id) + '.jpg', 'wb') as f:
                f.write(r.content)
            print(movie.id)
    except Exception as e:
        print(e)
        print('get movie failed')
        return movie.id

def crawlActorPic():
    try:
        actors = Actor.objects.filter(id__gt=4119)
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        for actor in actors:
            if (actor.imag_url != ''):
                r = requests.get(actor.imag_url, headers=headers)
                r.raise_for_status()
                with open('actor_pics/' + str(actor.id) + '.jpg', 'wb') as f:
                    f.write(r.content)
                print(actor.id)
    except Exception as e:
        print(e)
        print('get movie failed')
        return actor.id
def deletefiles():
    filelist = os.listdir('actors')
    cnt = 0
    for file in filelist:
        filename = re.match('(.*)' + '[.]txt', file).group(1)
        try:
            Actor.objects.get(id=filename)
        except Actor.DoesNotExist:
            os.remove('E:/QTproject/Week_3/actors/' + file)

if __name__ == '__main__':
    #getIndex()
    #print(getMovie())
    #print(crawlActor())
    #actor_changes()
    #print(crawlMovie())
    #crawlActorPic()
    #deletefiles()
    movie_changes()


