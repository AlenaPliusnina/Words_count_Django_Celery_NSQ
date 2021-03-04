from datetime import datetime
import nsq

import time

from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .tasks import word_count

from django.shortcuts import render, redirect

from .models import Tasks, Results


def index(request):
    if request.method == 'POST':
        url = request.POST['address']
        task = Tasks(address=url, timestamp=datetime.now(), task_status=1)
        task.save()
        task_for_celery = Tasks.objects.filter(pk=task.pk).first()

        word_count.delay(task_for_celery.pk)

        time.sleep(1)

        return redirect(results)

    return render(request, "index.html")


def handler(message):
    return message.body


@csrf_exempt
def results(request):
    results = Results.objects.all()

    if request.method == "POST":
        Results.objects.create(
                address=request.POST["address"],
                words_count=request.POST["words_count"],
                http_status_code=request.POST.get("http_status_code", False),
                about_error=request.POST.get("about_error", False)

        )
        results = Results.objects.all()
        return render(request, "results.html", context={"results": results})

    return render(request, "results.html", context={"results": results})


