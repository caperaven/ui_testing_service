# Installing and running

1. Clone repo to your local machine
2. Create a virtual environment and activate it
3. Install the requirements
4. Set up drivers
5. Setting up the basic URLs for the app
6. Run the app

## Clone repo to your local machine

```bash
git clone https://github.com/caperaven/ui_testing_service.git
```

## Create a virtual environment and activate it

```bash
python -m venv venv
.\venv\Scripts\activate
```

## Install the requirements

```bash
pip install fastapi
pip install uvicorn
pip install selenium
pip install pandas
pip install matplotlib
pip install aiofiles
pip install psutil
```

## Set up drivers
1. You need to make sure that you have a folder in the root of the project called "chrome". In that folder you need two things.

    1.1 copy of the chrome driver

    1.2 copy of the chrome binary

You can download both at: https://googlechromelabs.github.io/chrome-for-testing/#stable Make sure you download both as win64.
2. Extract the chromedriver.exe into the chrome folder.
3. Extract the contents of the chrome-win64.zip into the chrome folder.

The ui_testing_service/chrome folder should now contain the chrome exe and supporting files along with the chromedriver exe. You can download a newer version if you wish, but you should make sure that you download both the chrome and driver for the same version and extract them into the chrome folder.

## Setting up the basic URLs for the app
1. Navigate to the ui_testing_service/config folder.
2. Open up the servers.json file.
3. Copy the below structure into the file and save it.
4. You can add as many servers as you want. The text is what will be displayed in the dropdown and the value is the URL that will be used. Just use the same convention.
```json
[
    {
        "text": "localhost",
        "value": "https://localhost:1100/"
    },
    {
        "text": "google",
        "value": "https://www.google.com"
    },
    {
        "text": "onkey-local",
        "value": "https://localhost:1100/contoso/test/"
    },
    {
        "text": "onkey-daily",
        "value": "https://onkeydev.pragmaproducts.com/contoso/daily/"
    }
]

```

## Run the app

```bash
python main.py
```
1. In the terminal, you will see the URL that you can use to access the app. CTRL - click on the URL to open it in your browser.
2. Once the URL has opened, you can add "/index.html" to the end of the URL to open the app.

