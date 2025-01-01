
## Tests, linters and code coverage

To run the test suite:

    python manage.py test

To run the test suite and get code coverage statistics:

    coverage run manage.py test
    coverage report

To generate HTML reports, run this and open `htmlcov/index.html`
afterwards:

    coverage html

To format the code automatically using `black`, run it
from the project root directory:

    black .

To check for common programming errors or style problems,
run `ruff` linter in the project root directory:

    ruff --fix .

To automatically run `black` (formatting), `ruff` (linter)
and `isort` (sort/format package imports) on every git
commit, set up a git `pre-commit` hook:

    pre-commit install

Note that you'll need to have initialized your git repository for
the git pre-commit hook to be available. To test it without installation,
you can run:

    pre-commit run --all-files

## Docker support

Build the docker image with:

        docker build -t user-registration-and-profile-customization .

The default command is to start the web server (gunicorn). Run the image
with `-P` docker option to expose the internal port and check the exposed
port with `docker ps`:

        docker run --env-file .env --P user-registration-and-profile-customization
        docker ps

Make sure you provide the correct path to the env file (this example assumes
it's located in the local directory).

To run a custom command using the image (for example, db migrations):

        docker run --env-file .env user-registration-and-profile-customization python manage.py migrate

To run a Django shell inside the container:

        docker run --env-file .env -t user-registration-and-profile-customization

Note that any changes inside the container will be lost. For that reason,
running `collectstatic` or using a SQLite database within a container will
have no effect. If you want to use SQLite with docker, mount a docker
volume and place the SQLite database inside it.

For more information on the docker build process, see the included `Dockerfile`.
