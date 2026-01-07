import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils.exceptions import HTTPError
from todos.validators.todo_validator import validate_input
from todos.services.todo_service import TodoService

class TodoCreateView(APIView):

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            raise HTTPError(400, 'Invalid JSON')
        
        valid, err = validate_input(data)
        if not valid:
            raise HTTPError(400, err)

        todo = TodoService.create_todo(data)

        return Response({
            "success": True,
            "data": todo,
        }, status=status.HTTP_201_CREATED)
