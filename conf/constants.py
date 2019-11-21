ISO8601_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'
NEWLINE = '\n'

# URLs
APPLICATIONS_URL = '/applications/'
APPLICATION_SUBMIT_URL = '/submit/'
CASES_URL = '/cases/'
GOODS_URL = '/goods/'
DOCUMENTS_URL = '/documents/'
END_USER_DOCUMENT_URL = '/end-user/document/'
ULTIMATE_END_USER_URL = '/ultimate-end-user/'
CONSIGNEE_URL = '/consignee/'
CONSIGNEE_DOCUMENT_URL = '/consignee/document/'
THIRD_PARTIES_URL = '/third-parties/'
DOCUMENT_URL = '/document/'
GOODSTYPES_URL = '/goodstypes/'
GOODSTYPE_URL = '/goodstype/'
GOODSTYPE_COUNTRY_URL = '/assign-countries/'
USERS_URL = '/users/'
ORGANISATIONS_URL = '/organisations/'
EXTERNAL_LOCATIONS_URL = '/external_locations/'
SITES_URL = '/sites/'
ROLES_URL = '/roles/'
NOTIFICATIONS_URL = USERS_URL + 'notifications/'
CLC_NOTIFICATIONS_URL = USERS_URL + 'clc-notifications/'
AUTHENTICATION_URL = USERS_URL + 'authenticate/'
CASE_NOTES_URL = '/case-notes/'
ECJU_QUERIES_URL = '/ecju-queries/'
ADDITIONAL_DOCUMENT_URL = '/documents/'
MANAGE_STATUS_URL = '/status/'
EXPORTER_USERS_PERMISSIONS_URL = ORGANISATIONS_URL + "permissions/"

# Queries URLs
QUERIES_URL = '/queries/'
CONTROL_LIST_CLASSIFICATIONS_URL = QUERIES_URL + 'control-list-classifications/'
END_USER_ADVISORIES_URL = QUERIES_URL + 'end-user-advisories/'

# Static URLs
STATIC_URL = '/static/'
UNITS_URL = STATIC_URL + 'units/'
COUNTRIES_URL = STATIC_URL + 'countries/'
CONTROL_LIST_ENTRIES_URL = STATIC_URL + 'control-list-entries/'

# Applications constants
STANDARD_LICENCE = 'standard_licence'
OPEN_LICENCE = 'open_licence'
HMRC_QUERY = 'hmrc_query'

# Case statuses
READ_ONLY_STATUSES = ['finalised', 'under final review', 'under review', 'withdrawn']

APPLICANT_EDITING = 'applicant_editing'

NOT_STARTED = 'not_started'
IN_PROGRESS = 'in_progress'
DONE = 'done'
SUPER_USER_ROLE_ID = "00000000-0000-0000-0000-000000000003"
DEFAULT_USER_ROLE_ID = "00000000-0000-0000-0000-000000000004"


class Permissions:
    EXPORTER_ADMINISTER_ROLES = 'EXPORTER_ADMINISTER_ROLES'
    ADMINISTER_SITES = 'ADMINISTER_SITES'
    ADMINISTER_USERS = 'ADMINISTER_USERS'
    SUBMIT_CLEARANCE_APPLICATION = 'SUBMIT_CLEARANCE_APPLICATION'
    SUBMIT_LICENCE_APPLICATION = 'SUBMIT_LICENCE_APPLICATION'

    MANAGE_ORGANISATION_PERMISSIONS = [
        ADMINISTER_SITES,
        ADMINISTER_USERS,
        EXPORTER_ADMINISTER_ROLES
    ]
