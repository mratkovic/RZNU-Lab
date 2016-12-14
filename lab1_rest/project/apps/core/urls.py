from django.conf.urls import url, include
from rest_framework_nested  import routers
from core.views import PhotoViewSet, UserViewSet

router = routers.DefaultRouter()

router.register(r'photos', PhotoViewSet)
router.register(r'users', UserViewSet)

users_router  = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'photos', PhotoViewSet, base_name='user-photos')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(users_router.urls)),
]
