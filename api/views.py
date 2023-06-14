from rest_framework.decorators import action
from rest_framework.response import Response

from api.mixins import CreateUpdateDestroy, ListRetrieve
from api.serializers import (ClientSerializer, MailingListSerializer,
                             MailSerializer)
from mailing_list.models import Client, Mail, MailingList, StatusChoice
from mailing_list.tasks import cancel_task


class ClientViewSet(CreateUpdateDestroy):
    """Viewset for Client model"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingListViewSet(CreateUpdateDestroy):
    """Viewset for MailingList model"""
    queryset = MailingList.objects.all()
    serializer_class = MailingListSerializer

    @action(detail=False, methods=['get'])
    def general_statistics(self, request):
        """Method for general statistics"""
        statistics = {
            'Mailing lists count': MailingList.objects.count(),
            'Mails': {
                status.value: Mail.objects.filter(
                    status=status.value
                ).count() for status in StatusChoice},
        }
        return Response(statistics)

    @action(detail=True, methods=['get'])
    def detailed_statistics(self, request, pk=None):
        """Method for detailed statistics"""
        mailing_list = self.get_object()
        statistics = {
            'Mailing list': self.serializer_class(mailing_list).data,
            'Mails': {
                status.value: Mail.objects.filter(
                    mailing_list=mailing_list, status=status.value
                ).count() for status in StatusChoice},
        }
        return Response(statistics)

    def perform_destroy(self, instance):
        mail_ids = list(
            Mail.objects.filter(
                mailing_list=instance.id
            ).values_list('id', flat=True)
        )
        cancel_task(mail_ids=mail_ids)
        instance.delete()


class MailViewSet(ListRetrieve):
    """Viewset for Mail model"""
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
