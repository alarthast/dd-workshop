from ehrql import create_dataset, months, debug
from ehrql.tables.core import patients, ons_deaths
from ehrql.tables.tpp import apcs, practice_registrations
from itertools import product

# heart failure codes that downstream analyses will look for
HEART_FAILURE_CODES = [
    "I50",
    "I500",
    "I501",
    "I509"
]

# made-up ICD-10-like codes to use as non-heart failure codes
NON_HEART_FAILURE_CODES = [
    ''.join(x) for x in product(["A", "B", "C"], ["0", "1"], ["0", "1", "9"])
]

possible_icd10_codes = HEART_FAILURE_CODES + NON_HEART_FAILURE_CODES
null_cause_of_death = ~ons_deaths.underlying_cause_of_death.is_not_null()

records_start_date = "2021-01-01"
records_end_date = "2024-01-01"

hospitalisations = apcs.where(
    apcs.admission_date.is_on_or_between(records_start_date, records_end_date)
)

dataset = create_dataset()

dataset.define_population(
    ons_deaths.date.is_on_or_between(records_start_date, records_end_date)&
    hospitalisations.exists_for_patient()&
    (ons_deaths.underlying_cause_of_death.is_in(possible_icd10_codes)|null_cause_of_death)
)

dataset.configure_dummy_data(population_size=1000)