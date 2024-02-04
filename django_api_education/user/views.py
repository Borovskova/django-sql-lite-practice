from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import authenticate, login
from django.db import IntegrityError

import json

from car.models import Car
from .models import User


@csrf_exempt
def user_register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        age = data.get("age", 0)
        car_ids = data.get("car_ids", [])

        if not email or not password or not name:
            return JsonResponse(
                {"error": "Email, password, and name are required fields"}, status=400
            )
        try:
            user = User.objects.create_user(
                email=email, password=password, name=name, age=age
            )
            if user is not None:
                for car_id in car_ids:
                    try:
                        car = Car.objects.get(id=car_id)
                        user.cars.add(car)
                    except Car.DoesNotExist:
                        pass
                login(request, user)
                return JsonResponse(
                    {"status": "success", "userId": user.id}, status=201
                )
        except IntegrityError as e:
            return JsonResponse({"error": "Email already in use"}, status=409)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse(
                {"error": "Email and password are required fields"}, status=400
            )
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success", "userId": user.id}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def get_users_list(request, limit=10):
    limit_param = request.GET.get("limit")
    if limit_param is not None:
        limit = int(limit_param)
    try:
        users_list = User.objects.all()[:limit]
        users_data = [user.to_dict() for user in users_list]
        return JsonResponse({"status": "success", "users": users_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def action_with_user(request, id=None):
    dto = None
    if request.method == "PATCH":
        if "application/json" in request.content_type:
            body_data = request.body.decode("utf-8")
            data = json.loads(body_data)
            dto = {
                "email": data.get("email"),
                "password": data.get("password"),
                "name": data.get("name"),
                "age": data.get("age"),
                "car_ids": data.get("car_ids"),
            }

            return update_user(id, dto)
        else:
            return JsonResponse({"error": "Unsupported content type"}, status=415)
    elif request.method == "GET":

        return get_user(request, id)
    elif request.method == "DELETE":

        return delete_user(id)
    else:
        return HttpResponse(
            "Method is not implemented", status=400, reason="Invalid HTTP method"
        )


def get_user(request, id):
    if id == None:
        return HttpResponse(
            "ID parametr is required", status=400, reason="Invalid ID format"
        )
    try:
        user_data = User.objects.get(id=id)

        return JsonResponse(
            {"status": "success", "user": user_data.to_dict()}, status=200
        )

    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not exist"}, status=404)
    except MultipleObjectsReturned:
        return JsonResponse({"error": "Founded several users with same id"}, status=400)


def update_user(id, dto):
    if id == None:

        return HttpResponse(
            "ID parametr is required", status=400, reason="Invalid ID format"
        )
    elif not any(dto.values()):

        return HttpResponse(
            "You should change at least one field", status=400, reason="Nothing to save"
        )
    try:
        user_for_update = User.objects.get(id=id)
        for key, value in dto.items():
            if value != None and key != "car_ids":
                setattr(user_for_update, key, value)
        if "car_ids" in dto and dto["car_ids"] is not None:
            error_response = add_car_to_user_cars_list(dto, user_for_update)
            if error_response:
                return error_response

        user_for_update.save()

        return JsonResponse(
            {"status": "success", "userId": user_for_update.to_dict()}, status=200
        )
    except ObjectDoesNotExist:

        return JsonResponse({"error": "User not exist"}, status=404)


def delete_user(id):
    if id == None:
        return HttpResponse(
            "ID parametr is required", status=400, reason="Invalid ID format"
        )
    try:
        deleted_user_count, _ = User.objects.filter(id=id).delete()

        if deleted_user_count > 0:
            return JsonResponse({"status": "success", "deletedUserId": id}, status=200)
        else:
            return JsonResponse({"error": "User not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def add_car_to_user_cars_list(dto, user_for_update):
    car_ids_list = json.loads(dto["car_ids"])
    for car_id in car_ids_list:
        try:
            car = Car.objects.get(id=car_id)
            user_for_update.cars.add(car)
        except Car.DoesNotExist:
            return HttpResponse(
                f"Bad Car Id - {car_id}",
                status=404,
                reason=f"Car with id - {car_id} is not exist",
            )

    return None
