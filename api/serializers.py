from rest_framework.serializers import ModelSerializer

from mailing_list.models import Client, Mail, MailingList


class ClientSerializer(ModelSerializer):
    """Serializer for Client model"""

    class Meta:
        model = Client
        fields = (
            'phone_number', 'operator_code', 'tag', 'time_zone',
        )


class MailingListSerializer(ModelSerializer):
    """Serializer for MailingList model"""

    class Meta:
        model = MailingList
        fields = (
            'run_date', 'text', 'client_filter', 'end_date',
        )

    def create(self, validated_data):
        mailing_list = super().create(validated_data)
        mailing_list.start_sending()

        return mailing_list


class MailSerializer(ModelSerializer):
    """Serializer for Mail model"""

    class Meta:
        model = Mail
        fields = (
            'id', 'status', 'client', 'mailing_list', 'sent_at',
        )
