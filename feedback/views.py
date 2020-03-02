from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .serializers import FeedbackSerializer


class FeedbackView(APIView):
    renderer_classes = (JSONRenderer,)

    @method_decorator(csrf_exempt)
    def post(self, request):
        global feedback_saved
        feedback = request.data.get('feedback')

        serializer = FeedbackSerializer(data=feedback)
        if serializer.is_valid(raise_exception=True):
            feedback_saved = serializer.save()
        return JsonResponse({"success": "Feedback created successfully: {0} | {1} | {2} | {3}".format(
            feedback_saved.name, feedback_saved.email, feedback_saved.phone, feedback_saved.comment)}, safe=False)
