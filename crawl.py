from bs4.element import Tag
from bs4 import BeautifulSoup
import requests
from icecream import ic
import pyperclip as ppc
import re
import colorama


# noinspection SpellCheckingInspection
class Crawler:
    def __init__(self, base_uri: str) -> None:
        colorama.init(autoreset=True)
        self._base_uri: str = base_uri
        self._eras_ids: list[str] = [str(i) for i in range(48, 57)]
        self._eras_ids.append('123')
        self._eras_keys: list[str] = [str(i) for i in range(30, 100, 10)]
        self._eras_keys.append('0')
        self._eras_keys.append('10')
        self._eras_keys.append('20')

        self._era_to_id: dict[str, str] = {era: fid for era, fid in zip(self._eras_keys, self._eras_ids)}

        self._current_page: int = 1

        self._max_page: int = 4

        self._start_at: int = 0
        self._start_steps: int = 30

    def lookup_era(self, country: str, year: str):
        try:
            assert len(year) == 4

            era: str = str(int(year)%100 - int(year[-1]))

            era_soup: BeautifulSoup = BeautifulSoup(requests.get(f'{self._base_uri}viewforum.php?f={self._era_to_id[era]}').content, 'html.parser')

            self._lookup_pages(country, era, year, era_soup)

        except AssertionError:
            print(f'{colorama.Fore.RED}Year must be a 4 digit integer')

    def _lookup_pages(self, country: str, era: str, year: str, era_soup: BeautifulSoup) -> re.Match | None:
        found: bool = False
        while not found and self._current_page <= self._max_page:
            print(f'{colorama.Fore.YELLOW}Searching page {colorama.Fore.CYAN}{self._current_page}')
            topic_titles = era_soup.find_all('a', {'class' : 'topictitle'})

            for topic in topic_titles:
                found = bool(re.search(f'.*{country}.*{year}.*', topic.text, flags=re.I))
                if found:
                    suffix: list[str] = list(topic['href'])
                    suffix[0] = ''
                    suffix[1] = ''
                    suffix: str = ''.join(suffix)
                    self._lookup_image(f'{self._base_uri}{suffix}')
                    break
                    #ppc.copy(f'{self._base_uri}{}')
                else:
                    continue
            if not found:
                self._current_page += 1
                self._start_at += self._start_steps
                era_soup = BeautifulSoup(requests.get(f'{self._base_uri}viewforum.php?f={self._era_to_id[era]}&start={self._start_at}').text, 'html.parser')
        print(f'{colorama.Fore.RED}Image not found.')

    def _lookup_image(self, url: str) -> None:
        images_soup: BeautifulSoup = BeautifulSoup(requests.get(url).text, 'html.parser')
        image: BeautifulSoup | None = images_soup.find('img', {'src': re.compile('.*/formations/.*')})

        found = bool(image)
        if not found:
            fallback_image = images_soup.find_all('img')[5]['src']
            print(f'{colorama.Fore.GREEN}Copied: {colorama.Fore.BLUE}{fallback_image}')
            ppc.copy(fallback_image)

        elif found:
            ppc.copy(image['src'])
            print(f'{colorama.Fore.GREEN}Copied: {colorama.Fore.BLUE}{image['src']}')

        #elif not found and self._current_page == self._max_page:




def main() -> None:
    c: Crawler = Crawler('http://www.pesmitidelcalcio.com/')

    c.lookup_era('Rusia', '2008')

if __name__ == '__main__':
    main()