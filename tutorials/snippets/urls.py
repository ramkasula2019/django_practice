from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views


#https://stackoverflow.com/questions/71564307/converting-to-using-url-router-is-causing-a-improperlyconfigured-exception
# there was basename="snippets" in tutorial that is why we are getting issue, it should be singular
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet,basename="snippet")
router.register(r'users', views.UserViewSet, basename="user")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]