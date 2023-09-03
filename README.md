# Know Your Customer

The design document is here:
https://docs.google.com/document/d/1hrK7GAql40wek73UHXeBJbaNmMzjT_GSP6flwySQsl0/edit?usp=sharing

Project structure:

The `db` directory holds the following:
1. `data.py` - a module that holds the data and acts as a database. In the future this module should be replace by an actual database.
2. `data_access.py` - a module that queries the database

The `instructions` directory holds the instructions for this assignment

The `services` directory holds business logic that is running when the app endpoints are called:
1. `answers.py `- business logic that is related to processing and storing answers in the database
2. `questionnaire.py` - business logic that is related to retrieving the questionnaire

The `utils` directory contain helper classes and methods:
1. `answer_validator.py` - validates the answers retrieved from the save_answer endpoint as requested for the assignment
2. `consts.py` - holds various app consts
3. `enums.py` - holds various enums used in the app
4. `exceptions.py` - holds various exceptions
5. `models.py` - holds definition of app business entities

`main.py `- the main module of the app (the server is awakened through this module)
`tests.py` - API tests, in order to run the tests, navigate to the project root folder and run `pytest tests.py`
