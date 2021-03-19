from rest_framework.serializers import ModelSerializer, ReadOnlyField
from accounts.models import SearchTagList, SearchAccountList

class TagListSerializer(ModelSerializer):
    class Meta:
        model = SearchTagList
        fields = ['id', 'name']


class AccountListSerializer(ModelSerializer):
    class Meta:
        model = SearchAccountList
        fields = ['id', 'name']