from atrax.common.crawl_job import CrawlJob

crawl_job = CrawlJob('siemens17042013')
domain = crawl_job.crawled_urls

attribute_names = set()
next_token = None
try:
    while True:
        query = "select * from `%s`" % domain.name
        items = domain.select(query, next_token=next_token)

        numItems = 0
        for item in items:
            attribute_names.update(item.keys())
            numItems += 1

        if items.next_token is None or numItems == 0:
            break
        next_token = next_token
finally:
    with open('attributes.txt', 'w') as attributes_file:
        for name in attribute_names:
            attributes_file.write(name + '\n')
