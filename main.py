from collect_html_pages import CITIES, get_source_html
from parse_data import get_page_in_html, parsing, parse_to_json


def main():
    url = (
        'https://online.metro-cc.ru/virtual/produkty-halyal-31183?from=under_search'
    )

    for city in CITIES:
        # get_source_html(
        #     url,
        #     city,
        # )

        soup = get_page_in_html(
            f'/Users/faithk/Documents/pythonProject/html_pages/{city}/index_{city}.html'
        )
        parse_to_json(parsing(soup), city)


if __name__ == '__main__':
    main()
