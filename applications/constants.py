# TODO: fetch this information from API static endpoint

STANDARD_LICENCE = "standard_licence"
OPEN_LICENCE = "open_licence"
HMRC_QUERY = "hmrc_query"
EXHIBITION_CLEARANCE = "exhibition_clearance"
GIFTING_CLEARANCE = "gifting_clearance"
F680_CLEARANCE = "F680_clearance"

CASE_SECTIONS = {
    "HMRC": HMRC_QUERY,
    "F680": F680_CLEARANCE,
    "HAS_LICENCE_TYPE": [STANDARD_LICENCE, OPEN_LICENCE],
    "HAS_TOLD_BY_OFFICIAL": [STANDARD_LICENCE],
    "HAS_GOODS_TYPES": [OPEN_LICENCE, HMRC_QUERY],
    "HAS_COUNTRIES": OPEN_LICENCE,
    "HAS_END_USER": [STANDARD_LICENCE, OPEN_LICENCE, EXHIBITION_CLEARANCE, F680_CLEARANCE, GIFTING_CLEARANCE],
    "HAS_ULTIMATE_END_USERS": [STANDARD_LICENCE, HMRC_QUERY, EXHIBITION_CLEARANCE],
    "HAS_CONSIGNEE": [STANDARD_LICENCE, HMRC_QUERY, EXHIBITION_CLEARANCE],
    "HAS_THIRD_PARTIES": [STANDARD_LICENCE, EXHIBITION_CLEARANCE, F680_CLEARANCE, GIFTING_CLEARANCE],
    "HAS_OPTIONAL_NOTE": [HMRC_QUERY],
}
