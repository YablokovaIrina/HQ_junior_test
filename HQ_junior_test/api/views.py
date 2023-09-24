from rest_framework import generics
from rest_framework import permissions
from django.db.models import Count, Sum, Q
from products.models import Product, LessonView
from .serializers import ProductSerializer, LessonViewSerializer


class LessonListView(generics.ListAPIView):
    serializer_class = LessonViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return LessonView.objects.filter(user=user)


class ProductLessonListView(generics.ListAPIView):
    serializer_class = LessonViewSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']
        return LessonView.objects.filter(
            user=user, lesson__product_id=product_id
            )


class ProductStatsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.annotate(
            num_lessons_viewed=Count(
                'lessons__lessonview',
                filter=Q(lessons__lessonview__is_viewed=True)
            ),
            total_time_viewed=Sum('lessons__lessonview__viewed_time'),
            num_students=Count('owner__productaccess'),
            product_access_count=Count(
                'owner__productaccess__user', distinct=True
            ),
        )
