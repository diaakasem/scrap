from pygoogle import pygoogle


def google_scrape(query):
    g = pygoogle(query)
    g.pages = 5
    print '*Found %s results*' % (g.get_result_count())
    urls = g.get_urls()
    print urls

if __name__ == '__main__':
    links = google_scrape('blah')
