from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

import asyncio
import json
import aioredis

from .models import Car
from user.consumers import UserConsumer


def get_cars_list(request):
    limit = 10
    limit_param = request.GET.get("limit")
    if limit_param is not None:
        limit = int(limit_param)
    try:
        cars_list = Car.objects.all()[:limit]
        cars_data = [car.to_dict() for car in cars_list]
        return JsonResponse({"status": "success", "cars": cars_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def action_with_car(request, id=None):
    dto = None
    if request.method == "POST" or request.method == "PATCH":
        if "application/json" in request.content_type:
            body_data = request.body.decode("utf-8")
            data = json.loads(body_data)
            dto = {
                "make": data.get("make"),
                "model": data.get("model"),
                "year": data.get("year"),
            }
            return create_car(dto) if request.method == "POST" else update_car(id, dto)
        else:
            return JsonResponse({"error": "Unsupported content type"}, status=415)
    elif request.method == "GET":

        return get_car(id)
    elif request.method == "DELETE":

        return delete_car(id)
    else:

        return HttpResponse(
            "Method is not implemented", status=400, reason="Invalid HTTP method"
        )


def create_car(dto):
    if not all(dto.values()):
        return JsonResponse(
            {"error": "Make, model and year is required fields"}, status=400
        )
    try:
        # new_car = Car.objects.create(**dto)
        # new_car.save()
        subscribers = asyncio.run(get_subscribers())
        for user in subscribers:
            if user["connection"]:
                for user in subscribers:
                    if user["connection"]:
                        asyncio.run(
                            UserConsumer().send_message(
                                user["connection"],
                                {"event": "new_car_added", "carId": "id"},
                            )
                        )

        return JsonResponse({"status": "success", "carId": "id"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_car(id):
    if id == None:
        return HttpResponse(
            "ID parametr is required", status=400, reason="Invalid ID format"
        )
    try:
        car_data = Car.objects.get(id=id)

        return JsonResponse(
            {"status": "success", "car": car_data.to_dict()}, status=200
        )

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Car not exist"}, status=404)


def update_car(id, dto):
    if id == None:
        return HttpResponse(
            "ID parametr is required", status=400, reason="Invalid ID format"
        )
    elif not any(dto.values()):
        return HttpResponse(
            "You should change at least one field", status=400, reason="Nothing to save"
        )
    try:
        dto_filtered = dto.copy()
        # or the same
        # dto_filtered = dict(dto)
        for key, value in dto.items():
            if value is None:
                del dto_filtered[key]

        Car.objects.filter(id=id).update(**dto_filtered)

        return JsonResponse({"status": "success", "carId": id}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def delete_car(id):
    if id == None:
        return HttpResponse(
            "ID parametr is required", status=400, reason="Invalid ID format"
        )

    try:
        car = Car.objects.get(id=id)
        if car.users_owners.exists():
            return JsonResponse(
                {"error": "Car cannot be deleted, as it is associated with users"},
                status=400,
            )
        car.delete()
        return JsonResponse({"status": "success", "deletedCarId": id}, status=200)

    except Car.DoesNotExist:
        return JsonResponse({"error": "Car not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


async def get_subscribers():
    redis = await aioredis.from_url("redis://localhost")
    subscribers = await redis.smembers("new_car_subscribers")
    subscribers_data = []
    for subscriber in subscribers:
        subscribers_data.append(json.loads(subscriber))
    await redis.close()

    return subscribers_data
