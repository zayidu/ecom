from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse 
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import random
import re

# Create your views here.

# generate_session_token
def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)], [str(i) for i in range(10) ]) for _ in range (length))

# signin
@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a Post Request with valid parameters only'})
    
    username = request.POST['email']
    username = request.POST['password']

# validation Part
    if not re.match("([\w\.\-_]+)?\w+@[\w-_]+(\.\w+){1,}", username):
        return JsonResponse({'error':'Enter a Valid Email'})

    if len(password) < 3:
        return JsonResponse({'error':'Password must be more than 3 characters'})

    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(email=username)

        if user.check_password(password):
            usr_dict = UserModel.objects.filter(email=username).values().first()
            usr_dict.pop('password')

            if user.session_token != '0':
                user.session_token = '0'
                user.save()
                return JsonResponse({'error':'Previous Session Exists'})
            
            token = generate_session_token()
            user.session_token = token
            user.save()
            login(request, user)
            return JsonResponse({'token': token, 'user': usr_dict})
        
        else:
            return JsonResponse({'error':'Invlaid credentials'})
            
    except UserModel.DoesNotExist:
        return JsonResponse({'error':'Invlaid credentials'})


# signout
@csrf_exempt
def signout(request, id):
    logout(request)

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = '0'
        user.save()

    except UserModel.DoesNotExist:
        return JsonResponse({'error':'Invlaid User ID'})
 

    return JsonResponse({'success':'Logged out...'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]

        except KeyError:
            return [permission() for permission in self.permission_classes]

