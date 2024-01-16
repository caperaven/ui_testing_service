# Installing and running

1. Clone repo to your local machine
2. Create a virtual environment and activate it
3. Install the requirements
4. Run the app

## Clone repo to your local machine

```bash
git clone https://github.com/caperaven/ui_testing_service.git
```

## Create a virtual environment and activate it

```bash
python -m venv venv 


source venv/bin/activate
or 
./venv/scripts/activate
```

## Install the requirements

```bash
pip install -r requirements.txt
```

If you are running the update and you get some wheel errors just run the pip install commands manually.

## Installing selenium drivers.

To run the selenium tests you need to install the drivers for the browsers you want to test with.
You can see more instructions about it here: https://github.com/caperaven/py_process/blob/main/notebooks/selenium/chrome.ipynb

## Run the app

```bash
python main.py
```


