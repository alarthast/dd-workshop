from ehrql import create_dataset
from ehrql.tables.tpp import practice_registrations, vaccinations

study_start_date = "2023-04-01"
study_end_date = "2023-06-30"

covid_vaccinations = (
  vaccinations
  .where(vaccinations.target_disease == "SARS-2 CORONAVIRUS")
  .sort_by(vaccinations.date)
)

spring2023_boosters = covid_vaccinations.where(
    (covid_vaccinations.date >= study_start_date) & 
    (covid_vaccinations.date <= study_end_date)
  ).first_for_patient()


# booster dates
booster_date = spring2023_boosters.date

# registration info as at booster date
registration = practice_registrations.for_patient_on(booster_date)

dataset = create_dataset()

dataset.booster_date = booster_date

dataset.vaccine_type = spring2023_boosters.product_name

dataset.region = registration.practice_nuts1_region_name

dataset.define_population(registration.exists_for_patient())
