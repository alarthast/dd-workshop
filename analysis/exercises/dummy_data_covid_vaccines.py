from ehrql import create_dataset
from ehrql.tables.tpp import practice_registrations, vaccinations
from analysis.supporting_data.vaccine_product_names import COVID_VACCINE_PRODUCT_NAMES, NON_COVID_VACCINE_PRODUCT_NAMES

# study dates from target dataset definition (analysis/dataset_definition_covid_boosters.py)
study_start_date = "2023-04-01"
study_end_date = "2023-06-30"

# use dates one year before/after study dates so we ensure we filter to the right dates
dummy_data_start_date = "2022-04-01"
dummy_data_end_date = "2024-06-30"

covid_vaccinations = (
    vaccinations
    .where(
        vaccinations.target_disease.is_in(["SARS-2 CORONAVIRUS"]).is_not_null()
        & vaccinations.product_name.is_in(COVID_VACCINE_PRODUCT_NAMES).is_not_null()
    )
    .sort_by(vaccinations.date)
)

# Give some options for non-covid diseases so they're not all None
non_covid_vaccinations = (
    vaccinations
    .where(
        vaccinations.target_disease.is_in(["Other disease 1", "Other disease 2"]).is_not_null()
        & vaccinations.product_name.is_in(NON_COVID_VACCINE_PRODUCT_NAMES).is_not_null()
    )
    .sort_by(vaccinations.date)
)

# Find covid and non-covid vaccines with the date range
covid_vaccines_within_dates = covid_vaccinations.where(
    (covid_vaccinations.date >= dummy_data_start_date) & 
    (covid_vaccinations.date <= dummy_data_end_date)
).first_for_patient()

non_covid_vaccines_within_dates = non_covid_vaccinations.where(
    (non_covid_vaccinations.date >= dummy_data_start_date) & 
    (non_covid_vaccinations.date <= dummy_data_end_date)
).first_for_patient()

# Get registrations for both covid and non-covid vaccinations, to use for defining the population
covid_registration = practice_registrations.for_patient_on(covid_vaccines_within_dates.date)
non_covid_registration = practice_registrations.for_patient_on(non_covid_vaccines_within_dates.date)

dataset = create_dataset()
dataset.define_population(covid_registration.exists_for_patient() | non_covid_registration.exists_for_patient())

# Add the region so that it's included in the generated dummy tables
# vaccinations data will be included because it's required for defining the population
dataset.covid_region = covid_registration.practice_nuts1_region_name
dataset.non_covid_region = non_covid_registration.practice_nuts1_region_name

# Increase the populations size as we're generating dummy data in the tables that will
# be excluded by our target dataset definition
dataset.configure_dummy_data(population_size=100)
