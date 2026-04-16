from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from .models import SensorData

import json
from django.core.serializers.json import DjangoJSONEncoder


# API to fetch data (used by dashboard AJAX)
def get_sensor_data(request):
    data = list(SensorData.objects.all().order_by('-timestamp')[:50].values())
    return JsonResponse(data, safe=False)


# Dashboard page
def dashboard(request):
    data = SensorData.objects.all().order_by('-timestamp')[:20]

    data_json = json.dumps(list(data.values()), cls=DjangoJSONEncoder)

    return render(request, 'dashboard.html', {
        'data': data,
        'data_json': data_json
    })


# CSRF disabled for Lambda
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def receive_data(request):
    data = request.data

    SensorData.objects.create(
        temperature=data.get("temperature"),
        humidity=data.get("humidity"),
        soil_moisture=data.get("soil_moisture"),
        leaf_wetness=data.get("leaf_wetness"),
        light_intensity=data.get("light_intensity"),
        risk=data.get("risk", "LOW")
    )

    return Response({"message": "Data saved"})
