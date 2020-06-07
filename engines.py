from urllib.parse import quote


class Google:
    base_url = 'https://www.google.ru'
    start_url = 'https://www.google.ru/search?q='

    def start_point(self, query):
        return self.start_url + quote(query)

    @staticmethod
    def get_results(soup):
        results_list = soup.find_all('div', class_='r')
        results = []
        for res in results_list:
            results.append(
                {
                    'title': res.find('h3').text,
                    'link': res.find('a')['href']
                 }
            )
        return results

    def next_page_url(self, soup):
        navigation = soup.find('div', id='foot')
        next_page = navigation.find_all('td')[-1].find('a')['href']
        return self.base_url + next_page


class Yandex:
    base_url = 'https://yandex.ru'
    start_url = 'https://yandex.ru/search/?lr=10838&text='

    def start_point(self, query):
        return self.start_url + quote(query)

    @staticmethod
    def get_results(soup):
        results_div = soup.find('div', class_='content__left')
        results_list = results_div.find_all('a', class_='link_cropped_no')
        results = []
        for res in results_list:
            results.append(
                {
                    'title': res.find('div', class_='organic__url-text').text,
                    'link': res['href']
                }
            )
        return results

    def next_page_url(self, soup):
        try:
            navigation = soup.find('div', class_='pager')
            page_items = navigation.find('div', class_='pager__items')
            next_page = page_items.find_all('a')[-1]['href']
            return self.base_url + next_page
        except AttributeError:
            raise PermissionError('Похоже, что запрос заблокирован')
