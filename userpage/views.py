from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny, IsAdminUser
from .models import Profile
from myauth.models import User
from .serializers import *

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
            profile = int(request.data.get('user'))
            User.objects.get(pk=profile)
            profiles = Profile.objects.select_related('user').filter(user__id=profile)
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
            profile = int(request.data.get('user'))
            User.objects.get(pk=profile)
            infoblocks = InfoBlock.objects.select_related('profile').filter(profile_id=profile)
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
            profile = bracelet.objects.get(id=pk)
            if profile.is_activated:
                return Response(data={profile.unique_code, profile.profile_id})
            else:
                return Response({'status': 'get token'})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class JoinHandler(APIView):
    def post(self, request, pk):
        unique_handler = bracelet.objects.get(id=pk)
        serializer = JoinBraceletSerializers(unique_handler)
        code = request.data.get('unique_code')
        if code:
            if code == serializer.data.get('unique_code'):
                user_id = request.profile.id
                unique_handler.profile_id = user_id
                unique_handler.is_activated = True
                unique_handler.save()
                return Response({"status": "Connected"})
            else:
                return Response({"status": "Error"})
        else:
            return Response({"status": "Data Error"})


class createhandler(APIView):
    @permission_classes([IsAdminUser])
    def post(self, request):
        try:
            handler = CreateBraceletSerializers(data=request.data.get())
            if handler.is_valid():
                handler.save()
                return Response(status=201)
            else:
                return Response(status=400)
        except:
            return Response(status=404)


class deleteHandler(APIView):
    @permission_classes([IsAdminUser])
    def delete(self, request, pk):
        try:
            handler = bracelet.objects.get(pk=pk)
            handler.delete()
            return Response(status=201)
        except:
            return Response(status=404)
