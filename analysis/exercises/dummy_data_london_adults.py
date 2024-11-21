from ehrql import create_dataset
from ehrql.tables.core import patients
from ehrql.tables.tpp import addresses


index_date = "2024-01-01"
min_age = 18
max_age = 80

age = patients.age_on(index_date)

dataset = create_dataset()

possible_msoas = ["E02000001", "E02000002", "E02000003", "E02000004"]

address = (
   addresses
   .where(addresses.msoa_code.is_in(possible_msoas))
   .sort_by(addresses.end_date)
   .last_for_patient()
)

no_address = ~addresses.exists_for_patient()

dataset.age = patients.age_on(index_date)
dataset.msoa = address.msoa_code

dataset.define_population(patients.exists_for_patient() & (address.exists_for_patient() | no_address))
