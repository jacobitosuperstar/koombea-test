# koombea-test
Test for the Senior Python Developer Role

# CHEATED
Added and fixed some stuff after I said it was done. The last commed is titled
CHEAT, so you can discard it if you like.

1. There where context errors regarding the relative imports. Tried not to use
   relative imports, but they fizzle out when the Package Name and structure
   changes within the docker container. For example, RestAPI package exits
   within the realm of the project, but when only the contents of the folder
   are in the container, the root package name dissapears, needing everything
   a relative import instead of a Named import. **TLDR**: Tests weren't running
   inside the container, as the RestAPI app doesn't exists within the name
   space.
2. Added the tests to the `test_main.py` file within the NotificationProducer
   folder. The issue with testing directly within the pytest client, is that
   pytest creates another client that doesn't have a space shared with the main
   application. This means that when we try to update existing records within
   the Test app, it cannot be done, as the worker only interacts with the main
   application. So for the tests to work, everything needs to be running within
   the main application. **TLDR**: Added tests in the `test_main.py` file. They
   must be ran inside the docker container with everything running.

## INDEX

- [ARCHITECTURE OVERVIEW](#architecture-overview)
  - [BACKEND](#backend)
  - [DATABASE](#database)
  - [TESTING](#testing)
  - [FILE STRUCTURE](#file-structure)
- [SET UP](#set-up)
  - [RUNNING THE APP](#running-the-app)
  - [RUNNING THE TESTS](#running-the-tests)
    -[RestAPI](#restapi)
    -[Notification](#notification)
  - [API DOCUMENTATION](#api-documentation)

# ARCHITECTURE OVERVIEW
As the test suggested the main idea was to create a backend with a simple in
memory storage with a connection to an asyncronous worker.

## BACKEND
Nothing too exceptional really. Used threaded version of FastAPI to simplify
the code complexity within the RabbitMQ connection and the database creation.
Even though Pika does support full async Python, there are other considerations
to do within your code to work like that. The performance gains are only there
if you go all in with the async architecture, while threads allow a more
simplified and partial approach to the problem.

## DATABASE
For the storage of events, there was nothing fancy done. Created different
TypedDicts to structure the different request, responses and intermediary
states of the data. TypedDict is great, because that allows full Data
Validation support from the FastAPI/Pydantic side of things, while still having
all the simplicity of a dictionary. And all of the events are being stored
within a list, that uses a Lock to support thread safe operations and parallel
execution of tests.

## TESTING
For the testing I opted for a more modern approach, where we just feed to the
test function a bunch of json files, and they are just automatically created
and ran. For memory constraints, you could create several test_<abc>.py files,
so that the list of events created doesn't become too long, but those are not
problems within this implementation.

## FILE STRUCTURE
the folder structure follows a more classic Model View Controller style, like
moving closer to a Django Like structure. I have found this to be best, as if
in the future, bottlenecks of the application require separation into different
services, the refactor needed to move away the logic of one module to its own
singular service, minimal.

# SET UP

## RUNNING THE APP

To use the application having Docker installed in your computer is a must, and
you can download it from this [link][1]

to run the application locally, from the command line you can run the command
`docker-compose up` from this directory. To run the application as a background
or detached from the terminal window, you can run the command
`docker-compose up -d` or `docker-compose up --detach`.

To run commands inside the `web` service container you can run this while the
application is running.

There is also a Makefile on which the running and stopping commands are
simplified. But for all intents and purposes we can ignore that file.

`docker-compose exec web /bin/bash`

With this you will be able to be in the server environment and run the
different commands needed for the tests.

## RUNNING THE TESTS

### RestAPI
To run the tests, you have to enter to the bash environment in the `web`
service container, and now in that bash environment run `pipenv run pytest . -v
-s` to execute all the tests.

The tests to be executed they don't need a connection to rabbitMQ as in the
functionality there is an automatic check for connection. To run the tests
outside of the Docker container, you just need to have pipenv installed in
your machine and then run `pipenv install` to install all the packages and
generate the virtual environment, and then run `pipenv run pytest . -v -s` to
run all of them locally.

### Notification
To run the tests, you have to enter to the bash environment in the `worker`
service container, and now in that bash environment run `pipenv run pytest . -v
-s` to execute all the tests. All the containers must be running for this to
work.

## API DOCUMENTATION

The api documentation would be in the `http://localhost:8000/docs`.

[1]: https://www.docker.com
