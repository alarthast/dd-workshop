from ehrql import create_dataset
from ehrql.tables.core import patients
from ehrql.tables.tpp import addresses

possible_msoas = ["E02000001", "E02000002", "E02000003", "E02000004"]

dataset = create_dataset()
