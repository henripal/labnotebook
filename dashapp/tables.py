import xpbase

db_string = "postgres://postgres:1418@localhost/experiments"
experiments, steps = xpbase.initialize(db_string)

