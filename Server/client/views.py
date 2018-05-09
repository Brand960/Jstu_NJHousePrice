from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Server.settings import BASE_DIR
from itertools import islice
import os, csv, json


# Create your views here.

def index(request):
    files_list = []
    files_dir = os.path.dirname(BASE_DIR) + "/csv"
    for root, dir, files_list in os.walk(files_dir):
        pass

    files_list.sort()
    file_name = request.GET.get("name", "")
    if file_name:
        csv_reader = csv.reader(open(files_dir + '/' + file_name, encoding='utf-8'))
        data_list = []
        for row in islice(csv_reader, 1, None):
            if row[0] == "0":
                continue
            try:
                data_list.append(
                    {"lng": float(row[2]), "lat": float(row[3]), "count": int(row[0]),
                     "place_name": row[4]})  # , "name": row[4]})
            except Exception as e:
                pass
        return render(request, "index.html", {"files": files_list, "file_name": file_name, "data_list": data_list})
    return render(request, "index.html", {"files": files_list})
