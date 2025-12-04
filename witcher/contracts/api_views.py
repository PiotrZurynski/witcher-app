from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from .models import Realm, Town, Monster, Contract
from .serializers import RealmSerializer,TownSerializer,MonsterSerializer,ContractSerializer,ContractListSerializer
from django.db.models import Count,Sum
from django.utils import timezone
User = get_user_model()

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def realm_list(request):
    if request.method == 'GET':
        realms = Realm.objects.all()
        serializer = RealmSerializer(realms, many=True)
        return Response(serializer.data)
    if not request.user.has_perm('contracts.add_realm'):
        return Response({'detail': 'Brak uprawnień do tworzenia krain.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = RealmSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def realm_detail(request, pk):
    realm = Realm.objects.get(pk=pk)
    if request.method == 'GET':
        return Response(RealmSerializer(realm).data)
    elif request.method == 'PUT':
        if not request.user.has_perm('contracts.change_realm'):
             return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = RealmSerializer(realm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if not request.user.has_perm('contracts.delete_realm'):
             return Response(status=status.HTTP_403_FORBIDDEN)
        realm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def town_list(request):
    if request.method == 'GET':
        towns = Town.objects.all()
        return Response(TownSerializer(towns, many=True).data)
    if not request.user.has_perm('contracts.add_town'):
        return Response({'detail': 'Brak uprawnień do dodawania miast.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = TownSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def town_detail(request, pk):
    town = get_object_or_404(Town, pk=pk)
    if request.method == 'GET':
        return Response(TownSerializer(town).data)
    elif request.method == 'PUT':
        if not request.user.has_perm('contracts.change_town'):
            return Response({'detail': 'Brak uprawnień do edycji miast.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = TownSerializer(town, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if not request.user.has_perm('contracts.delete_town'):
            return Response({'detail': 'Brak uprawnień do usuwania miast.'}, status=status.HTTP_403_FORBIDDEN)
        town.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def monster_list(request):
    if request.method== 'GET':
        monsters = Monster.objects.all()
        return Response(MonsterSerializer(monsters, many=True).data)
    if not request.user.has_perm('contracts.add_monster'):
        return Response({'detail': 'Brak uprawnień do dodawania potworów.'}, status=status.HTTP_403_FORBIDDEN)
    serializer =MonsterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def monster_detail(request, pk):
    monster= Monster.objects.get(pk=pk)
    if request.method== 'GET':
        return Response(MonsterSerializer(monster).data)
    elif request.method== 'PUT':
        if not request.user.has_perm('contracts.change_monster'):
            return Response({'detail': 'Brak uprawnień do edycji potworów.'}, status=status.HTTP_403_FORBIDDEN)
        serializer =MonsterSerializer(monster, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        if not request.user.has_perm('contracts.delete_monster'):
            return Response({'detail': 'Brak uprawnień do usuwania potworów.'}, status=status.HTTP_403_FORBIDDEN)
        monster.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def validate_contract(data):
    errors = {}
    reward = data.get('reward')
    try:
        if int(reward) < 0:
            errors['reward']='Nagroda nie może być ujemna.'
    except (TypeError, ValueError):
        errors['reward']='Nagroda musi byc integerem'
    for key, Model in [('realm_id', Realm), ('town_id', Town), ('monster_id', Monster)]:
        if not data.get(key):
            errors[key]='Wymagane.'
        elif not Model.objects.filter(pk=data[key]).exists():
            errors[key]='Nieprawidłowe ID.'
    return errors

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def contract_list(request):
    if request.method == 'GET':
        qs = Contract.objects.all().order_by('-time_created')
        return Response(ContractListSerializer(qs, many=True).data)
    data=request.data.copy()
    errs=validate_contract(data)
    if errs:
        return Response(errs,status=status.HTTP_400_BAD_REQUEST)
    owner=request.user
    realm=Realm.objects.get(pk=data['realm_id'])
    town=Town.objects.get(pk=data['town_id'])
    monster=Monster.objects.get(pk=data['monster_id'])
    obj=Contract.objects.create(title=data.get('title', ''),description=data.get('description', ''),realm=realm,town=town,monster=monster,
        currency=data.get('currency', 'KRN'),reward=int(data.get('reward', 0)),state=data.get('state', 'OPN'),owner=owner,
    )
    return Response(ContractSerializer(obj).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def contract_detail(request, pk):
    try:
        obj=Contract.objects.get(pk=pk)
    except Contract.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ContractSerializer(obj).data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def contract_update(request, pk):
    obj=get_object_or_404(Contract,pk=pk)
    if not (request.user.is_staff or obj.owner_id == request.user.id):
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    data=request.data.copy()
    errs=validate_contract(data)
    if errs:
        return Response(errs, status=status.HTTP_400_BAD_REQUEST)

    obj.title=data.get('title', obj.title)
    obj.description=data.get('description', obj.description)
    obj.currency=data.get('currency', obj.currency)
    obj.reward=int(data.get('reward', obj.reward))
    obj.state=data.get('state', obj.state)
    obj.realm=Realm.objects.get(pk=data['realm_id'])
    obj.town=Town.objects.get(pk=data['town_id'])
    obj.monster=Monster.objects.get(pk=data['monster_id'])
    obj.save()
    return Response(ContractSerializer(obj).data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def contract_delete(request, pk):
    obj = get_object_or_404(Contract, pk=pk)
    if not (request.user.is_staff or obj.owner_id == request.user.id):
        return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET'])
def contract_search(request):
    q = request.query_params.get('title', '')
    qs = (Contract.objects.select_related('realm', 'town', 'monster', 'owner').filter(title__icontains=q) if q else
          Contract.objects.select_related('realm', 'town', 'monster', 'owner').all())
    serializer=ContractListSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_contracts(request):
    qs=(Contract.objects.select_related('realm','town','monster','owner').filter(owner=request.user).order_by('-time_created'))
    serializer=ContractListSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def contracts_stats_monthly(request):
    year=int(request.query_params.get('year', timezone.now().year))
    qs=(Contract.objects.filter(time_created__year=year).values('time_created__month').annotate(total=Count('id')).order_by('time_created__month'))
    data=[{'month': r['time_created__month'], 'total': r['total']} for r in qs]
    return Response({'year': year, 'items': data})

@api_view(['GET'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_contracts_summary(request):
    qs=Contract.objects.filter(owner=request.user)
    by_state=(qs.values('state').annotate(total=Count('id')).order_by('state'))
    by_currency=(qs.values('currency').annotate(total_reward=Sum('reward')).order_by('currency'))
    return Response({'counts_by_state': list(by_state),'sum_by_currency': list(by_currency),})