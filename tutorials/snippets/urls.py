from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('', views.api_root),
    path('snippets/', views.SnippetList.as_view(),name='snippet-list'),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view(),name='snippet-detail'),
    # path('users/', views.UserList.as_view()),
    # path('users/<int:pk>/', views.UserDetail.as_view()),    
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name ='snippet-highlight'),
    path('users/',
        views.UserList.as_view(),
        name='user-list'),
    ## how to make this user-detail works in reverse
    path('users/<int:pk>/',
        views.UserDetail.as_view(),
        name='user-detail'),
    # path('snippets/',
    #     views.SnippetList.as_view(),
    #     name='snippet-list'),
    # # path('snippets/<int:pk>/',
    #     views.SnippetDetail.as_view(),
    #     name='snippet-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)