from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
import requests
from django.http import JsonResponse
import pyrebase

# Create your views here.
config = {
    "apiKey": "AIzaSyC59vAEywYwmZY3USztoFh5EtVSAu_DIEs",
    "authDomain": "idp-letsgooo.firebaseapp.com",
    "databaseURL": "https://idp-letsgooo-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "idp-letsgooo",
    "storageBucket": "idp-letsgooo.appspot.com",
    "messagingSenderId": "184004956450",
    "appId": "1:184004956450:web:6826e95265a37517a2957b",
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def index(request):
    return render(request, 'Index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('admin/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'login.html')


def route(request):
    my_headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hcGkudW0uZWR1Lm15Iiwic3ViIjoiMzExNTkyYWYtMWY0NC01MDMyLThiYjQtNGFjNzYzZGFlOWFmIiwiaWF0IjoxNTQ1NjM0OTMzLCJleHAiOjE2MzE5NDg1MzMsIm5hbWUiOiJ2ZWhpY2xlIn0.-EwaMdzZyILuKZ7Mjuemm4hvQM-H5kcza1dTle3nsWs'
    }
    response = requests.get('https://api.um.edu.my/vehicle/route', headers=my_headers)
    data = response.json()

    context = {
        'data': data,
    }
    return render(request, 'Test.html', context)


def bus_stop(request, pk):
    my_headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hcGkudW0uZWR1Lm15Iiwic3ViIjoiMzExNTkyYWYtMWY0NC01MDMyLThiYjQtNGFjNzYzZGFlOWFmIiwiaWF0IjoxNTQ1NjM0OTMzLCJleHAiOjE2MzE5NDg1MzMsIm5hbWUiOiJ2ZWhpY2xlIn0.-EwaMdzZyILuKZ7Mjuemm4hvQM-H5kcza1dTle3nsWs'
    }
    response = requests.get('https://api.um.edu.my/vehicle/route/' + pk, headers=my_headers)
    data = response.json()
    locations = []

    for item in data['stops']:
        locations.append(
            {'stop_id': item['stop_id'],
             'name': item['name'],
             'latitude': item['lat'],
             'longitude': item['long'],
             'url': 'http://127.0.0.1:8000/rtbl/' + data['route_id'] + '/' + item['stop_id']
             }
        )

    context = {
        'locations': locations,
    }
    return render(request, 'stops.html', context)


def rtbl(request, pk, pt):
    my_headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hcGkudW0uZWR1Lm15Iiwic3ViIjoiMzExNTkyYWYtMWY0NC01MDMyLThiYjQtNGFjNzYzZGFlOWFmIiwiaWF0IjoxNTQ1NjM0OTMzLCJleHAiOjE2MzE5NDg1MzMsIm5hbWUiOiJ2ZWhpY2xlIn0.-EwaMdzZyILuKZ7Mjuemm4hvQM-H5kcza1dTle3nsWs'
    }
    response = requests.get('https://api.um.edu.my/vehicle/route/' + pk, headers=my_headers)
    data = response.json()
    locations = []
    user_info = [
        {
            'route_id': pk,
            'stop_id': pt,
        }
    ]

    for item in data['stops']:
        if item['stop_id'] == pt:
            locations.append(
                {
                    'latitude': item['lat'],
                    'longitude': item['long'],
                }
            )

    context = {
        'locations': locations,
        'user_info': user_info,
    }

    return render(request, 'buslocation.html', context)


def get_buslocation(request, pk, pt):
    my_headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hcGkudW0uZWR1Lm15Iiwic3ViIjoiMzExNTkyYWYtMWY0NC01MDMyLThiYjQtNGFjNzYzZGFlOWFmIiwiaWF0IjoxNTQ1NjM0OTMzLCJleHAiOjE2MzE5NDg1MzMsIm5hbWUiOiJ2ZWhpY2xlIn0.-EwaMdzZyILuKZ7Mjuemm4hvQM-H5kcza1dTle3nsWs'
    }
    response = requests.get('https://api.um.edu.my/vehicle/bus/' + pk + '/' + pt, headers=my_headers)
    response_1 = requests.get('https://api.um.edu.my/vehicle/route/' + pk, headers=my_headers)

    data = response.json()
    data_1 = response_1.json()

    passenger_counter = database.child('Dummy_Data').get().val()
    print(passenger_counter)

    bus_location = []
    i = 1
    info = []

    for item in data:
        bus_location.append(
            {
                'latitude': item['position']['latitude'],
                'longitude': item['position']['longitude'],
                'eta': item['eta']['time'],
                'distance': item['eta']['distance'],
                'plate_no': item['bus']['plate_no'],
                'color': random_color(i),
                'seq': item['seq'],
            }
        )
        i += 1

    for item in data_1['polylines']:
        info.append(
            {
                'latitude': item['lat'],
                'longitude': item['lng'],
            }
        )

    context = {
        'bus_location': bus_location,
        'info': info,
        'passenger_counter': passenger_counter,
    }

    return JsonResponse(context)


def tablet(request, pk, pt):
    my_headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hcGkudW0uZWR1Lm15Iiwic3ViIjoiMzExNTkyYWYtMWY0NC01MDMyLThiYjQtNGFjNzYzZGFlOWFmIiwiaWF0IjoxNTQ1NjM0OTMzLCJleHAiOjE2MzE5NDg1MzMsIm5hbWUiOiJ2ZWhpY2xlIn0.-EwaMdzZyILuKZ7Mjuemm4hvQM-H5kcza1dTle3nsWs'
    }
    response = requests.get('https://api.um.edu.my/vehicle/route/' + pk, headers=my_headers)
    data = response.json()
    locations = []
    user_info = [
        {
            'route_id': pk,
            'stop_id': pt,
        }
    ]

    for item in data['stops']:
        if item['stop_id'] == pt:
            locations.append(
                {
                    'latitude': item['lat'],
                    'longitude': item['long'],
                }
            )

    context = {
        'locations': locations,
        'user_info': user_info,
    }

    return render(request, 'tablet.html', context)


def random_color(i):
    color = ['red', 'yellow', 'green', 'purple', 'maroon', 'aqua']
    return color[i]


def strtoint(i):
    lst = []
    for letter in i:
        lst.append(letter)
    y = []
    total = 0
    k = len(lst)
    h = len(lst)
    l = 0
    while l < k:
        n = check_num(lst[l])
        if h == 3:
            n = n * 100
        elif h == 2:
            n = n * 10
        else:
            n = n * 1
        y.append(n)
        h -= 1
        l += 1

    for g in y:
        total = total + g

    return total


def check_num(i):
    if i == "1":
        return 1
    elif i == '2':
        return 2
    elif i == '3':
        return 3
    elif i == '4':
        return 4
    elif i == '5':
        return 5
    elif i == '6':
        return 6
    elif i == '7':
        return 7
    elif i == '8':
        return 8
    else:
        return 9
