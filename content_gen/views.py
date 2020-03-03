from django.shortcuts import render
from django.http import JsonResponse
from bot.models import *


def content_gen(request):
    if request.method == 'GET':
        qs = QuranOneDayContent.objects.all().order_by('-pk')
        print(qs)
        context = {
            'qs': qs
        }
        print(context)
        return render(request, 'content_gen.html', context)
    else:
        sura = request.POST['sura']
        qs = QuranAyat.objects.filter(sura=sura)
        data = []
        for q in qs:
            data.append({
                'sura': q.sura,
                'ayat': q.ayat,
            })
        response = {
            'data': data
        }
        return JsonResponse(response)
