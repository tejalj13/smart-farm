from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SensorData
from django.shortcuts import render
from .models import SensorData
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import SensorData


def dashboard(request):
    data = SensorData.objects.all().order_by('-timestamp')[:20]

    data_json = json.dumps(list(data.values()), cls=DjangoJSONEncoder)

    return render(request, 'dashboard.html', {
        'data': data,
        'data_json': data_json
    })


@api_view(['POST'])
def receive_data(request):
    data = request.data

    SensorData.objects.create(
        temperature=data["temperature"],
        humidity=data["humidity"],
        soil_moisture=data["soil_moisture"],
        leaf_wetness=data["leaf_wetness"],
        light_intensity=data["light_intensity"],
        risk=data["risk"]
    )

    return Response({"message": "Data saved"})
