import logging
import time
import uuid

from django.shortcuts import redirect
from django.urls import resolve, reverse_lazy
from s3chunkuploader.file_handler import UploadFailed

from conf.settings import FILE_UPLOAD_HANDLERS
from lite_content.lite_exporter_frontend import strings
from lite_forms.generators import error_page


class ProtectAllViewsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            name = f"{resolve(request.path).app_name}:{resolve(request.path).url_name}"
            allowed_paths = ["auth:login", "auth:callback", "core:home", "core:register_an_organisation"]

            if name not in allowed_paths:
                return redirect(reverse_lazy("auth:login"))

        response = self.get_response(request)

        return response


class UploadFailedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(f"Mark S upload handler count = {len(FILE_UPLOAD_HANDLERS)}")
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not isinstance(exception, UploadFailed):
            return None
        return error_page(request, strings.Goods.Documents.AttachDocuments.FILE_TOO_LARGE)


class LoggingMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        request.correlation = uuid.uuid4().hex
        data = {
            "user": request.user.lite_api_user_id if hasattr(request.user, "lite_api_user_id") else None,
            "message": "liteolog exporter",
            "corrID": request.correlation,
            "type": "http request",
            "method": request.method,
            "url": request.path,
        }
        response = self.get_response(request)
        data["type"] = "http response"
        data["elapsed_time"] = time.time() - start
        logging.info(data)
        return response
