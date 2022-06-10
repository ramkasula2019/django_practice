import re
from urllib import response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer, PasswordSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework.schemas import AutoSchema
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework import permissions
import json
from json import JSONEncoder
from rest_framework import viewsets
from rest_framework import views
from rest_framework import authentication, permissions
from django.shortcuts import get_object_or_404
# class SnippetList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]

#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()  
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GuideRequestView(views.APIView):
    """
    {"cockpits":[{"id":0,"cms_provider":{"values":["1215153929"],"inverted":false,"and":false,"count":1},"year":154,"grainsMapped":{"main":["cms_provider"]},"grains":["cms_provider"]},{"id":1,"peer_type":{"values":["45","164","244","251","312"],"inverted":true,"and":false,"count":5},"year":154,"grainsMapped":{"main":["peer_type"]},"grains":["peer_type"]}],"controls":{"volume_actual":"1","value_labels":"1","color_by":"0"},"additional":{}}
    """
    
    def post(self, request):                                 
        ## find response attribute
        response=Response(request.data)
        
        data = {'data':request.data, 
                'method':request.method, 
                'content_type':request.content_type,
                'auth':request.auth,
                'stream':request.stream,
                'username':request.user.username,
                'session':request.session,
                'meta':request.META.keys(),
                'res_status_code':response.status_code,
                'res_data':response.data
                }
        return Response(data )

    def get(self, request):
        # for this to work need to pass query param in url itself. it is like get method
        # http://127.0.0.1:8001/hi/?cockpits=test  
        # https://stackoverflow.com/questions/15770488/return-the-current-user-with-django-rest-framework (to print request.user)      
        param = self.request.query_params.get('cockpits','no_request_param')
        user = request.user
        data = {'param':param, 'username': user.username,}  
 
        return Response(data)

class EmployeeEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

# django api guide - 3
class ListUsers(views.APIView):
    permission_classes= [permissions.IsAdminUser]
    # authentication_classes=[authentication.TokenAuthentication]

    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view. (by i80430)
    """
    def get(self, request, format = None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})


# the following define decorator attribut and similar as above class
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAdminUser])
def list_user_fn_based(request):
    usernames = [user.username for user in User.objects.all()]
    return Response(usernames)



class CustomAutoSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        # override view introspection here...
        pass

@api_view(['GET'])
@schema(CustomAutoSchema())
def test_schema_view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})


## Generic
# Note we can change UserList as any class name.
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset() # why get_query_set() method because  it Defaults to returning the queryset specified by the queryset attribute.


        #need to add context while instantiting
        #https://stackoverflow.com/questions/57397471/how-to-fix-this-error-hyperlinkedidentityfield-requires-the-request-in-the-se
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

# this will also work
class OnlyUserListTest(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]



class UserListTest(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset =self.queryset
        # this class is to test difference between self.queryset or self.get_queryset() method. some caching issue 
        #so we used .all()
        queryset = self.queryset.all()


        #need to add context while instantiting
        #https://stackoverflow.com/questions/57397471/how-to-fix-this-error-hyperlinkedidentityfield-requires-the-request-in-the-se
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)



class UserListOverrideQueryset(generics.ListCreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(username=user)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset() # note we override default to get only user with requiresing i80430 only


        #need to add context while instantiting
        #https://stackoverflow.com/questions/57397471/how-to-fix-this-error-hyperlinkedidentityfield-requires-the-request-in-the-se
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)



## custom mixing
class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class RetrieveUserView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ['pk','username']




######## VIEWSETS ###############
class TestUserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    

    
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user,context={'request': request})
        return Response(serializer.data)

# mark extra action viewsets  

########### not working
class ExtraActionUserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().filter(username='i80430').order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)