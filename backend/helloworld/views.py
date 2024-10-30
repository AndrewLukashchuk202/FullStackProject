from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json


class ReceiveCoordinates(APIView):
    def post(self, request):
        # Extract x and y coordinates from the request
        data = request.data
        x = data.get('x')
        y = data.get('y')

        # Print to console
        print(f"Received coordinates: x={x}, y={y}")

        return Response({"message": "Coordinates received successfully"}, status=status.HTTP_200_OK)
