from rest_framework import viewsets
from .models import User, Photo
from .serializers import UserSerializer, PhotoSerializer
from .mixins import RequestLogViewMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class PhotoViewSet(RequestLogViewMixin, viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class UserViewSet(RequestLogViewMixin, viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = User.objects.all()
    serializer_class = UserSerializer