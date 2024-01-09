from .models import CategoryModel


def categories(request):
    return {'categories': CategoryModel.objects.all().prefetch_related('types').order_by('-created_at')}
