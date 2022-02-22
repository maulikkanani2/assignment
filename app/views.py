from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Assignment
from app.serialzer import AssignmentSeializer
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
import base64

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

class PdfGenerate(APIView):
    def get(self, request, pk, *args, **kwargs):
        assignment = Assignment.objects.get(id=pk)
        data = {
            'title': assignment.title, 
            'description': assignment.description,
            'music_genre': assignment.music_genre,
            'daily_practice_time': assignment.daily_practice_time,
            'days':assignment.days,
            'days_practiced':assignment.days_practiced
        }
        template = get_template("pdf.html")
        html_string = render_to_string('pdf.html', {'data': data})

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/pdf.pdf');

        fs = FileSystemStorage('/tmp')
        with fs.open('pdf.pdf', "rb") as pdf:
            encoded_string = base64.b64encode(pdf.read())
            assignment.base = encoded_string
            assignment.save()
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="pdf.pdf"'
            return HttpResponse(encoded_string) 