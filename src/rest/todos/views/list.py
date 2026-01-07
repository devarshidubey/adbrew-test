from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils.exceptions import HTTPError
from todos.services.todo_service import TodoService

class TodoListView(APIView):

    def get(self, request):
        return Response({"key": "gigigi"}, status=status.HTTP_200_OK)

    def get(self, request):
        # Implement this method - return all todo items from db instance above.
        page = request.query_params.get("page", 1)
        limit = request.query_params.get("limit", 20)

        try:
            page = int(page)
            limit = int(limit)
            if page < 1 or limit < 1:
                raise ValueError
        except ValueError:
            raise HTTPError(400, "page and limit must be positive integers")

        result = TodoService.list_todos(
            page=page,
            limit=limit,
        )

        total_pages = (result["total"] + limit - 1) // limit

        return Response(
            {
                "success": True,
                "data": result["items"],
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total_items": result["total"],
                    "total_pages": total_pages,
                },
            },
            status=status.HTTP_200_OK,
        )
