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
    begin_date = request.GET.get("begin_date", "")
    end_date = request.GET.get("end_date", "")
    begin_price = request.GET.get("begin_price", "")
    end_price = request.GET.get("end_price", "")
    if file_name:
        csv_reader = csv.reader(open(files_dir + '/' + file_name, encoding='utf-8'))
        log_name = os.path.dirname(BASE_DIR) + "/log/" + file_name.split(".csv")[0] + ".log"
        file_log = "暂无日志"
        try:
            file_log = open(log_name).read()
        except Exception as e:
            pass
        data_list = []
        for row in islice(csv_reader, 1, None):
            if row[0] == "0":
                continue
            try:
                if begin_date:
                    if not begin_date < row[5]:
                        continue
                if end_date:
                    if not end_date > row[5]:
                        continue
                if begin_price:
                    if not int(begin_price) < int(row[0]):
                        continue
                if end_price:
                    if not int(end_price) > int(row[0]):
                        continue
                data_list.append(
                    {"lng": float(row[2]), "lat": float(row[3]), "count": int(row[0]),
                     "place_name": row[4]})  # , "name": row[4]})
            except Exception as e:
                pass
        if end_price:
            scale = {"a": (int(end_price) * 0.45), "b": int(end_price) * 0.55, "c": int(end_price) * 0.65,
                     "d": int(end_price) * 0.8,
                     "e": int(end_price) * 0.95, "f": int(end_price)}
        else:
            scale = {"a": 45000, "b": 55000, "c": 65000, "d": 80000, "e": 95000,
                     "f": 100000}
        return render(request, "index.html",
                      {"files": files_list, "file_name": file_name, "data_list": data_list, "begin_date": begin_date,
                       "end_date": end_date, "file_log": file_log, "begin_price": begin_price, "end_price": end_price,
                       "scale": scale})
    return render(request, "index.html", {"files": files_list})
