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
    # if begin_date and not end_date:
    #     end_date = "2099-12-31"
    # if end_date and not begin_date:
    #     begin_date = "1996-02-25"
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
                data_list.append(
                    {"lng": float(row[2]), "lat": float(row[3]), "count": int(row[0]),
                     "place_name": row[4]})  # , "name": row[4]})
            except Exception as e:
                pass
        return render(request, "index.html",
                      {"files": files_list, "file_name": file_name, "data_list": data_list, "begin_date": begin_date,
                       "end_date": end_date, "file_log": file_log})
    return render(request, "index.html", {"files": files_list})
