# Yonder
Yonder Integrated Self-Driving Laboratory Software Suite

### Run Application
- Clone repository
- Add your database `credentials.json` to the root of the project folder
- Cd into the root folder
- Download dependencies by running `poetry update`
- Run `poetry run python app.py` to run the program

### Run Tests
- Cd into the root folder
- Download dependencies by running `poetry update --with dev`
- Run `poetry run python -m pytest tests` to run the tests

### Build Application (WIP)
- Cd into the root folder
- Download dependencies by running `poetry update --with build`
- Run `poetry run build` to build the application
- Run the application from `app` in the `dist` directory
