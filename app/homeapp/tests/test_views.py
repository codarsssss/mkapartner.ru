import pytest
from django.urls import reverse
from homeapp.models import *


@pytest.mark.django_db
def test_index_view(client):
    """Тест главной страницы: проверка ответа 200."""
    response = client.get(reverse('homeapp:index'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_team_view(client):
    """Тест страницы команды: создаётся один партнёр и проверяется загрузка страницы."""
    Partner.objects.create(name="Иван", my_order=1, context="Описание", min_context1="Кратко", photo="path/test.jpg")
    response = client.get(reverse('homeapp:team'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_news_detail_view(client):
    """Тест детальной страницы новости по slug."""
    news = News.objects.create(title="Новость", slug="novost", text="Текст", status="Да")
    response = client.get(reverse('homeapp:news_detail', args=[news.slug]))
    assert response.status_code == 200
    assert news.title in response.content.decode()


@pytest.mark.django_db
def test_news_list_view(client):
    """Тест списка новостей: отображение опубликованных новостей."""
    News.objects.create(title="Новость", slug="novost", text="Текст", status="Да")
    response = client.get(reverse("homeapp:news_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_article_detail_view(client):
    """Тест детальной страницы статьи по slug."""
    article = Article.objects.create(title="Статья", slug="statya", content="Контент", published_at="2024-01-01")
    response = client.get(reverse("homeapp:article_detail", args=[article.slug]))
    assert response.status_code == 200
    assert article.title in response.content.decode()


@pytest.mark.django_db
def test_practice_detail_view(client):
    """Тест детальной страницы случая практики."""
    category = PracticeCategory.objects.create(title="Уголовное")
    partner = Partner.objects.create(name="Адвокат", my_order=1, context="Описание", min_context1="Кратко", photo="test.jpg")
    instance = PracticeInstance.objects.create(
        category=category, title="Дело", partner=partner,
        circumstances="Обст.", lawyer_position="Позиция", outcome="Результат"
    )
    response = client.get(reverse("homeapp:practice_detail", args=[instance.pk]))
    assert response.status_code == 200
    assert instance.title in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize("audience", ["individual", "legal"])
def test_service_list_view(client, audience):
    """Проверка списка услуг для обеих аудиторий: физ и юр лица."""
    ServiceCategory.objects.create(title="Категория", audience=audience)
    response = client.get(reverse("homeapp:service_list", args=[audience]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_service_detail_view(client):
    """Тест детальной страницы конкретной услуги."""
    category = ServiceCategory.objects.create(title="Физ", audience="individual")
    service = Service.objects.create(title="Консультация", slug="kons", category=category)
    response = client.get(reverse("homeapp:service_detail", args=[service.slug]))
    assert response.status_code == 200
    assert service.title in response.content.decode()


@pytest.mark.django_db
def test_article_list_view(client):
    """Тест списка статей в пресс-центре."""
    Article.objects.create(title="Заголовок", slug="test", content="Текст", published_at="2024-01-01")
    response = client.get(reverse("homeapp:article_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_video_list_view(client):
    """Тест страницы со списком видео в пресс-центре."""
    Video.objects.create(title="Видео", url="https://youtu.be/dQw4w9WgXcQ", published_at="2024-01-01")
    response = client.get(reverse("homeapp:video_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_review_list_view(client):
    """Тест страницы отзывов: отображение активных отзывов."""
    Review.objects.create(author_name="Клиент", content="Хорошо", is_active=True)
    response = client.get(reverse("homeapp:reviews"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_client_list_view(client):
    """Тест страницы клиентов: создаётся один клиент и проверяется загрузка."""
    category = ServiceCategory.objects.create(title="Физ", audience="individual")
    service = Service.objects.create(title="Услуга", slug="slug", category=category)
    Client.objects.create(name="Компания", service=service)
    response = client.get(reverse("homeapp:client_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_tariffs_view(client):
    """Тест страницы онлайн консультаций."""
    response = client.get(reverse('homeapp:tariffs'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_procedure_pages(client):
    """Цикл по всем процедурным страницам: проверка кодов ответа."""
    paths = [
        'rabotaem', 'polnomochiya', 'tayna',
        'soglashenie', 'varianty', 'privicy'
    ]
    for path in paths:
        response = client.get(reverse(f'homeapp:{path}'))
        assert response.status_code == 200


@pytest.mark.django_db
def test_practices_view(client):
    """Тест страницы списка практик (без фильтрации)."""
    PracticeCategory.objects.create(title="Уголовные дела")
    response = client.get(reverse('homeapp:cases'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_cases_filter_view(client):
    """Тест фильтрации практик по категории и партнёру через AJAX-запрос."""
    category = PracticeCategory.objects.create(title="Уголовка")
    partner = Partner.objects.create(name="Адвокат", my_order=1, context="Описание", min_context1="Кратко", photo="p.jpg")
    PracticeInstance.objects.create(
        category=category, partner=partner,
        title="Случай", circumstances="...", lawyer_position="...", outcome="..."
    )
    response = client.get(reverse("homeapp:cases_filter"), {
        "category": category.id,
        "partner": partner.id
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    assert response.status_code == 200
    assert "Случай" in response.json()['html']


@pytest.mark.django_db
def test_robots_txt(client):
    """
    проверяется, что он возвращается с кодом 200 и содержит директиву User-agent.
    """
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert "User-agent" in response.content.decode()


@pytest.mark.django_db
def test_sitemap_xml(client):
    """
    проверяется наличие основных тегов XML-карты сайта (<urlset>, <loc>), что подтверждает корректную генерацию.
    """
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert b"<urlset" in response.content
    assert b"<loc>" in response.content