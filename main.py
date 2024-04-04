import requests
from concurrent.futures import ThreadPoolExecutor
from time import time

URL_LIST = ["http://localhost:8000/", "http://localhost:8000/about"] * 25

def get_page(url: str):
    init_time = time()
    response = requests.get(url)
    total = format(time() - init_time, '.4f')

    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Requisição falhou: {response.status_code}")

    print(f"Tempo de execução: {total}s")

if __name__ == "__main__":
    run_type = "sequencial"

    if run_type == "thread":
        init_time = time()
        with ThreadPoolExecutor(5) as executor:
            executor.map(get_page, URL_LIST)
        total = format(time() - init_time, '.4f')
    else:
        init_time = time()

        for url in URL_LIST:
            get_page(url)
        
        total = format(time() - init_time, '.4f')

    print(f"Tempo total ({run_type}): {total}s")