import csv
import json
import math
from random import uniform
from time import sleep

import requests
from bs4 import BeautifulSoup

from engines import Google, Yandex

results = []


def validate_int(option):
    try:
        int_option = int(option)
        return int_option
    except Exception:
        raise ValueError('Введите числовое значение')


def get_search_engine(option):
    if option == 1:
        return Google()
    if option == 2:
        return Yandex()
    else:
        raise ValueError('Неправильный вариант')


def validate_recursive(option):
    if option.lower() in ['д', 'н']:
        return option
    else:
        raise ValueError('Неправильный вариант')


def is_recursive(option):
    if option.lower() == 'д':
        return True
    return False


def get_export_format(option):
    if option == 1:
        return 'console'
    if option == 2:
        return 'json'
    if option == 3:
        return 'csv'
    else:
        raise ValueError('Неправильный вариант')


def get_html(url):
    try:
        response = requests.get(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/83.0.4103.97 Safari/537.36'})
        return response.text
    except ConnectionError:
        print('Не удалось получить html страницу')


def parse_html(html):
    return BeautifulSoup(html, 'html.parser')


def fill_page_results(search_engine, page_need, result_quantity, query):
    next_page_url = None
    for page_count in range(1, page_need + 1):
        if page_count == 1:
            html = get_html(search_engine.start_point(query))
        else:
            sleep(uniform(3, 6))
            html = get_html(next_page_url)
        soup = parse_html(html)
        next_page_url = search_engine.next_page_url(soup)

        page_results = search_engine.get_results(soup)

        for page_result in page_results:
            if len(results) < result_quantity:
                results.append(page_result)


def get_recursive_links(url, links_list):
    links = []
    for i in range(len(links_list)):
        link = links_list[i]['href']
        if link.startswith('#'):
            links.append(url + link)
        elif link.startswith('/'):
            links.append(url + link[1:])
        else:
            links.append(link)
    return links


def export_results(export_format, search_results, recursive=False):
    if export_format == 'console':
        print_results(search_results)
    elif export_format == 'json':
        save_to_json(search_results)
    elif export_format == 'csv':
        save_to_csv(search_results, recursive)


def print_results(search_results):
    for result in search_results:
        res_string = f'{result["title"]}: {result["link"]}'
        if 'recursive_links' in result:
            res_string = res_string + ', Рекурсивные ссылки: '
            for link in result['recursive_links']:
                res_string = res_string + link + ', '
        print(res_string)


def save_to_json(search_results):
    with open('results.txt', 'w') as json_file:
        json.dump(search_results, json_file, ensure_ascii=False, indent=4)


def save_to_csv(search_results, recursive=False):
    with open('results.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        if recursive:
            csv_writer.writerow(
                ['Заголовок', 'Ссылка', 'Рекурсивные ссылки']
            )
            for result in search_results:
                recursive_links = ', '.join(
                    [str(link) for link in result['recursive_links']]
                )
                csv_writer.writerow(
                    [result['title'], result['link'], recursive_links]
                )
        else:
            csv_writer.writerow(['Заголовок', 'Ссылка'])
            for result in search_results:
                csv_writer.writerow([result['title'], result['link']])


def main():
    query = input('Введите текст запроса: ')
    search_engine = get_search_engine(
        validate_int(input('Выберите поисковый сервис:\n'
                           '1. Google.\n'
                           '2. Yandex.\n'
                           'Вариант: '))
    )
    result_quantity = validate_int(input('Количество результатов: '))
    recursive = is_recursive(
        validate_recursive(input('Выполнить рекурсивный поиск? (Д/Н): '))
    )
    export_format = get_export_format(
        validate_int(input('Укажите формат вывода результатов:\n'
                           '1. Консоль.\n'
                           '2. JSON.\n'
                           '3. CSV.\n'
                           'Вариант: '))
    )

    print('--------------------\n'
          'Начинаю поиск ссылок')

    page_need = math.ceil(result_quantity / 10)

    fill_page_results(search_engine, page_need, result_quantity, query)

    if recursive:
        for res in results:
            html = get_html(res['link'])
            soup = BeautifulSoup(html, 'html.parser')
            links_list = soup.find_all('a', href=True)

            link = res['link']
            res['recursive_links'] = get_recursive_links(link, links_list)

    export_results(export_format, results, recursive)

    print('Готово!')


if __name__ == '__main__':
    main()
