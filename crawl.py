
from bs4 import BeautifulSoup
import requests
from icecream import ic
import re
import colorama

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

        self._era_to_id: dict[str, str] = {era: id for era, id in zip(self._eras_keys, self._eras_ids)}

    def lookup_era(self, country: str, year: str):
        try:
            assert len(year) == 4

            era = str(int(year)%100 - int(year[-1]))

            era_soup: BeautifulSoup = BeautifulSoup(requests.get(f'{self._base_uri}viewforum.php?f={self._era_to_id[era]}').content, 'html.parser')

            results: re.Match | None = self._lookup_pages(country, era, era_soup)

            print(era_soup.prettify())

        except AssertionError:
            print(f'{colorama.Fore.RED}Year must be a 4 digit integer')


def main() -> None:
    c: Crawler = Crawler('http://www.pesmitidelcalcio.com/')

    c.lookup_era('Japan', '2002')

if __name__ == '__main__':
    main()