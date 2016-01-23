from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model


class ProfileForm(forms.ModelForm):
    """
    Edit profile form
    """
    name = forms.CharField(label=_("Name"),
                           widget=forms.TextInput(attrs={'placeholder': _('Name')}))
    description = forms.CharField(label=_("Description,Position"), required=False,
                                  widget=forms.TextInput(attrs={'placeholder': _('Description, Position')}))
    website = forms.URLField(label=_("Website"), required=False,
                             widget=forms.TextInput(attrs={'placeholder': _('Website URL')}))
    git = forms.URLField(label=_("Git URL"), required=False,
                         widget=forms.TextInput(attrs={'placeholder': _('Git URL')}))
    twitter = forms.URLField(label=_("Twitter URL"), required=False,
                             widget=forms.TextInput(attrs={'placeholder': _('Twitter URL')}))

    class Meta:
        model = get_user_model()
        fields = ['name', 'description', 'website',
                  'git', 'twitter']

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
        twitter = cleaned_data.get('twitter')
        if twitter:
            if not twitter.startswith('http://') and not twitter.startswith('https://') and twitter != '':
                twitter = 'https://' + twitter
                cleaned_data['twitter'] = twitter
            elif twitter == '':
                del(cleaned_data['twitter'])
        return cleaned_data
