import requests
import bs4
from collections import defaultdict


def default_value():
    return 0


def grab_tags():
    res = requests.get("http://quotes.toscrape.com")
    soup = bs4.BeautifulSoup(res.content, "lxml")
    # grab the authors
    author_tags = soup.select(".author")
    authors = set()
    for tag in author_tags:
        authors.add(tag.text)
    print(f"All the authors in the page: {authors}")
    quote_tags = soup.select(".text")
    quotes = list()
    for tag in quote_tags:
        quotes.append(tag.text)
    print(f"All the quotes in the page: {quotes}")
    tag_counts = defaultdict(default_value)
    all_tags = soup.select(".tag")
    for tag in all_tags:
        tag_counts[tag.text] += 1
    all_tags = dict(sorted(tag_counts.items(), key=lambda item: item[1]))
    print("Top 10 tags: ")
    for i in range(10):
        print(all_tags.popitem()[0])
    page_pattern = "http://quotes.toscrape.com/page/{}/"
    authors = set()
    index = 1
    try:
        while True:
            page_url = page_pattern.format(index)
            res = requests.get(page_url)
            soup = bs4.BeautifulSoup(res.content, "lxml")
            author_tags = soup.select(".author")
            quote_tags = soup.select(".quote")
            if len(quote_tags) != 0:
                for tag in author_tags:
                    authors.add(tag.text)
                index += 1
            else:
                break
    except:
        print(f"the page does not exist: {page_pattern.format(index)}")
    finally:
        print(f"all unique authors of the whole pages: {authors}")


if __name__ == "__main__":
    grab_tags()
    pass
