from django.contrib.sites.shortcuts import get_current_site
current_site = get_current_site(request)
print("Current Site: ", current_site.domain)
print("Custom Host: ", request.get_host())


if (res.status === "added") {

    alertify.success(res.message);
    $("#wish-count").text(res.wish_count);

} else if (res.status === "removed") {

    alertify.error(res.message);
    $("#wish-count").text(res.wish_count);
}



