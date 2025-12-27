def global_access_control(request):
    is_writer = False
    if request.user.is_authenticated:
        is_writer = request.user.groups.filter(name='Writer').exists()
    return {'is_writer': is_writer}