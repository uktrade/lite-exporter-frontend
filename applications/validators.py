def validate_external_location_choice(_request, _pk, json):
    if json.get('choice'):
        return json, 200

    return {'errors': {'choice': ['Select a choice']}}, 400
