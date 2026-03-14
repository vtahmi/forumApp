from datetime import datetime, time

from django.http import HttpResponseForbidden


class ReadOnlyMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for field in self.fields:
            self.fields[field].disabled = True
            self.fields[field].widget.attrs['readonly'] = True

class TimeRestrictedMixin:
    access_start_time = time(9, 0) # 9:00 AM
    access_end_time = time(23, 0) # 5:00 PM
    def dispatch(self, request, *args, **kwargs):
        current_time = datetime.now().time()
        if not (self.access_start_time <= current_time <= self.access_end_time):
            return HttpResponseForbidden("Access to this view is restricted to business hours (9 AM - 5 PM).")
        return super().dispatch(request, *args, **kwargs)