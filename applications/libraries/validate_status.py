def check_all_parties_have_a_document(parties):
    if not parties:
        return None

    for party in parties:
        if not party:
            return None

        if not party['document']:
            return 'in_progress'

    return 'done'
