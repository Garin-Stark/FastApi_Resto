import os
from time import strftime
from fastapi.responses import JSONResponse
from fastapi import UploadFile
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
import string
import random
import base64
import numpy as np
from fastapi import UploadFile, File

app = FastAPI()

def success(message, status_code=200):
    return JSONResponse(content={'status_code': status_code, 'message': message}, status_code=status_code)

def success_data(message, data, status_code=200):
    return JSONResponse(content={'status_code': status_code, 'message': message, 'data': data}, status_code=status_code)

def authorization_error():
    return JSONResponse(content={'error': 'Permission Denied', 'status_code': 403}, status_code=403)

def invalid_params():
    return JSONResponse(content={'error': 'Invalid Parameters', 'status_code': 400}, status_code=400)

def bad_request(description=""):
    return JSONResponse(content={'description': f"{description}", 'error': 'Bad Request', 'status_code': 400}, status_code=400)

def not_found_error():
    return JSONResponse(content={'error': 'Not Found', 'status_code': 404}, status_code=404)

def defined_error(description, error="Defined Error", status_code=400):
    return JSONResponse(content={'description': description, 'error': error, 'status_code': status_code}, status_code=status_code)

def parameter_error(description, error="Parameter Error", status_code=400):
    return JSONResponse(content={'description': description, 'error': error, 'status_code': status_code}, status_code=status_code)

def random_string_number_only(stringLength):
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

def random_string(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def save(encoded_data, filename):
    encoded_data = encoded_data.split(',')[1]
    arr = np.fromstring(base64.b64decode(encoded_data), np.uint8)

def validatepassword(password):
    message = ""
    if len(password) < 8:
        message += "Panjang Password setidaknya harus 8"
    if len(password) > 20:
        message += "Panjang Password tidak boleh lebih dari 20"
    if not any(char.isdigit() for char in password):
        message += "Password harus memiliki setidaknya satu angka"
    if not any(char.isupper() for char in password):
        message += "Password harus memiliki setidaknya satu huruf besar"
    if not any(char.islower() for char in password):
        message += "Password harus memiliki setidaknya satu huruf kecil"
    return message
