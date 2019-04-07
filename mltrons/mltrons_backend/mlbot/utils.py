# from django.core.exceptions import ImproperlyConfigured
# from .models import *
# import json
# from django.contrib.auth import get_user_model
# User = get_user_model()
#
# def belongs_to_user(fn=None):
#     def decorator(view):
#         def wrapped_view(self, request, *args, **kwargs):
#             if callable(fn):
#                 obj = fn(request, *args, **kwargs)
#             else:
#                 obj = fn
#             try:
#                 project_id = request.POST.get('project_id')
#                 if member_group == None:
#                     data = request.data
#                     member_group = data['group']
#                 member_permissions = GroupMember.objects.get(group_id=member_group, user=request.user).user_role.permissions.all().values_list('codename', flat=True)
#                 member_permissions = list(member_permissions)
#                 missing_permissions = [perm for perm in permissions
#                                        if perm not in member_permissions]
#             except Exception as e:
#                 missing_permissions = [perm for perm in permissions]
#
#             if any(missing_permissions):
#                 # raises a permission denied exception causing a 403 response
#                 self.permission_denied(
#                     request,
#                     message=('Missing: {}'
#                              .format(', '.join(missing_permissions)))
#                 )
#             return view(self, request, *args, **kwargs)
#         return wrapped_view
#     return decorator