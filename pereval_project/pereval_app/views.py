from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PerevalSerializer

@api_view(['POST'])
def submit_data(request):
    serializer = PerevalSerializer(data=request.data)

    if serializer.is_valid():
        pereval = serializer.save()
        return Response(
            {"status": 200, "message": None, "id": pereval.id},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"status": 400, "message": "Bad Request: invalid data", "id": None},
            status=status.HTTP_400_BAD_REQUEST
        )