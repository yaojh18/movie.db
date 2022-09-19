from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
import time

# Create your views here.
def admin(request):
    return HttpResponseRedirect('display?type=movie&page=1')

def search(request):
    search_time = time.time()
    if request.GET.get('type'):
        type = request.GET.get('type')
    else:
        type = 'movie'
    search_text = request.GET.get('search_text')
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1
    if (type == 'movie'):
        objects = Movie.objects.filter(Q(title__contains=search_text) | Q(actors__name__contains=search_text)).distinct()
    elif (type == 'actor'):
        objects = Actor.objects.filter(Q(name__contains=search_text) | Q(movies__title__contains=search_text)).distinct()
    else:
        objects = Comment.objects.filter(description__contains=search_text)
    search_num = len(objects)
    paginator = Paginator(objects, 5)
    try:
        objects = paginator.page(page)
        if paginator.num_pages > 5:
            if page - 2 < 1:
                pageRange = list(range(1, 6))
            elif page + 2 > paginator.num_pages:
                pageRange = list(range(paginator.num_pages - 4, paginator.num_pages + 1))
            else:
                pageRange = list(range(page - 2, page + 3))
        else:
            pageRange = paginator.page_range
    except EmptyPage:
        raise Http404("Page not found!")
    search_time = round(time.time() - search_time, 4)
    if (type == 'movie'):
        return render(request, 'movie_search_result.html', locals())
    elif (type == 'actor'):
        return render(request, 'actor_search_result.html', locals())
    else:
        return render(request, 'comment_search_result.html', locals())

def display(request):
    if request.GET.get('type'):
        type = request.GET.get('type')
    else:
        type = 'movie'
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1
    if (type == 'movie'):
        objects = Movie.objects.all()
    else:
        objects = Actor.objects.all()
    paginator = Paginator(objects, 40)
    try:
        results = paginator.page(page)
        if paginator.num_pages > 5:
            if page - 2 < 1:
                pageRange = list(range(1,6))
            elif page + 2 > paginator.num_pages:
                pageRange = list(range(paginator.num_pages - 4, paginator.num_pages + 1))
            else:
                pageRange = list(range(page - 2, page + 3))
        else:
            pageRange = paginator.page_range
    except EmptyPage:
        raise Http404("Page not found!")
    if (type == 'movie'):
        return render(request, 'movie_list.html', locals())
    elif (type == 'actor'):
        return render(request, 'actor_list.html', locals())
    else:
        raise Http404("Page not found!")

def detail(request):
    if request.GET.get('type'):
        type = request.GET.get('type')
    else:
        type = 'movie'
    if request.GET.get('id'):
        id = int(request.GET.get('id'))
    else:
        raise Http404("Page not found!")
    try:
        if (type == 'movie' ):
            object = Movie.objects.get(id=id)
            lst1 = object.actors.all()
            lst2 = object.comments.all()
        else:
            object = Actor.objects.get(id=id)
            lst1 = object.movies.all()
            cnt = {}
            for movie in lst1:
                for actor in movie.actors.all():
                    if (actor!=object):
                        if actor.id in cnt:
                            cnt[actor.id] += 1
                        else:
                            cnt[actor.id] = 1
            res = sorted(cnt.items(), key=lambda item: item[1], reverse=True)
            lst2 = [i[1] for i in res[:10]]
            ids = [Actor.objects.get(id=i[0]) for i in res[:10]]
            lst2 = zip(ids, lst2)
    except ObjectDoesNotExist:
        raise Http404("Page not found!")
    if (type == 'movie'):
        return render(request, 'movie_page.html',locals())
    else:
        return render(request, 'actor_page.html', locals())