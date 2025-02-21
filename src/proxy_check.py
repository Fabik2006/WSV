import queue
import requests
import threading

PROXY_FILE = "D:/MyProjects/WSCareerSite/WSV/src/proxy_list.txt"
VALID_PROXIES = "D:/MyProjects/WSCareerSite/WSV/src/valid_proxies.txt"

def check_proxy(q, valid_proxies):

    while len(valid_proxies) <= 5:
        proxy = q.get()
        try:
            res = requests.get("https://www.google.com/",
                                   proxies = {"http": proxy,
                                              "https": proxy},
                                   timeout=2)
            if res.status_code == 200:
                    valid_proxies.append(proxy)
                    print(f"Proxy {proxy} is valid")

        except requests.RequestException:
                continue

        finally:
                q.task_done()



def check_proxies():

    print("Running proxy rotation...")
    print("Please wait!")

    q = queue.Queue()
    valid_proxies = []

    with open(PROXY_FILE, "r") as f:
        proxies = f.read().split("\n")
        for p in proxies:
            q.put(p)

    threads = []
    for _ in range(10):
        t = threading.Thread(target = check_proxy,
                             args=(q, valid_proxies))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    with open (VALID_PROXIES, "w") as r:
        r.write("\n".join(valid_proxies))
    print(f"Found {len(valid_proxies)} valid proxies")

def read_proxies():
    with open ("D:/MyProjects/WSCareerSite/WSV/src/valid_proxies.txt", "r") as p:
        proxies = p.read().split("\n")

    return proxies

check_proxies()
