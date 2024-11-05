def add_hashtags(tags: str) -> str:
    """
    This function adds hashtags to the given string.

    Args:
        tags (str): The string to which hashtags will be added.

    Returns:
        str: The string with added hashtags.
    """
    hashtags: list[str] = tags.replace(',', '').split(' ')
    hashtags = ['#' + tag for tag in hashtags]
    return ' '.join(hashtags)