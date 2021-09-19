from livefeed.models import UserHandlesMap

def addHandleUtil(user, handle):
    new_row = UserHandlesMap(user=user, handle=handle)
    new_row.save()

def handleExists(user, handle):
    results = UserHandlesMap.objects.filter(user=user, handle=handle.screen_name)
    if results.exists():
        handle.following = True
    return handle
