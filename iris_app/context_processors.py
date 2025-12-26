# iris_app/context_processors.py

def global_access_control(request):
    # Kullanıcı giriş yapmışsa ve Writer grubundaysa TRUE döner
    is_writer = False
    if request.user.is_authenticated:
        is_writer = request.user.groups.filter(name='Writer').exists()

    # Bu değişkeni artık TÜM HTML sayfalarında kullanabilirsin
    return {'is_writer': is_writer}