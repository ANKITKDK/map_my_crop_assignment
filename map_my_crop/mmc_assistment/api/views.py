from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import openmeteo_requests
import requests_cache
import pandas as pd
import json
from datetime import datetime
from django.http import JsonResponse
from retry_requests import retry

# Create your views here.
class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class SampleApi(APIView):
    def post(self, request, *args, **kwargs):
        cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)
        try:
            REQUIRED_KEYS = ['latitude', 'longitude', 'start_date', 'end_date']
            json_data = json.loads(request.body.decode('utf-8'))
            for key in REQUIRED_KEYS:
                if key not in json_data or json_data[key] is None or json_data[key] == '':
                    return JsonResponse({'error': f'Missing or invalid value for key: {key}'})
            latitude = json_data.get('latitude')
            longitude = json_data.get('longitude')
            start_date = json_data.get('start_date')
            end_date = json_data.get('end_date')
            start_date_1 = datetime.strptime(json_data['start_date'], '%Y-%m-%d')
            end_date_1 = datetime.strptime(json_data['end_date'], '%Y-%m-%d')

            if end_date_1 < start_date_1:
                return JsonResponse({'error': 'End date must be greater than start date'})
            # return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'})
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ["temperature_2m", "precipitation", "cloud_cover"],
            "timezone": "Asia/Tokyo"
        }
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(2).ValuesAsNumpy()
        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["precipitation"] = hourly_precipitation
        hourly_data["cloud_cover"] = hourly_cloud_cover
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        json_data = hourly_dataframe.to_json(orient='records', date_format='iso', default_handler=str)
        data_list = json.loads(json_data)
        formatted_data_list = [
            {
                "date": entry["date"],
                "temperature_2m": entry["temperature_2m"],
                "precipitation": entry["precipitation"],
                "cloud_cover": entry["cloud_cover"]
            }
            for entry in data_list
        ]
        response_data = {'data': formatted_data_list}
        json_response = JsonResponse(response_data, safe=False)

        return json_response

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]




