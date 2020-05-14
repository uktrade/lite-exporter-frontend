from applications.services import get_application_countries_and_contract_types


def get_countries_missing_contract_types(request, object_pk):
    return [
        entry["country"]
        for entry in get_application_countries_and_contract_types(request, object_pk)
        if not entry["contract_types"]
    ]


class ContractTypes:
    contract_types = {
        "nuclear_related": "Nuclear-related (trigger list items)",
        "navy": "Navy",
        "army": "Army",
        "air_force": "Air force",
        "police": "Police",
        "ministry_of_interior": "Ministry of Interior (or equivalent)",
        "other_security_forces": "Other security forces",
        "companies_nuclear_related": "Companies requesting Nuclear Trigger List items",
        "maritime_anti_piracy": "Maritime anti-piracy",
        "aircraft_manufacturers": "Aircraft manufacturers, maintainers or operators",
        "registered_firearm_dealers": "Registered firearm dealers",
        "oil_and_gas_industry": "Oil and gas industry",
        "pharmaceutical_or_medical": "Pharmaceutical or medical",
        "media": "Media",
        "private_military": "Private military or security companies (including security transportation)",
        "education": "Education (e.g. schools, colleges and universities)",
        "for_the_exporters_own_use": "For the exporters own use",
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
