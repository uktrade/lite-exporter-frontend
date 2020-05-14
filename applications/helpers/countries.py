from applications.services import get_application_countries_and_contract_types
from lite_content.lite_exporter_frontend.applications import ContractTypes as contractTypeStrings


def get_countries_missing_contract_types(request, object_pk):
    return [
        entry["country"]
        for entry in get_application_countries_and_contract_types(request, object_pk)
        if not entry["contract_types"]
    ]


class ContractTypes:
    contract_types = {
        "nuclear_related": contractTypeStrings.NUCLEAR_RELATED,
        "navy": contractTypeStrings.NAVY,
        "army": contractTypeStrings.ARMY,
        "air_force": contractTypeStrings.AIR_FORCE,
        "police": contractTypeStrings.POLICE,
        "ministry_of_interior": contractTypeStrings.MINISTRY_OF_INTERIOR,
        "other_security_forces": contractTypeStrings.OTHER_SECURITY_FORCES,
        "companies_nuclear_related": contractTypeStrings.COMPANIES_NUCLEAR_RELATED,
        "maritime_anti_piracy": contractTypeStrings.MARITIME_ANTI_PIRACY,
        "aircraft_manufacturers": contractTypeStrings.AIRCRAFT_MANUFACTURERS,
        "registered_firearm_dealers": contractTypeStrings.REGISTERED_FIREARM_DEALERS,
        "oil_and_gas_industry": contractTypeStrings.OIL_AND_GAS_INDUSTRY,
        "pharmaceutical_or_medical": contractTypeStrings.PHARMACEUTICAL_OR_MEDICAL,
        "media": contractTypeStrings.MEDIA,
        "private_military": contractTypeStrings.PRIVATE_MILITARY,
        "education": contractTypeStrings.EDUCATION,
        "for_the_exporters_own_use": contractTypeStrings.FOR_THE_EXPORTERS_OWN_USE,
        "other_contract_type": "",
    }


def prettify_country_data(countries):
    for country in countries:
        pretty_contract_types = []
        if country["contract_types"]:
            for contract_type in country["contract_types"]:
                if contract_type != "other_contract_type":
                    pretty_contract_types.append(ContractTypes.contract_types[contract_type])
            country["contract_types"] = pretty_contract_types
    return countries
