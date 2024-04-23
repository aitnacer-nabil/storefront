from django.shortcuts import render
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductApi(APIView):
    def get(self, request, id=None):
        if id:
            try:
                product = Product.objects.get(id=id)
                product_serializer = ProductSerializer(product)
                return Response(product_serializer.data)
            except Product.DoesNotExist:
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            products = Product.objects.select_related('collection').all()
            products_serializer = ProductSerializer(products, many=True, context={'request': request})
            return Response(products_serializer.data)

    def post(self, request):
        product_serializer = ProductSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product_serializer = ProductSerializer(instance=product, data=request.data, partial=True)
            product_serializer.is_valid(raise_exception=True)
            product_serializer.save()
            return Response(product_serializer.data)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, stGIatus=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
            if product.orderItems.count() > 0:
                return Response({'message': 'Product cannot be deleted because it is associated with an order item'},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)




@api_view()
def collection_list(request):
    query = Collection.objects.all()
    serializer = CollectionSerializer(query, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def collection_save(request):
    serializer = CollectionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    try:
        collection = Collection.objects.annotate(
            products_count=Count('products')
        ).get(pk=pk)
    except Collection.DoesNotExist:
        return Response({'message': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CollectionSerializer(instance=collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products_count > 0:
            return Response({'message': 'Collection cannot be deleted because it contains products'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)
