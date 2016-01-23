# Packathon API & Web Client
==================================

## Documentation:

 * Api Endpoint: `/api`
 * Login Endpoint: `/api/login/`
 * Login will return Token, it should be in request header: `Authorization Token xxx`
 * Current user: `/api/user/`
 * Vote time: `/api/votetime/`
 * By default api returns 100 results, adding `page_size=N` will change size
 * django-filters added, in list views you can search using parameters: `/api/teams/?name=pyninjas`
 * Voting: POST `/api/projects/<id>/vote`
 * ...
----------------------------------
## INSTALL:

* `git clone repo_url`
* `cd packathon-vote`
* `sudo pip3 install -U -r requirements.txt`
* Check settings file
* `python3 manage.py makemigrations`
* `python3 manage.py migrate`
* `python3 manage.py createsuperuser`
* `python3 manage.py runserver`
----------------------------------
### Developed by pyninjas.com
