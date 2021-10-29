def trolly_contents(request):

    trolly_items = []
    trolly_count = 0

    context = {
        'trolly_items': trolly_items,
        'trolly_count': trolly_count,
    }

    return context
