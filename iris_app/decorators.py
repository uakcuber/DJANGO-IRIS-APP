# iris_app/decorators.py
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def writer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Önce giriş yapmış mı
        if not request.user.is_authenticated:
            return redirect('login')

        # Kullanıcı 'Writer' grubunda mı veya Yönetici mi
        is_writer = request.user.groups.filter(name='Writer').exists()

        if is_writer or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            # Yetkisi yoksa 403
            return HttpResponseForbidden("Bu işlem için yetkiniz yok (Sadece Yazarlar).")

    return _wrapped_view