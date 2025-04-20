import os
import asyncio

from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, FileResponse, Http404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import News, Partner, PracticeCategory, PracticeInstance, Review
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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


# def zashchita_view(request: HttpRequest):
#     context = {
#         'title': 'Защита при уголовном преследовании',
#         'user': request.session.get('username')
#     }
#
#     return render(request, 'homeapp/practices/zashchita.html', context=context)


# def business_view(request: HttpRequest):
#     context = {
#         'title': 'Уголовно-правовая защита бизнеса',
#         'user': request.session.get('username')
#
#     }
#
#     return render(request, 'homeapp/practices/business.html', context=context)


# def antikorruptsionnoe_view(request: HttpRequest):
#     context = {
#         'title': 'Антикоррупционный комплайнс',
#         'user': request.session.get('username')
#     }
#
#     return render(request, 'homeapp/practices/korporativnaya.html', context=context)


# def semeynaya_view(request: HttpRequest):
#     context = {
#         'title': 'Семейная практика',
#         'user': request.session.get('username')
#     }
#
#     return render(request, 'homeapp/practices/semeynaya.html', context=context)


# def zemelnaya_view(request: HttpRequest):
#     context = {
#         'title': 'Земельная практика',
#         'user': request.session.get('username')
#     }
#
#     return render(request, 'homeapp/practices/zemelnaya.html', context=context)


# def nalogovaya_view(request: HttpRequest):
#     context = {
#         'title': 'Налоговая практика',
#         'user': request.session.get('username')
#     }
#
#     return render(request, 'homeapp/practices/nalogovaya.html', context=context)


# def mediatsiya_view(request: HttpRequest):
#     context = {
#         'title': 'Медиация',
#         'user': request.session.get('username')
#     }
#
#     return render(request, 'homeapp/practices/mediatsiya.html', context=context)


# def it_ip_praktika_view(request: HttpRequest):
#     context = {
#         'title': ' IT/ IP практика',
#         'user': request.session.get('username')
#     }
#
#     return render(request, 'homeapp/practices/it_ip_praktika.html', context=context)


# def korporativnaya_view(request: HttpRequest):
#     context = {
#         'title': 'Корпоративная практика',
#         'user': request.session.get('username')
#     }
#
#     return render(request, 'homeapp/practices/korporativnaya.html', context=context)


# def meditsinskoe_view(request: HttpRequest):
#     context = {
#         'title': 'Медицинское право',
#         'user': request.session.get('username')
#     }
#
#     return render(request, 'homeapp/practices/meditsinskoe.html', context=context)


# def arbitrazhnaya_view(request: HttpRequest):
#     context = {
#         'title': 'Арбитражная практика',
#         'user': request.session.get('username')
#     }
#
#     return render(request, 'homeapp/practices/arbitrazhnaya.html', context=context)


# def sanktsionnaya_view(request: HttpRequest):
#     context = {
#         'title': 'Санкционная практика',
#         'user': request.session.get('username')
#     }
#
#     return render(request, 'homeapp/practices/sanktsionnaya.html', context=context)



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


def get_individual_service_list(request: HttpRequest):
    context = {
        'title': 'Услуги для физических лиц',
        'user': request.session.get('username')
    }
    return render(request,
                  'homeapp/services/individuals/individual_service_list.html', context=context)

def get_legal_service_list(request: HttpRequest):
    context = {
        'title': 'Услуги для юридических лиц',
        'user': request.session.get('username')
    }

    return render(request, 'homeapp/services/legals/legal_service_list.html', context=context)

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

def get_insolvecy_support_detail(request: HttpRequest):
    context = {
        'title': 'Сопровождение банкротства',
        'user': request.session.get('username'),
    }
    return render(request, 'homeapp/services/legals/insolvency_support.html', context=context)

def get_complex_support_detail(request: HttpRequest):
    context = {
        'title': 'Комплексное сопровождение',
        'user': request.session.get('username'),
    }
    return render(request, 'homeapp/services/legals/complex_support.html', context=context)

def get_criminal_defense_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Уголовные дела)',
        'user': request.session.get('username'),
    }
    return render(request, 'homeapp/services/individuals/criminal_defense.html', context=context)

def get_civil_defense_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Гражданские дела)',
        'user': request.session.get('username'),
    }

    return render(request, 'homeapp/services/individuals/civil_defense.html', context=context)

def get_inheritance_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Дела по наследованию)',
        'user': request.session.get('username'),
    }

    return render(request,
                  'homeapp/services/individuals/inheritance_service.html', context=context)

def get_migration_detail(request: HttpRequest):
    context = {
        'title': 'Адвокаты (Миграционным дела)',
        'user': request.session.get('username'),
    }

    return render(request, 'homeapp/services/individuals/migration_service.html', context=context)

def get_traffic_accident_detail(request: HttpRequest):
    context = {
        'title': 'Автоюрист (ДТП)',
        'user': request.session.get('username'),
    }

    return render(request,
                  'homeapp/services/individuals/traffic_accident_service.html', context=context)

def get_license_revocation_detail(request: HttpRequest):
    context = {
        'title': 'Автоюрист (Лишение водительского удостоверения)',
        'user': request.session.get('username'),
    }

    return render(request,
                  'homeapp/services/individuals/license_revocation_service.html', context=context)

def get_family_matters_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Семейные дела)',
        'user': request.session.get('username'),
    }

    return render(request,
                  'homeapp/services/individuals/family_matters_service.html', context=context)

def get_individual_bankruptcy_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Банкротство физичеких лиц)',
        'user': request.session.get('username'),
    }

    return render(request,
                  'homeapp/services/individuals/individual_bankruptcy_service.html', context=context)
    
def get_consumer_protection_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Защита прав потребителя)',
        'user': request.session.get('username'),
    }

    return render(request,
                  'homeapp/services/individuals/consumer_protection_service.html', context=context)

def get_land_disputes_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Земельные споры)',
        'user': request.session.get('username'),
    }

    return render(request,
                  'homeapp/services/individuals/land_disputes_service.html', context=context)

def get_debt_recovery_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Взыскание долгов)',
        'user': request.session.get('username'),
    }

    return render(request,
                  'homeapp/services/individuals/debt_recovery_service.html', context=context)

def get_medical_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Возмещение вреда здоровью)',
        'user': request.session.get('username'),
    }

    return render(request, 'homeapp/services/individuals/medical_service.html', context=context)

def get_enforcement_lawyer_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Исполнительного производство)',
        'user': request.session.get('username'),
    }

    return render(request,
                  'homeapp/services/individuals/enforcement_lawyer_service.html', context=context)

def get_appeals_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Обжалование решений)',
        'user': request.session.get('username'),
    }

    return render(request, 'homeapp/services/individuals/appeals_service.html', context=context)

def get_administrative_penalties_detail(request: HttpRequest):
    context = {
        'title': 'Адвокат (Административные наказания)',
        'user': request.session.get('username'),
    }

    return render(request,
                  'homeapp/services/individuals/administrative_pinalties_service.html', context=context)

def get_online_consultation_detail(request: HttpRequest):
    context = {
        'title': 'Онлайн консультации',
        'user': request.session.get('username'),
    }

    return render(request,
                  'homeapp/services/individuals/online_consultation_service.html', context=context)


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


class ReviewListView(ListView):
    model = Review
    template_name = 'homeapp/reviews.html'
    context_object_name = 'reviews'
    queryset = Review.objects.filter(is_active=True)
