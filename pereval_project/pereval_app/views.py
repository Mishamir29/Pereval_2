from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pereval, User
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


@api_view(['GET'])
def get_pereval_by_id(request, id):
    try:
        pereval = Pereval.objects.select_related('user', 'coords').prefetch_related('images__image').get(id=id)
    except Pereval.DoesNotExist:
        return Response(
            {"message": "Pereval not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = PerevalSerializer(pereval)
    data = serializer.data
    # Добавляем статус в ответ, если его нет
    data['status'] = pereval.status
    return Response(data)


@api_view(['PATCH'])
def edit_pereval(request, id):
    try:
        pereval = Pereval.objects.get(id=id)
    except Pereval.DoesNotExist:
        return Response(
            {"state": 0, "message": "Pereval not found"},
            status=status.HTTP_404_NOT_FOUND
        )


    if pereval.status != 'new':
        return Response(
            {"state": 0, "message": "Editing is allowed only for entries with status 'new'"},
            status=status.HTTP_400_BAD_REQUEST
        )


    data = request.data.copy()
    if 'user' in data:
        data.pop('user')

    serializer = PerevalSerializer(pereval, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"state": 1, "message": None}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"state": 0, "message": "Invalid data"},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_perevals_by_user_email(request):
    email = request.GET.get('user__email')

    if not email:
        return Response(
            {"message": "Email parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"message": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    perevals = Pereval.objects.filter(user=user).select_related('coords').prefetch_related('images__image')
    serializer = PerevalSerializer(perevals, many=True)
    return Response(serializer.data)