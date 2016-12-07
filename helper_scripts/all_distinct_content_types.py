from atrax.common.crawl_job import CrawlJob

crawl_job = CrawlJob('siemens17042013')

distinct_content_types = set()
next_token = None
try:
    while True:
        query = "select `content-type` from `%s`" % crawl_job.crawled_urls.name
        items = crawl_job.crawled_urls.select(query, next_token=next_token)

        numItems = 0
        for item in items:
            if 'content-type' in item:
                distinct_content_types.add(item['content-type'])
            numItems += 1

        if items.next_token is None or numItems == 0:
            break
        next_token = next_token
finally:
    with open('content_types.txt', 'w') as content_types_file:
        for contentType in distinct_content_types:
            content_types_file.write(contentType + '\n')
