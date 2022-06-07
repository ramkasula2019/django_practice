import re
from urllib import response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework import permissions
import json
from json import JSONEncoder
from rest_framework import viewsets
from rest_framework import views

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

class GuideRequestViewSet(views.APIView):
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