function getCookie(cookie, c_name) {
    if (0 < cookie.length) {
        var c_start = cookie.indexOf(c_name + "=");

        if (0 <= c_start) {
            var c_start = c_start + c_name.length + 1;
            var c_end = cookie.indexOf(";", c_start);

            if (-1 == c_end) {
                c_end = cookie.length;
            }

            return unescape(cookie.substring(c_start, c_end));
        }
    }

    return "";
}

function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection.
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(function () {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie(document.cookie, "csrftoken"));
            }
        }
    });
});
