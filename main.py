from time import sleep, time
import configparser
import requests
import json

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')

auth_url = 'https://lalafo.kg/api/auth/login'
ads_url = 'https://lalafo.kg/api/search/v3/feed/my/active?&page=1&expand=url&status_id_not[]=11'
ad_update_url = 'https://lalafo.kg/api/catalog/v32/posting-ads/'

auth_payload = json.dumps({
  'mobile': config.get('auth', 'phone'),
  'password': config.get('auth', 'password')
})

headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'ru-RU,ru;q=0.9',
  'authorization': 'Bearer',
  'content-type': 'application/json',
  'country-id': '12',
  'device': 'pc',
  'language': 'ru_RU',
  'origin': 'https://lalafo.kg',
  'referer': 'https://lalafo.kg/',
  'user-agent': 'Mozilla/5.0 (Linux; U; Linux x86_64) AppleWebKit/600.40 (KHTML, like Gecko) Chrome/52.0.2333.255 Safari/603'
}

try:
  auth_response = requests.post(auth_url, headers=headers, data=auth_payload).json()
  token = auth_response.get('token')
  headers['authorization'] = 'Bearer ' + token
  ads_response = requests.get(ads_url, headers=headers).json()
  ads_items = ads_response.get('items')
  start_time = time()
  for index, item in enumerate(ads_items):
    ad_id = str(item['id'])
    update_data = json.dumps({
      'currency': item['currency']
    })
    update_url = ad_update_url + ad_id
    ad_update_response = requests.put(update_url, headers=headers, data=update_data).json()
    print(ad_update_response.get('id'))

    if index != len(ads_items) - 1:
      sleep(3)
  end_time = time()
  print(f'Updated: {len(ads_items)} ads, to {end_time - start_time} seconds :)')

except:
  print('Error')
