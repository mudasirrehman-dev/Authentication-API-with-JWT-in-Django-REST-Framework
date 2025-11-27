''' Note
Global setting (settings.py)

Sari views → same format return karengi(yani json or xml etc)

Agar hum sari views ki bajy sirf custom kuch format lagana chaty hain 
jasy JSON, Xml etc,

To hum renderers.py say custom format bana sakty hai specific view kay liay

'''

from rest_framework import renderers
import json

class UserRenderers(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors' : data})
        else:
            response = json.dumps(data)
        return response
    