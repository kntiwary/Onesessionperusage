from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime,timezone
from django.shortcuts import render
from accounts.models  import LoggedInUser


class SimpleMiddlewaree:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # print(request)
        # Code to be executed for each request before
        # the view (and later middleware) are called.\
        token =request.META.get('HTTP_AUTHORIZATION')
        url =request.path_info
        print(url)

        exempt=['/api/v1/signin','/']
        if request.path_info and request.path_info not in exempt:
            # Request header has token
            if token:
                if User.objects.filter(logged_in_user__token=token[6:]):  # User is logged in
                    user = User.objects.filter(logged_in_user__token=token[6:])[0]
                    elapse_time = datetime.now(timezone.utc).minute - user.logged_in_user.login_time.minute
                    print(elapse_time)
                    if elapse_time and 0 < elapse_time < 1:
                        print("session it running")

                    else:
                        print("Session has to be expired and redirected ")
                        # return render(request, 'home.html')
                        ## Need to add login function

            else:
                print("Request path", request.path)
                # print(HttpResponseRedirect(''))
                # return render(request, 'home.html')
                # return HttpResponse("Hello, world. You're at the polls index.")
                # return redirect('login')
            response = self.get_response(request)
            # Code to be executed for each request/response after
            # the view is called.
            return response

        else:
            return HttpResponseRedirect(reverse('login'))
            # return HttpResponse("Hello, world. You're at the polls index.")
            # print("Redirect to login page")
            # response = self.get_response(request)
            # return response
