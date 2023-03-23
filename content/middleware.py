# Question 1 Create a custom middleware to log each request with id of user and request id.

from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin
import uuid
from django.http import HttpResponsePermanentRedirect


class LogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # each request with id of user and request id
        # request.META Is Dictionary contains all HTTPS headers
        request_id = str(uuid.uuid4())
        setattr(request, "request_id", request_id)  # We can create UUID for each unique request
        user_id = request.META.get("USERNAME")
        print(f"user_id :{user_id}  Req_id :{request_id}")

        # print(request.META.keys())
        # print(request.META.values())
        return None

    def process_response(self, request, response):
        # Check response for any sensitive middleware
        # TODO keys to check password, DOB, address
        print("inside response --->", response.content)

        return response
