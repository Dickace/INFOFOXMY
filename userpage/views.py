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
        request.data['user'] = request.user.id
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
class InfoBlockCreateView(APIView):
    def post(self, request, profile_pk):
        infoblock = InfoBlockCreateSerializer(data=request.data)
        status_code = status.HTTP_201_CREATED

        if infoblock.is_valid():
            try:
                profile = Profile.objects.get(pk=profile_pk)
                if profile.user == request.user:
                    infoblock.save(profile=profile)
                else:
                    status_code = status.HTTP_403_FORBIDDEN
            except ObjectDoesNotExist:
                status_code = status.HTTP_404_NOT_FOUND
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(status=status_code)


@permission_classes([IsAuthenticated])
class InfoBlockDeleteView(APIView):
    def delete(self, request, profile_pk, block_pk):
        try:
            infoblock = InfoBlock.objects.get(pk=block_pk)
            profile = Profile.objects.get(pk=profile_pk)
            if infoblock.profile != profile:
                raise ObjectDoesNotExist
            if request.user == profile.user:
                infoblock.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class InfoBlockChangeView(APIView):
    def put(self, request, profile_pk, block_pk):
        infoblock_ser = InfoBlockCreateSerializer(data=request.data)
        if infoblock_ser.is_valid():
            try:
                infoblock = InfoBlock.objects.get(pk=block_pk)
                profile = Profile.objects.get(pk=profile_pk)

                if infoblock.profile != profile:
                    raise ObjectDoesNotExist
                if request.user == profile.user:
                    infoblock.title = infoblock_ser.validated_data['title']
                    infoblock.content = infoblock_ser.validated_data['content']
                    infoblock.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)

            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# @permission_classes([AllowAny])
# class InfoBlockDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             infoblock = InfoBlock.objects.get(pk=pk)
#             serializer = InfoBlockDetailSerializer(infoblock)
#             return Response(serializer.data)
#         except ObjectDoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)


class InfoBlockFromProfileListView(APIView):
    @permission_classes([AllowAny])
    def get(self, request, pk):
        try:
            profile = Profile.objects.get(id=pk)
            if profile.is_activated:
                infoblocks = InfoBlock.objects.select_related('profile').filter(profile=profile)
                serializer = InfoBlockDetailSerializer(infoblocks, many=True)
                return Response(serializer.data)
            else:
                return Response(data={'status': 'Профиль не активирован'}, status=status.HTTP_423_LOCKED)
        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        status_code = status.HTTP_200_OK
        try:
            profile = Profile.objects.get(pk=pk)
            if request.user == profile.user:
                profile.delete()
            else:
                status_code = status.HTTP_403_FORBIDDEN
        except ObjectDoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
        return Response(status=status_code)

    def put(self, request, pk):
        try:
            new_profile_name = NewProfileNameSerializer(data=request.data)
            if new_profile_name.is_valid():
                try:
                    profile = Profile.objects.get(pk=pk)
                    if request.user == profile.user:
                        profile.name = new_profile_name.validated_data['name']
                        profile.save()
                        return Response(status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_403_FORBIDDEN)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AccountDefinition(APIView):
    @permission_classes([AllowAny])
    def get(self, request, pk):
        try:
            bracelet = Bracelet.objects.get(id=pk)
            if bracelet.profile:
                data = {
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

            if bracelet.profile:
                return Response({"status": "Bracelet already activated"}, status=status.HTTP_400_BAD_REQUEST)

            if request.user == profile.user and bracelet.unique_code == unique_code:
                bracelet.profile = profile
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


@permission_classes([IsAuthenticated])
class DisconnectBracelet(APIView):
    def post(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)

            if request.user != profile.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            bracelet = Bracelet.objects.get(profile__id=pk, id=request.data['id'])
            bracelet.profile = None
            bracelet.save()
            if Bracelet.objects.select_related('profile').filter(profile__id=profile.id).count() <= 0:
                profile.is_activated = False
                profile.save()
            return Response({"status": "Bracelet disconnected"})

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
