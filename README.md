# TinyURL External API Adapter
This service will provide and API to create and manage short urls with
[TinyURL](https://tinyurl.com/). You should visit
[TinyURL](https://tinyurl.com/) website and create an account. After that, get
a token and use that to create or manage your short urls with this service.
Please note that some features are only available in the paid version of
TinyURL. [More information is available here](https://tinyurl.com/app/pricing).

## Managing the Environment and Dependencies
To start working, first install `virtualenv` with pip.
```bash
pip install virtualenv
```

Then create an empty virtual environment.
```bash
virtualenv .venv
```
Note that `.venv` is the name of the virtual environment directory, this
directory is omitted in the `.gitignore` file.

After creating the virtual environment, activate it.

UNIX based Operating Systems (GNU/Linux, macOS, etc.)
```bash
source .venv/bin/activate
```

Windows
```batch
.\venv\Scripts\activate
```

Now you can install the required python packages in the clean environment you
just created.
```bash
pip install -r requirements.txt
```

This will only install `flask` and its dependencies. If you need other
packages, you need to install them with `pip install` first, and then update
the `requirements.txt` file with this command.
```bash
pip freeze > requirements.txt
```
Be careful not to update `requirements.txt` outside the virtual environment,
since every python package you have installed on your computer will be added
to the requirements of the project.

## Running the Service

After installing `flask` and its dependencies from `requirements.txt` file,
you can go to the `app` folder and run the app with this command.
```
flask --app main --debug run
```
