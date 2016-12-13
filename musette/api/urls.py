from rest_framework import routers
from musette.api import views

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/users', views.UserViewSet)
router.register(r'api/categories', views.CategoryViewSet)
router.register(r'api/forums', views.ForumViewSet)
router.register(r'api/topics', views.TopicViewSet)
router.register(r'api/registers', views.RegisterViewSet)
router.register(r'api/comments', views.CommentViewSet)
router.register(r'api/profiles', views.ProfileViewSet)
