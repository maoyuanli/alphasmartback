from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FeedbackSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


class FeedbackView(APIView):
    renderer_classes = (JSONRenderer,)

    @method_decorator(csrf_protect)
    def post(self, request):
        feedback = request.data.get('feedback')

        serializer = FeedbackSerializer(data=feedback)
        if serializer.is_valid(raise_exception=True):
            feedback_saved = serializer.save()
        return JsonResponse({"success": "Feedback created successfully: {0} | {1} | {2} | {3}".format(feedback_saved.name,feedback_saved.email,feedback_saved.phone,feedback_saved.comment)}, safe=False)
