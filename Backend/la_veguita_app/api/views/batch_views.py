from django.shortcuts import render
from rest_framework import generics
from ..models import Batch
from ..serializers import BatchSerializer


class BatchListCreate(generics.ListCreateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer


class BatchRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    lookup_field = "id_batch"