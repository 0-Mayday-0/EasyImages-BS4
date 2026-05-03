
from crawl import Crawler
import string
import colorama
from icecream import ic

class Menu:
    def __init__(self) -> None:
        colorama.init()
        self._crawler: Crawler = Crawler('http://www.pesmitidelcalcio.com/')

        self._allowed_characters: list[str] = list(string.ascii_letters)
        self._allowed_characters.extend(list(string.digits))
        self._allowed_characters.append('ô')
        self._allowed_characters.append('\'')
        self._allowed_characters.append(' ')

    def mainloop(self) -> None:
        while True:
            raw_input: str = input(f'{colorama.Fore.BLUE}Enter year and country to search: ')

            valid: tuple[str, str] | None = self._verify_input(raw_input)

            if not valid:
                print(f'{colorama.Fore.RED}Invalid character in input.')
            else:
                self._crawler.lookup_era(valid[0], valid[1])

    def _verify_input(self, raw_input: str) -> tuple[str, str] | None:

        for c in raw_input:
            if c not in self._allowed_characters:
                return None
            if c.isdigit():
                country_and_year: tuple[str, str] = (raw_input[:raw_input.index(c)], raw_input[raw_input.index(c):])
                return country_and_year

def main() -> None:
    menu: Menu = Menu()

    menu.mainloop()

if __name__ == '__main__':
    main()

