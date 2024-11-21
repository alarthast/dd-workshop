from ehrql import create_dataset
from ehrql.tables.core import patients

index_date = "2020-03-31"

dataset = create_dataset()

age = patients.age_on(index_date)

dataset.define_population((age > 18) & (age < 80))
dataset.age = age
dataset.sex = patients.sex
