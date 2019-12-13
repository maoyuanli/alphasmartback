from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from logging import getLogger

logger = getLogger('AccountView Logger')


class AccountView(APIView):

    @method_decorator(csrf_exempt)
    def post(self, request):
        new_user = request.data.get('new_user')
        if User.objects.filter(username=new_user['username']).exists():
            return JsonResponse({"ErrMsg": f"Username exists {new_user['username']}"}, safe=False)
        elif User.objects.filter(email=new_user['email']).exists():
            return JsonResponse({"ErrMsg": f"Email exists {new_user['email']}"}, safe=False)
        else:
            user = User.objects.create_user(username=new_user['username'],
                                            password=new_user['password'],
                                            email=new_user['email'],
                                            first_name=new_user['first_name'],
                                            last_name=new_user['last_name'])
            user.save()
            created_user = User.objects.get(username=new_user['username'])
            return JsonResponse({"success": f"User created successfully: username : {created_user.username} | email : {created_user.email}"},
                                safe=False)
