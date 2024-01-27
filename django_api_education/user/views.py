from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import User

@csrf_exempt 
def actionWithUser(request):
    if request.method == 'POST':
        dto = {
        'email': request.POST.get("email"), 
        'password': request.POST.get("password"),
        'name': request.POST.get("name"),
        'age': request.POST.get("age"),
         }
        
        if not dto['email'] or not dto['password']:
            return JsonResponse({'error': 'Email and password is required fields'}, status=400)
        
        return createUser(dto)
    elif request.method == 'PATCH':
         
         return updateUser()
    elif request.method == 'DELETE':

        return deleteUser()
    else:

        return HttpResponse("Method is not exist", status=404, reason="Not found")

def getUsersList(request):
    try:
        usersList = User.objects.all()
        users_data = [user.to_dict() for user in usersList]
        return JsonResponse({'status': 'success', 'users': users_data}, status=200)
    
    except Exception as e:
          return JsonResponse({'error': str(e)}, status=500)

def getUser(_, id):
    try:
        userData = User.objects.get(id=id)

        return JsonResponse({'status': 'success', 'user': userData.to_dict()}, status=200)
    
    except ObjectDoesNotExist:
         return JsonResponse({'error': 'User not exist'}, status=404)
    except MultipleObjectsReturned:
         return JsonResponse({'error': 'Founded several users with same id'}, status=400)

def createUser(dto):
    try:
        dto["password"] = make_password(dto["password"])
        newUser = User.objects.create(**dto)
        newUser.save()
        return JsonResponse({'status': 'success', 'userId': newUser.id}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def updateUser():
    return JsonResponse({})

def deleteUser():
    return JsonResponse({})