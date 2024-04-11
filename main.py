import requests
from concurrent.futures import ThreadPoolExecutor
from time import time
from threading import Semaphore

URL_LIST = ["http://localhost:8000/", "http://localhost:8000/about"] * 100
MAX_REQUEST = 5

semaphore = Semaphore(MAX_REQUEST)

def get_page(url: str):
    semaphore.acquire()
    print(f"Semaphore acquire: {semaphore}")
    init_time = time()
    response = requests.get(url)
    total = format(time() - init_time, '.4f')

    if response.status_code == 200:
        print(response.status_code)
    else:
        print(f"Requisição falhou: {response.status_code}")

    semaphore.release()
    print(f"Semaphore release: {semaphore}")
    print(f"Tempo de execução: {total}s")

if __name__ == "__main__":
    TYPES = ["sequencial", "thread"]
    run_type = TYPES[1]

    times = []
    MAX_ITERATION = 5

    for _ in range(MAX_ITERATION):
        if run_type == "thread":
            init_time = time()
            print("Iniciou Requisição")
            with ThreadPoolExecutor(20) as executor:
                executor.map(get_page, URL_LIST)
            total = format(time() - init_time, '.4f')
            print("Finalizou requisição")
        else:
            init_time = time()

            for url in URL_LIST:
                get_page(url)
            
            total = format(time() - init_time, '.4f')

        times.append(total)

    print(times)