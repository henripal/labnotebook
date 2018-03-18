# LabNotebook
### A simple experiment manager for deep learning experiments

`labnotebook` is a package that allows you to flexibly save your experimental data to a postgres database without the hassle of printing outputs.

All you need to do is to modify your code to include `labnotebook.start_experiment()` and `labnotebook.stop_experiment()` and pass the info you would like to save to the database as arguments. As an option, you can save information for each training step by using `labnoteebook.step_experiment()`.

The package exposes the `experiments` and `steps` tables which you can then query using [sqlalchemy](https://www.sqlalchemy.org/)'s rich ORM or traditional SQL text queries.

