"""Scraper do catálogo oficial atualizado do exercício EBAC.

Referência: https://github.com/havokkmorands/multithreading (v2).
"""
import argparse
import csv
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import perf_counter
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://havokkmorands.github.io/movie-catalog/'
HEADERS = {'User-Agent': 'EBAC-Educational-Scraper/1.0', 'Accept-Language': 'pt-BR,pt;q=0.9'}


def get_soup(url):
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')


def extract_movie_details(url):
    soup = get_soup(url)
    section = soup.select_one('[data-testid="movie-detail"]')
    if section is None:
        raise ValueError(f'Página sem detalhes de filme: {url}')
    fields = []
    for field, prefix in [('movie-title', ''), ('movie-release', 'Lançamento:'), ('movie-rating', 'Nota:'), ('movie-synopsis', 'Sinopse:')]:
        tag = section.select_one(f'[data-testid="{field}"]')
        if tag is None:
            raise ValueError(f'Campo ausente: {field} em {url}')
        fields.append(tag.get_text(' ', strip=True).removeprefix(prefix).strip())
    return fields


def extract_movies(threads=5):
    soup = get_soup(BASE_URL)
    links = list(dict.fromkeys(urljoin(BASE_URL, tag['href']) for tag in soup.select('[data-testid="movie-link"][href]')))
    if not links:
        raise ValueError('Catálogo sem filmes; nenhum CSV será apresentado como sucesso.')
    with ThreadPoolExecutor(max_workers=min(threads, len(links))) as executor:
        # map preserva a ordem; gravação ocorre só na thread principal.
        return list(executor.map(extract_movie_details, links))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--threads', type=int, default=5)
    parser.add_argument('--output', type=Path, default=Path('movies.csv'))
    args = parser.parse_args()
    if args.threads < 1:
        parser.error('--threads precisa ser maior que zero')
    started = perf_counter()
    rows = extract_movies(args.threads)
    elapsed = perf_counter() - started
    with args.output.open('w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'release_date', 'rating', 'synopsis'])
        writer.writerows(rows)
    print(json.dumps({'source': BASE_URL, 'threads': args.threads, 'movies': len(rows), 'seconds': round(elapsed, 4), 'output': str(args.output)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
