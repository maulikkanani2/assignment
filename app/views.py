from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Assignment
from app.serialzer import AssignmentSeializer

class AssignmentView(APIView):
    def get(self, request, pk=None, format=None):
        """
        Return a list of all Assignment.
        """
        if pk:
            assignment = Assignment.objects.get(id=pk)
            serializer = AssignmentSeializer(assignment)
            return Response(serializer.data)
        
        assignment = Assignment.objects.all()
        serializer = AssignmentSeializer(assignment,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        create a Assignment.
        """
        assignment = request.data

        serializer = AssignmentSeializer(data=assignment)
        if serializer.is_valid(raise_exception=True):
            assignment_saved = serializer.save()
        return Response({"success": "Assignment '{}' created successfully".format(assignment_saved.title)})
    
    def put(self, request, pk, format=None):
        """
        update a Assignment.
        """
        assignment = Assignment.objects.get(id=pk)
        serializer = AssignmentSeializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)