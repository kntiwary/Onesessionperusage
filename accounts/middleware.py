from django.contrib.sessions.models import Session
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from datetime import datetime,timezone
from django.shortcuts import render

class OneSessionPerUsage:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # print(request)
        if not request.user.is_authenticated:
            # print(request.user)

            current_session_key = request.user.logged_in_user.session_key
            token= request.user.logged_in_user.token


            # avoid multiple session
            if current_session_key and  current_session_key != request.session.session_key:
                Session.objects.get(session_key=current_session_key).delete()

            # API Implementation the following code can be omitted . it's other way
            # check if token exist in header, expire the session and redirect
            exempt = ['/api/v1/signin', '/','login','admin']
            if request.path_info and request.path_info not in exempt:
                print("success")
                if token:
                    if User.objects.filter(logged_in_user__token=token[6:]):  # User is logged in
                        user = User.objects.filter(logged_in_user__token=token[6:])[0]
                        elapse_time = datetime.now(timezone.utc).minute - user.logged_in_user.login_time.minute
                        print(elapse_time)
                        if elapse_time and 0 < elapse_time < 30:
                            print("session it running")

                        else:
                            print("Session has to be expired and redirected ")
                            return render(request, 'home.html')
                            ## Need to add login function

                else:
                    # print("Request path", request.path)
                    return render(request, 'home.html')
                response = self.get_response(request)
                # Code to be executed for each request/response after
                # the view is called.
                return response

            # print("TOKEN",Token.objects.get(user=request.user))
            request.user.logged_in_user.session_key=request.session.session_key
            request.user.logged_in_user.token=Token.objects.get(user=request.user).key
            request.user.logged_in_user.save()



        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response