# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
   gpsdata = forms.FileField(
                             label='Select a file',
                             help_text='max. 42 megabytes'
                             )