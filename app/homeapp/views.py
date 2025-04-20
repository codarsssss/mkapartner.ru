import os
import asyncio

from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, FileResponse, Http404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import News, Partner, PracticeCategory, PracticeInstance, Review, ServiceCategory, Service, Client
from django.conf import settings


def download_resume(request, file_path):
    file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_full_path):
        return FileResponse(open(file_full_path, 'rb'))
    raise Http404('Такого файла не существует :(')


def home_index(request: HttpRequest):
    news = News.published.all()  # Все новости, у которых status = Published
    partners = Partner.objects.all()
    reviews = Review.objects.filter(is_active=True)
    context = {
        'title': 'Главная страница',
        'user': request.session.get('username'),
        'News': news,
        'partners': partners,
        'reviews': reviews,
    }

    return render(request, 'homeapp/index.html', context=context)


def team_view(request: HttpRequest):
    partners = Partner.objects.all()
    context = {
        'title': 'Команда',
        'user': request.session.get('username'),
        'partners': partners,
    }

    return render(request, 'homeapp/team.html', context=context)


def rabotaem_view(request: HttpRequest):
    context = {
        'title': 'Как мы работаем',
        'user': request.session.get('username')
    }

    return render(request, 'homeapp/procedure/rabotaem.html', context=context)


def polnomochiya_view(request: HttpRequest):
    context = {
        'title': 'Полномочия адвоката',
        'user': request.session.get('username')
    }

    return render(request, 'homeapp/procedure/polnomochiya.html', context=context)


def tayna_view(request: HttpRequest):
    context = {
        'title': 'Адвокатская тайна',
        'user': request.session.get('username')
    }

    return render(request, 'homeapp/procedure/tayna.html', context=context)


def soglashenie_view(request: HttpRequest):
    context = {
        'title': 'Соглашение и ордер',
        'user': request.session.get('username')
    }

    return render(request, 'homeapp/procedure/soglashenie.html', context=context)


def varianty_view(request: HttpRequest):
    context = {
        'title': 'Варианты вознагрождения',
        'user': request.session.get('username')
    }

    return render(request, 'homeapp/procedure/varianty.html', context=context)


def privicy_view(request: HttpRequest):
    context = {
        'title': 'Политика конфиденциальности',
        'user': request.session.get('username')
    }

    return render(request, 'homeapp/privicy.html', context=context)


def get_news_list(request: HttpRequest):
    news = News.published.all()
    context = {
        'title': 'Новости',
        'user': request.session.get('username'),
        'News': news,
    }

    return render(request, 'homeapp/news_list.html', context=context)

def news_detail(request, slug):
    news_obj = get_object_or_404(News, slug=slug)
    context = {
        'title': 'Новости',
        'news_obj': news_obj
    }

    return render(request, 'homeapp/news_detail.html', context=context)


def tariffs_view(request: HttpRequest):
    context = {
        'title': 'Онлайн консультации',
        'user': request.session.get('username'),
    }

    return render(request, 'homeapp/tariffs.html', context=context)


def practices_view(request: HttpRequest):
    context = {
        'title': 'Практика адвокатов',
        'practice_categories': PracticeCategory.objects.all(),
        'partners': Partner.objects.all(),
        'practice_instances': PracticeInstance.objects.all(),
        'user': request.session.get('username')
    }
    return render(request, 'homeapp/practices.html', context)

def cases_filter_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        category_id = request.GET.get('category')
        partner_id = request.GET.get('partner')

        queryset = PracticeInstance.objects.all()

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if partner_id:
            queryset = queryset.filter(partner_id=partner_id)

        html = render_to_string('homeapp/partials/_practice_list.html', {'items': queryset})
        return JsonResponse({'html': html})

class PracticeDetailView(DetailView, View):
    model = PracticeInstance
    template_name = 'homeapp/practice_detail.html'
    context_object_name = 'practice'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


def service_list_view(request, audience):
    if audience not in ['individual', 'legal']:
        raise Http404("Тип аудитории не найден")

    categories = ServiceCategory.objects.filter(audience=audience).order_by("order")

    return render(request, "homeapp/services/service_list.html", {
        "categories": categories,
        "audience": audience,
        "title": "Услуги для физических лиц" if audience == "individual" else "Услуги для юридических лиц",
    })


def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, "homeapp/services/service_detail.html", {
        "service": service,
        "title": service.title
    })


class ReviewListView(ListView):
    model = Review
    template_name = 'homeapp/reviews.html'
    context_object_name = 'reviews'
    queryset = Review.objects.filter(is_active=True)


def client_list_view(request):
    clients = Client.objects.all()
    return render(request, 'homeapp/client_list.html', {'clients': clients})
