def page_range(page, last, span=5):
    """Return a range of page numbers around page, containing span pages
    (if possible). Page numbers run from 1 to last.
    >>> list(page_range(2, 10))
    [1, 2, 3, 4, 5]
    >>> list(page_range(4, 10))
    [2, 3, 4, 5, 6]
    >>> list(page_range(9, 10))
    [6, 7, 8, 9, 10]

    Credit: https://codereview.stackexchange.com/a/92158
    """
    return range(max(min(page - (span - 1) // 2, last - span + 1), 1),
                 min(max(page + span // 2, span), last) + 1)