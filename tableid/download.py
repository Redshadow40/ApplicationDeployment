# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
import os

def downloadFile(request, filePath, applicationType):
        if os.path.exists(filePath):
                with open(filePath, 'rb') as fh:
                        response = HttpResponse(fh.read(), content_type='application/' + applicationType )
                        response['Content-Disposition'] = 'inline; filename=%s' % os.path.basename(filePath)
                        return response
        raise Http404
