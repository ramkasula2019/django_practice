from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views
from django.contrib.auth.models import User
from snippets.serializers import SnippetSerializer, UserSerializer
#https://stackoverflow.com/questions/71564307/converting-to-using-url-router-is-causing-a-improperlyconfigured-exception
# there was basename="snippets" in tutorial that is why we are getting issue, it should be singular
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet,basename="snippet")
router.register(r'users', views.UserViewSet, basename="user")
router.register(r'test_user_viewset_router', views.TestUserViewSet, basename='user')

# router.register(r'test_requests', views.TestRequestViewSet, basename="test_requests")

# this gives url like http://127.0.0.1:8001/testing_router/recent_users/ or http://127.0.0.1:8001/1/set_password/
router.register(r'testing_router', views.ExtraActionUserViewSet, basename='user')

urlpatterns = router.urls

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('api_request/', views.GuideRequestView.as_view()),
    path('user_list/',views.ListUsers.as_view()),
    path('hello_world/',views.hello_world),
    path('user_list_fn/', views.list_user_fn_based),
    path('test_schema_view/', views.test_schema_view),
    # both users_test commented and uncomment are fine url
    # path('users_test/', views.UserList.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-list')
    path('users_test/', views.UserList.as_view()),
    path('users_list_test/', views.UserListTest.as_view()),
    path('users_list_override/', views.UserListOverrideQueryset.as_view()),
    path('only_users_list_test/', views.OnlyUserListTest.as_view()),

    path('custom_mixing/<int:pk>/', views.RetrieveUserView.as_view()), # why this not working
    path('custom_mixing/<int:pk>/<username>/', views.RetrieveUserView.as_view()),
    # http://127.0.0.1:8001/custom_mixing/1/i80430/

    ## viewsets url --typically we won't do this rather register in default router
    path(
        'test_user_viewset/<int:pk>/',
        views.TestUserViewSet.as_view({'get': 'retrieve'}),
        name='user-detail',
    ),
    path(
        'test_user_viewset/',
        views.TestUserViewSet.as_view({'get': 'list'}),
        name='user-list',
    ),
# it seems little working but not  need to kept on top register part
    path(
        'user_set_password/<int:pk>/',
        views.ExtraActionUserViewSet.as_view({'post': 'set_password'}),
        name='user-list',
    ),
    path(
        'recent_user/',
        views.ExtraActionUserViewSet.as_view({'get': 'recent_users'}),
        name='recent_user',
    ),
# render user list 'revisti for template .html so error
    path('render_user_html/<int:pk>/',views.RendererUserDetail.as_view()),
# http://127.0.0.1:8001/render_user_html/1/
    path('download_xlsx/<int:pk>/',views.MyExampleViewSet.as_view({'get':'list'}))
    
]