from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class SetSession(View):
    def get(self, request):
        request.session['user_name'] = 'Faruk Cse'
        request.session['user_id'] = 123

        request.session.save()  # 🔥 force save

        print("Session Key:", request.session.session_key)
        print("Session Data:", request.session.items())

        return HttpResponse("Session set successfully")


class GetSession(View):
    def get(self, request):
        print("Session Key in Get:", request.session.session_key)
        print("Session Data in Get:", request.session.items())

        context = {
            'user_name': request.session.get('user_name', 'Guest'),
            'user_id': request.session.get('user_id', 'Not Found')
        }
        return render(request, 'info/info.html', context)


class ClearSession(View):
    def get(self, request):
        request.session.flush()
        return HttpResponse("Session Cleared")
