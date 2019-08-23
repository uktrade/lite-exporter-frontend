def add_document_data(request):
    files = request.FILES.getlist("file")
    if len(files) is 0:
        return None, 'No files attached'
    if len(files) is not 1:
        return None, 'Multiple files attached'

    file = files[0]
    try:
        original_name = file.original_name
    except Exception:
        original_name = file.name

    data = {
        'name': original_name,
        's3_key': file.name,
        'size': int(file.size / 1024) if file.size else 0,  # in kilobytes
    }
    if 'description' in request.POST:
        data['description'] = request.POST.get('description')

    return data, None
