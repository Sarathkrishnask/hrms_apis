from django.shortcuts import HttpResponse
import json


def Response(data,message,http_code, error=True, json_format=True):
    if error:
        status = True
        response = {
            "result": data,
            "message":message,
            "status": status,
            "responseCode": http_code
        }
        # http_code=200
    else:
        status = False
        # http_code=404
        response = {
            "result": data,
            "message":message,
            "status": status,
            "responseCode":http_code
        }
    if json_format:
        response = json.dumps(response)

    return HttpResponse(response, content_type='Application/json', status=int(http_code))

