from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import json

from car.models import Car

from .models import User


def getUsersList(request, limit=10):
    limit_param = request.GET.get("limit")
    if limit_param is not None:
        limit = int(limit_param)
    try:
        users_list = User.objects.all()[:limit]
        users_data = [user.to_dict() for user in users_list]
        return JsonResponse({"status": "success", "users": users_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def actionWithUser(request, id=None):
    dto = None
    if request.method == "POST" or request.method == "PATCH":
        if "application/json" in request.content_type:
            body_data = request.body.decode("utf-8")
            data = json.loads(body_data)
            dto = {
                "email": data.get("email"),
                "password": data.get("password"),
                "name": data.get("name"),
                "age": data.get("age"),
            }

            if request.method == "PATCH":
                dto["carIds"] = data.get("carIds", [])
            return createUser(dto) if request.method == "POST" else updateUser(id, dto)
        else:
            return JsonResponse({"error": "Unsupported content type"}, status=415)
    elif request.method == "GET":

        return getUser(id)
    elif request.method == "DELETE":

        return deleteUser(id)
    else:

        return HttpResponse("Method is not exist", status=404, reason="Not found")


def getUser(id):
    if id == None:
        return HttpResponse("ID parametr is required", status=404, reason="Not found")
    try:
        user_data = User.objects.get(id=id)

        return JsonResponse(
            {"status": "success", "user": user_data.to_dict()}, status=200
        )

    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not exist"}, status=404)
    except MultipleObjectsReturned:
        return JsonResponse({"error": "Founded several users with same id"}, status=400)


def createUser(dto):
    if not dto["email"] or not dto["password"]:
        return JsonResponse(
            {"error": "Email and password is required fields"}, status=400
        )
    try:
        dto["password"] = make_password(dto["password"])
        new_user = User.objects.create(**dto)
        new_user.cars.set([])
        new_user.save()
        return JsonResponse({"status": "success", "userId": new_user.id}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def updateUser(id, dto):
    if id == None:

        return HttpResponse("ID parametr is required", status=404, reason="Not found")
    elif not any(dto.values()):

        return HttpResponse(
            "You should change at least one field", status=400, reason="Nothing to save"
        )
    try:
        user_for_update = User.objects.get(id=id)
        for key, value in dto.items():
            if value is not None and key is not "carIds":
                setattr(user_for_update, key, value)
        if "carIds" in dto and dto["carIds"] is not None:
            addCarToUserCarsList(dto, user_for_update)
        user_for_update.save()

        return JsonResponse(
            {"status": "success", "userId": user_for_update.to_dict()}, status=200
        )
    except ObjectDoesNotExist:

        return JsonResponse({"error": "User not exist"}, status=404)


def deleteUser(id):
    if id == None:
        return HttpResponse("ID parametr is required", status=404, reason="Not found")
    try:
        deleted_user_count, _ = User.objects.filter(id=id).delete()

        if deleted_user_count > 0:
            return JsonResponse({"status": "success", "deletedUserId": id}, status=200)
        else:
            return JsonResponse({"error": "User not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def addCarToUserCarsList(dto, user_for_update):
    car_ids_list = json.loads(dto["carIds"])
    for car_id in car_ids_list:
        try:
            car = Car.objects.get(id=car_id)
            user_for_update.cars.add(car)
        except Car.DoesNotExist:
            pass
