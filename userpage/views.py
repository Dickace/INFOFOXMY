from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny, IsAdminUser
from .models import Profile, Bracelet
from .serializers import *

User = get_user_model()

@permission_classes([IsAuthenticated])
class CreateProfile(APIView):
    def post(self, request):
        newProfile = ProfileCreateSerializer(data=request.data)
        if newProfile.is_valid():
            newProfile.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class ViewProfile(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            profiles = Profile.objects.select_related('user').filter(user__id=user_id)
            serializer = ProfileViewListSerializer(profiles, many=True)
            return Response(serializer.data)
        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class ProfileDeleteView(APIView):
    def delete(self, request):
        try:
            profile = Profile.objects.get(pk=request.data.id)
            profile.delete()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class InfoBlockCreateView(APIView):
    def post(self, request):
        infoblock = InfoBlockCreateSerializer(data=request.data)
        if infoblock.is_valid():
            print(infoblock.validated_data)
            infoblock.save(profile=request.profile)
            print(infoblock.data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class InfoBlockDeleteView(APIView):
    def delete(self, request, pk):
        try:
            infoblock = InfoBlock.objects.get(pk=pk)
            if request.profile == infoblock.proflie:
                infoblock.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class InfoBlockChangeView(APIView):
    def put(self, request, pk):
        infoblock_ser = InfoBlockCreateSerializer(data=request.data)
        if infoblock_ser.is_valid():
            try:
                infoblock = InfoBlock.objects.filter(pk=pk)
                if request.profile == infoblock[0].profile:
                    infoblock.update(**infoblock_ser.data)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class InfoBlockDetailView(APIView):
    def get(self, request, pk):
        try:
            infoblock = InfoBlock.objects.get(pk=pk)
            serializer = InfoBlockDetailSerializer(infoblock)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([AllowAny])
class InfoBlockListView(APIView):
    def get(self, request):
        try:
            profile_id = int(request.data.get('user'))
            User.objects.get(pk=profile_id)
            infoblocks = InfoBlock.objects.select_related('profile').filter(profile_id=profile_id)
            serializer = InfoBlockDetailSerializer(infoblocks, many=True)
            return Response(serializer.data)
        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([AllowAny])
class InfoBlockListCountView(APIView):
    def get(self, request):
        try:
            profile_id = int(request.data.get('profile_id'))
            start_block_id = int(request.data.get('start_block_id')) + 1
            count = int(request.data.get('count'))
            User.objects.get(pk=profile_id)

            infoblocks = (
                InfoBlock.objects.select_related('profile')
                    .filter(
                    user__id=profile_id,
                    id__gte=start_block_id)
                    .order_by('id')[:count]
            )

            serializer = InfoBlockDetailSerializer(infoblocks, many=True)
            return Response(serializer.data)

        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AccountDefinition(APIView):
    @permission_classes([AllowAny])
    def get(self, request, pk):
        try:
            bracelet = Bracelet.objects.get(id=pk)
            if bracelet.is_activated:
                data = {
                    'unique_code': bracelet.unique_code,
                    'profile_id': bracelet.profile_id,
                }
                return Response(data=data)
            else:
                return Response({'status': 'bracelet is not attached'}, status=status.HTTP_423_LOCKED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class JoinHandler(APIView):
    def post(self, request, pk):
        try:
            unique_code = request.data['unique_code']
            profile_id = int(request.data['profile_id'])
            
            bracelet = Bracelet.objects.get(pk=pk)
            profile = Profile.objects.get(pk=profile_id)
            
            if bracelet.is_activated:
                return Response({"status": "Bracelet already activated"}, status=status.HTTP_400_BAD_REQUEST)
            
            if request.user == profile.user and bracelet.unique_code == unique_code:
                bracelet.profile = profile
                bracelet.is_activated = True
                profile.is_activated = True
                bracelet.save()
                profile.save()
                return Response({"status": "Attached to profile"})
            else:
                return Response({"status": "Invalid unique_code or profile_id"}, status=status.HTTP_400_BAD_REQUEST)
                
        except (KeyError, ValueError, TypeError):
            return Response({"status": "unique_code and profile_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"status": "no such bracelet or profile"}, status=status.HTTP_404_NOT_FOUND)


class createhandler(APIView):
    @permission_classes([IsAdminUser])
    def post(self, request):
        if not request.user.is_superuser:
            return Response(status=403)
            
        handler = CreateBraceletSerializer(data=request.data)
        if handler.is_valid():            
            handler.save()
            return Response(status=201)
        else:
            return Response(handler.errors, status=400)


class deleteHandler(APIView):
    @permission_classes([IsAdminUser])
    def delete(self, request, pk):
        if not request.user.is_superuser:
            return Response(status=403)
        try:
            handler = Bracelet.objects.get(pk=pk)
            handler.delete()
            return Response(status=200)
        except:
            return Response(status=404)
