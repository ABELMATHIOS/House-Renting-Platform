def user_info(request):
    if request.user.is_authenticated:
        return {
            'current_username': request.user.username,
            'current_email': request.user.email
        }
    return {}
