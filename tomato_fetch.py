import pandas as pd
import requests
import random
import time
import json

tomato = pd.DataFrame(columns=['date', 'score', 'city', 'comment', 'nick'])
rangeList = range(1000)
print(rangeList)
randomList = random.sample(rangeList, 1000)
for i in randomList:
    print(str(i))
    try:
        time.sleep(1)
        url= 'http://m.maoyan.com/mmdb/comments/movie/1212592.json?_v_=yes&offset=' + str(i)
        html = requests.get(url=url).content
        data = json.loads(html.decode('utf-8'))['cmts']
        for item in data:
            tomato = tomato.append({'date': item['time'].split(' ')[0],
                                    'city': item['cityName'],
                                    'score': item['score'],
                                    'comment': item['content'],
                                    'nick': item['nick']}, ignore_index=True)
        tomato.to_csv('tomato.csv', index=False)
    except IOError as e:
        print(e.message)
        continue
    except:
        print('error')
        continue

