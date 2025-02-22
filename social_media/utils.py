from functools import wraps
from django.db.models.query import QuerySet


def skip_for_swagger(view_method):
    @wraps(view_method)
    def wrapper(self, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            if hasattr(self, 'queryset') and isinstance(self.queryset, QuerySet):
                return self.queryset.none()
            return QuerySet().none()
        return view_method(self, *args, **kwargs)

    return wrapper
