from ehrql import create_dataset
from ehrql.tables.core import patients
from ehrql.tables.tpp import addresses


index_date = "2024-01-01"
min_age = 18
max_age = 80

age = patients.age_on(index_date)

dataset = create_dataset()

london_msoa = (
    addresses
    .where((addresses.msoa_code == "E02000001").is_not_null())
   .sort_by(addresses.end_date)
   .last_for_patient()
)

dataset.define_population((age >= min_age) & (age <= max_age) & london_msoa.exists_for_patient())
dataset.msoa = london_msoa.msoa_code

