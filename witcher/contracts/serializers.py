from rest_framework import serializers
from .models import Contract, Realm, Town, Monster

class RealmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realm
        fields = ['id', 'name', 'description']

class TownSerializer(serializers.ModelSerializer):
    realm = serializers.StringRelatedField()
    
    class Meta:
        model = Town
        fields = ['id', 'name', 'realm']

class MonsterSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Monster
        fields = ['id', 'name', 'category', 'category_display', 'description']

class ContractSerializer(serializers.ModelSerializer):
    realm = RealmSerializer(read_only=True)
    town = TownSerializer(read_only=True)
    monster = MonsterSerializer(read_only=True)
    owner = serializers.StringRelatedField()
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    state_display = serializers.CharField(source='get_state_display', read_only=True)
    
    class Meta:
        model = Contract
        fields = ['id',
            'title',
            'slug',
            'description',
            'realm',
            'town',
            'monster',
            'currency',
            'currency_display',
            'reward',
            'state',
            'state_display',
            'time_created',
            'owner'
        ]

class ContractListSerializer(serializers.ModelSerializer):
    realm_name = serializers.CharField(source='realm.name', read_only=True)
    town_name = serializers.CharField(source='town.name', read_only=True)
    monster_name = serializers.CharField(source='monster.name', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Contract
        fields = ['id',
                  'title',
                  'slug',
                  'realm_name',
                  'town_name',
                  'monster_name',
                  'reward',
                  'currency',
                  'state',
                  'time_created',
                  'owner_username']