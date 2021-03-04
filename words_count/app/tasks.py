from __future__ import absolute_import, unicode_literals

import json
import urllib
from urllib.request import Request, urlopen

from .models import Tasks, Results
from bs4 import BeautifulSoup

from words_count.celery import app
import requests
from django.conf import settings


@app.task
def word_count(pk):
    task = Tasks.objects.filter(pk=pk).first()
    task.task_status = 2 # 'PENDING'
    task.save()
    address = task.address

    word = 'python'
    count = 0

    try:
        req = Request(address)
        html = urlopen(req, timeout=10).read()

        soup = BeautifulSoup(html)
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk).lower()

        count = text.count(word)

        result = Results(address=address, words_count=count, http_status_code=200)

    except urllib.error.HTTPError as e:
        http_status_code = e.code
        result = Results(address=address, http_status_code=http_status_code)
    except urllib.error.URLError as e:
        about_error = e.reason
        result = Results(address=address, about_error=about_error)

    requests.post("http://nsqd:4151/pub?topic=bg_worker",
                  json={"address": address, "word": word, "words_count": count, "http_status_code": result.http_status_code, "about_error": str(result.about_error)})

    task = Tasks.objects.get(pk=pk)
    task.task_status = 3 #'FINISHED'
    task.save()



