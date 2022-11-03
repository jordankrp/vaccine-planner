# vaccine-planner

To run this application, first create a virtual environment and install the requirements (use Python 3.7 or later):

```shell
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r ./requirements.txt
```

Then run the REST API Flask application by running `python3 restful_api.py` on one terminal. In order to interact with the API, you can run the `python3 user_interface.py` program on another terminal. This will provide some options to the user, like viewing an existing booking, requesting a new one, modifying or deleting. The unit tests need to run while the API server is running, by opening another terminal and running `python3 unit_tests.py`. They are a few of the edge cases that could occur and they are also integrated in the CICD pipeline that you can find in `.github/workflows/main.yml`. The CICD pipeline is implemented through Github Actions upon pushing or requesting to merge with the master branch.
