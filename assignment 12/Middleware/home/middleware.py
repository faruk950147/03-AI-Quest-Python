# Function-based middleware
from django.shortcuts import render, HttpResponse
def first_middleware(get_response):
    print("First One time initialization")  # server start a one time print

    def middleware_func(request):
        print("First Function Middleware: Before view")
        # anyone code
        response = get_response(request)
        print("First Function Middleware: After view")
        # anyone code
        return response

    return middleware_func

def second_middleware(get_response):
    print("Second One time initialization")  # server start a one time print

    def middleware_func(request):
        print("Second Function Middleware: Before view")
        # anyone code
        response = HttpResponse("Second Middleware View")
        print("Second Function Middleware: After view")
        # anyone code
        return response

    return middleware_func

# Class-based middleware
class CLSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("Class Middleware Initialized")  # server start a one time print

    def __call__(self, request):
        print("Class Middleware: Before view")
        # anyone code
        response = self.get_response(request)
        print("Class Middleware: After view")
        # anyone code
        return response