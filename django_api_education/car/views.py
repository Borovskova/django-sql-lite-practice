from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

import json

from .models import Car


def getCarsList(request):
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
def actionWithCar(request, id=None):
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
            return createCar(dto) if request.method == "POST" else updateCar(id, dto)
        else:
            return JsonResponse({"error": "Unsupported content type"}, status=415)
    elif request.method == "GET":

        return getCar(id)
    elif request.method == "DELETE":

        return deleteCar(id)
    else:

        return HttpResponse("Method is not exist", status=404, reason="Not found")


def createCar(dto):
    for key, value in dto.items():
        if value == None:
            return JsonResponse(
                {"error": "Make, model and year is required fields"}, status=400
            )
    try:
        new_car = Car.objects.create(**dto)
        new_car.save()
        return JsonResponse({"status": "success", "carId": new_car.id}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def getCar(id):
    if id == None:
        return HttpResponse("ID parametr is required", status=404, reason="Not found")
    try:
        car_data = Car.objects.get(id=id)

        return JsonResponse(
            {"status": "success", "car": car_data.to_dict()}, status=200
        )

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Car not exist"}, status=404)


def updateCar(id, dto):
    return JsonResponse({})


def deleteCar(id):
    return JsonResponse({})
