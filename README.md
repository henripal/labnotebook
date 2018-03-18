# LabNotebook
## A simple experiment manager for deep learning experiments

`labnotebook` allows you to:
- flexibly save **all** your experimental data in a postgres database through a very simple interface
- monitor **any** indicators from your running experiments by streaming them through a web application
![](./nbs/img/labnotebook.gif)
- access all this data forever through the web app, through [sqlalchemy](https://www.sqlalchemy.org/), or through traditional sql text queries.

All you need to do is to modify your code to include `labnotebook.start_experiment()` and `labnotebook.stop_experiment()` and pass the info you would like to save to the database as arguments. As an option, you can save information for each training step by using `labnotebook.step_experiment()`.

You can see a very simple example notebook [here](./nbs/example_usage.ipynb).

