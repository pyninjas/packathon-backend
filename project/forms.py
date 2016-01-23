from django.utils.translation import ugettext_lazy as _
from django import forms
from project.models import Project


class ProjectForm(forms.ModelForm):
    """
    Form for adding or editing project
    Note: Set vote to 0 manually before save() while creating new project
    """
    name = forms.CharField(label=_("Project Name"),
                           widget=forms.TextInput(attrs={
                               'placeholder': _('Project Name'),
                               'class': 'form-control textinput',
                               'required': 'required'}))
    git = forms.URLField(label=_("Git"), required=False,
                         widget=forms.TextInput(attrs={
                             'placeholder': _('Git URL'),
                             'class': 'form-control textinput'}))
    website = forms.URLField(label=_("Website"), required=False,
                             widget=forms.TextInput(attrs={
                                 'placeholder': _('Website URL'),
                                 'class': 'form-control textinput'}))

    class Meta:
        model = Project
        fields = ['name', 'git', 'website']

    def clean(self):
        cleaned_data = self.cleaned_data
        website = cleaned_data.get('website')
        if website:
            if not website.startswith('http://') and not website.startswith('https://') and website != '':
                website = 'http://' + website
                cleaned_data['website'] = website
            elif website == '':
                del(cleaned_data['website'])
        git = cleaned_data.get('git')
        if git:
            if not git.startswith('http://') and not git.startswith('https://') and git != '':
                git = 'https://' + git
                cleaned_data['git'] = git
            elif git == '':
                del(cleaned_data['git'])
        return cleaned_data
