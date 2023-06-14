from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ClientViewSet, MailingListViewSet, MailViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'client', ClientViewSet, basename='client')
router.register(r'mailing_list', MailingListViewSet, basename='mailing_list')
router.register(r'mail', MailViewSet, basename='mail')


urlpatterns = [
    path('', include(router.urls)),
]
