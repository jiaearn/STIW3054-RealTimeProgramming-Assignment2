import time
from django.db import models


class Victim(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True, verbose_name='Timestamp', editable=False)
    ic_no = models.CharField(primary_key=True, max_length=255, verbose_name='IcNo', editable=False)
    name = models.CharField(max_length=255, verbose_name='Name', editable=False)
    phone = models.CharField(max_length=255, verbose_name='Phone')

    def age_count(self):
        ic_year = int(self.ic_no[0:2])
        cur_year = int(time.strftime("%y", time.localtime()))
        if ic_year > cur_year:
            age = cur_year - ic_year + 100
        else:
            age = cur_year - ic_year
        return age

    age = property(age_count)
