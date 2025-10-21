import os
import re

from django.http import JsonResponse, FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import (
    TemplateView,
    DetailView,
    ListView,
    View,
)
from django.conf import settings

from .models import (
    News, Partner, PracticeCategory, PracticeInstance,
    Review, ServiceCategory, Service, Client, Article, Video, SiteConfig
)

# === СЛУЖЕБНЫЕ ФУНКЦИИ ===

def download_resume(request, file_path):
    """Отдаёт файл резюме (PDF/DOCX) пользователю."""
    file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_full_path):
        return FileResponse(open(file_full_path, 'rb'))
    raise Http404('Такого файла не существует :(')


def cases_filter_view(request):
    """AJAX-фильтр для страницы практики."""
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


# === МИКСИН ===

class SiteConfigMixin:
    """Добавляет настройки сайта (город, контакты, шаблоны) в контекст."""

    def get_site_config(self):
        config = SiteConfig.objects.first()
        if not config:
            raise ValueError("Не найдена запись SiteConfig — создайте её в админке.")
        return config

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config = self.get_site_config()

        context.update({
            "city_name": dict(SiteConfig.CITY_CHOICES).get(config.city),
            "phone": config.phone,
            "phone_display": config.phone_display,
            "address": config.address,
            "map_link": config.map_link,
            "email": config.email,
            "telegram_link": config.telegram_link,
            "instagram_link": config.instagram_link,
            "banner_template": config.banner_template,
            "menu_advocates_template": config.menu_advocates_template,
            "reviews_link": config.reviews_link or "#",
            "team_banner": config.team_banner,
        })
        return context


# === ГЛАВНАЯ СТРАНИЦА ===

class HomePageView(SiteConfigMixin, TemplateView):
    """Главная страница."""
    template_name = "homeapp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Главная страница",
            "user": self.request.session.get("username"),
            "News": News.published.all(),
            "partners": Partner.objects.all(),
            "reviews": Review.objects.filter(is_active=True),
            "clients": Client.objects.exclude(logo="").exclude(logo__isnull=True),
        })
        return context


# === КОМАНДА ===

class TeamView(SiteConfigMixin, TemplateView):
    template_name = 'homeapp/team.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Команда',
            'user': self.request.session.get('username'),
            'partners': Partner.objects.all(),
        })
        return context


# === ТАРИФЫ ===

class TariffsView(SiteConfigMixin, TemplateView):
    template_name = 'homeapp/tariffs.html'
    extra_context = {'title': 'Онлайн консультации'}


# === ПРОЦЕДУРНЫЕ СТРАНИЦЫ ===

class ProcedurePageView(SiteConfigMixin, TemplateView):
    """Базовый класс для страниц процедуры."""
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            'user': self.request.session.get('username'),
        })
        return context


class RabotaemView(ProcedurePageView):
    template_name = 'homeapp/procedure/rabotaem.html'
    title = 'Как мы работаем'


class PolnomochiyaView(ProcedurePageView):
    template_name = 'homeapp/procedure/polnomochiya.html'
    title = 'Полномочия адвоката'


class TaynaView(ProcedurePageView):
    template_name = 'homeapp/procedure/tayna.html'
    title = 'Адвокатская тайна'


class SoglashenieView(ProcedurePageView):
    template_name = 'homeapp/procedure/soglashenie.html'
    title = 'Соглашение и ордер'


class VariantyView(ProcedurePageView):
    template_name = 'homeapp/procedure/varianty.html'
    title = 'Варианты вознаграждения'


class PrivicyView(ProcedurePageView):
    template_name = 'homeapp/privicy.html'
    title = 'Политика конфиденциальности'


# === ПРАКТИКА ===

class PracticesView(SiteConfigMixin, TemplateView):
    template_name = 'homeapp/practices.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Практика адвокатов',
            'practice_categories': PracticeCategory.objects.all(),
            'partners': Partner.objects.all(),
            'practice_instances': PracticeInstance.objects.all(),
            'user': self.request.session.get('username'),
        })
        return context


class PracticeDetailView(SiteConfigMixin, DetailView):
    model = PracticeInstance
    template_name = 'homeapp/practice_detail.html'
    context_object_name = 'practice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        context["meta"] = self.object.get_meta()
        return context


# === УСЛУГИ ===

class ServiceListView(SiteConfigMixin, TemplateView):
    template_name = "homeapp/services/service_list.html"

    def get(self, request, audience):
        if audience not in ['individual', 'legal']:
            raise Http404("Тип аудитории не найден")

        categories = ServiceCategory.objects.filter(audience=audience).order_by("order")
        title = "Услуги для физических лиц" if audience == "individual" else "Услуги для юридических лиц"
        return self.render_to_response({
            "categories": categories,
            "audience": audience,
            "title": title,
            "meta": {
                "title": title,
                "description": "Список юридических услуг, предоставляемых нашей командой.",
                "keywords": "услуги, юридические услуги, консультации",
            }
        })


class ServiceDetailView(SiteConfigMixin, DetailView):
    model = Service
    template_name = "homeapp/services/service_detail.html"
    context_object_name = "service"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        context["meta"] = self.object.get_meta()
        return context


# === НОВОСТИ ===

class NewsListView(SiteConfigMixin, ListView):
    model = News
    queryset = News.published.all()
    template_name = "homeapp/press/article_news_list.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Новости",
            "section_title": "Новости и публикации",
            "detail_url_name": "homeapp:news_detail",
            "meta": {
                "title": "Новости",
                "description": "Последние новости и обновления нашей компании",
                "keywords": "новости, публикации, события",
            },
        })
        return context


class NewsDetailView(SiteConfigMixin, DetailView):
    model = News
    template_name = "homeapp/news_detail.html"
    context_object_name = "news_obj"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        context["meta"] = self.object.get_meta()
        return context


# === ПРОЧЕЕ ===

class ReviewListView(SiteConfigMixin, ListView):
    model = Review
    template_name = 'homeapp/reviews.html'
    context_object_name = 'reviews'
    queryset = Review.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Отзывы"
        context["meta"] = {
            "title": "Отзывы клиентов",
            "description": "Отзывы клиентов о нашей работе и результатах",
            "keywords": "отзывы, доверие, клиенты",
        }
        return context


class ClientListView(SiteConfigMixin, ListView):
    model = Client
    template_name = 'homeapp/client_list.html'
    context_object_name = 'clients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Клиенты"
        context["meta"] = {
            "title": "Наши клиенты",
            "description": "Компании и организации, с которыми мы работаем",
            "keywords": "клиенты, бизнес, кейсы",
        }
        return context


class ArticleListView(SiteConfigMixin, ListView):
    model = Article
    queryset = Article.objects.filter(is_active=True)
    template_name = "homeapp/press/article_news_list.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Статьи",
            "section_title": "Статьи",
            "detail_url_name": "homeapp:article_detail",
            "meta": {
                "title": "Полезные статьи",
                "description": "Публикации и статьи наших адвокатов",
                "keywords": "статьи, публикации, юридические советы",
            },
        })
        return context


class ArticleDetailView(SiteConfigMixin, DetailView):
    model = Article
    template_name = "homeapp/article_detail.html"
    context_object_name = "article"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        context["meta"] = self.object.get_meta()
        return context


class VideoListView(SiteConfigMixin, ListView):
    model = Video
    queryset = Video.objects.filter(is_active=True)
    template_name = "homeapp/press/video_list.html"
    context_object_name = "videos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Видео"
        context["meta"] = {
            "title": "Юридические видео",
            "description": "Видео с юридическими советами и примерами практики",
            "keywords": "видео, адвокат, практика",
        }
        return context
