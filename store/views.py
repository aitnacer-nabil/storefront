from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


# Create your views here.
@api_view()
def product_list(request):
    products = Product.objects.select_related('collection').all()
    products_serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(products_serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
        product_serializer = ProductSerializer(product)
    except Product.DoesNotExist:
        return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        product_serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        print("Product Update")
        return Response(product_serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if product.orderItems.count() > 0:
            return Response({'message': 'Product cannot be deleted because it is associated with an order item'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'GET':
        return Response(product_serializer.data)


@api_view(['POST'])
def product_save(request):
    product_serializer = ProductSerializer(data=request.data)
    product_serializer.is_valid(raise_exception=True)
    product_serializer.save()
    return Response(product_serializer.data, status=status.HTTP_201_CREATED)




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

@api_view(['GET', 'PUT','DELETE'])
def collection_detail(request, pk):
    try:
        collection = Collection.objects.get(id=pk)
    except Collection.DoesNotExist:
        return Response({'message': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CollectionSerializer(instance=collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)



