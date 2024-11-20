from tqdm import tqdm
from collections import defaultdict

import pandas as pd

from bs4 import BeautifulSoup


from retry_requests import (
    retry,
)


def get_animals_from_page(
    soup,
):
    page_li_with_names = soup.find(
        "div",
        {"class": "mw-category mw-category-columns"},
    ).find_all("li")
    animal_names = []
    for animal in page_li_with_names:
        animal_names.append(animal.text)
    return animal_names


def get_all_links(
    soup,
):
    links = soup.find(
        "div",
        {"class": "ts-module-Индекс_категории plainlinks"},
    ).find_all("a")
    return [link.get("href") for link in links]


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}

url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
session = retry()
r = session.get(
    url,
    headers=headers,
)
soup = BeautifulSoup(
    r.content,
    "html5lib",
)

links = list(set(get_all_links(soup)))

animal_names = []
for link in tqdm(links):
    r = session.get(
        link,
        headers=headers,
    )
    soup = BeautifulSoup(
        r.content,
        "html5lib",
    )
    animal_names += get_animals_from_page(soup)

animal_names = set(animal_names)
print(f"Found {len(animal_names)} animals")

c = defaultdict(int)
for name in animal_names:
    c[name[0]] += 1

res = {
    "Letter": c.keys(),
    "count": c.values(),
}
df = pd.DataFrame(res)
df = df.sort_values(by="Letter")
df.to_csv(
    "result.csv",
    index=False,
    header=False,
)
