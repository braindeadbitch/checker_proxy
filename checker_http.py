import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time
with open('proxy_list.json', 'r') as f:
    proxy_list = json.load(f)

start_time = time.time()
def check_proxy(proxy_dict):
    proxy = proxy_dict['proxy']
    proxies = {'http': 'http://' + proxy}
    try:
        response = requests.get('https://www.google.com/', proxies=proxies, timeout=5)
        print(response.status_code)
        if response.status_code == 200:
            return proxy_dict
    except:
        pass

with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(check_proxy, proxy_dict) for proxy_dict in proxy_list]

    valid_proxies = []

    for future in futures:
        result = future.result()
        if result:
            valid_proxies.append(result)

with open('valid_proxy_list.json', 'w') as f:
    json.dump(valid_proxies, f)

work_time = time.time() - start_time
print(f'Время работы чекера:{work_time}\n'
      f'Прочекано:{len(proxy_list)} прокси\n'
      f'Валидных прокси: {len(valid_proxies)}')
