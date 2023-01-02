import validators


def url_validation(url, url_name="Url", ignore_protocol=False):
    """ Raises an exception if url is not valid.
    """
    if not url:
        raise ValueError("Url is required.")

    if ignore_protocol:
        url_with_protocol = "http://" + url
        if not validators.url(url_with_protocol) and not validators.url(url):
            raise ValueError(f"{url_name} is not valid.")
    else:
        if not validators.url(url):
            raise ValueError(f"{url_name} is not valid.")
