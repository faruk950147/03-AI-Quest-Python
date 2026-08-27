from django.contrib.sites.shortcuts import get_current_site
current_site = get_current_site(request)
print("Current Site: ", current_site.domain)
print("Custom Host: ", request.get_host())
