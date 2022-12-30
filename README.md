# YSD

- Pull repo
- make branch

## Getting started

Look at the *runtime.txt* file to see the required python version for this repo.

We use **poetry** to manage our dependencies which simply uses `poetry install` to install the required modules. This can be done after setting up a python interpreter for the required version or automatically done via pycharm by configuring a poetry environment. 

This will install all of the required packages from the *project.toml* file and update them to the version according to the *poetry.lock* file.

You will also need to install **Docker** for pulling the containers required to build this project later on.


## Code standards
We use various python tools to enforce a consistent code style across the app, this helps to ensure that code reviews relate to actual implementation details and don't devolve into quibbling over code style.

The tools we use are as follows
- black
- isort
- flake8 (and friends)

> Before making any changes to the code, you should make sure that you run the above code formatters to fall inline with the typical code standard of this repo.

## Setting up your environment 

In order to run the server, you will need to set up your environment.

### *Setting Up Environment Variables*
The .env.sample file contains useful environment variables that can be considered global for a Developer environment. You should merely need to copy .env.sample to .env and much of the app will work.

You will also need to to setup your personal environment. These are included in the local.env.template or as a block at the top of the .env.sample. You will need to have these set up for you personally, or you can temporarily borrow another developer's.

PyCharm users should update the local.env and add it in addition to the .env, as this makes updates easier. Those who like directly running the app will also find it easier to maintain a local.env and copy it over to the .env during upgrades.

You can have as many *.env files in the project root as you like and git will ignore them, so you can switch local.envs if required.

In addition to these, you will need to set up the `DJANGO_CONFIGURATION` and `DJANGO_SETTINGS_MODULE` variables before running Django. These values tell django (or more specifically django-configurations) which configuration to use, and where to find it. PyCharm users can do this directly in the configuration, while those running them directly can choose to add them to the .env. The values are:

> If you add functionality requiring a new environment variable, make sure to update the sample - this serves as useful documentation for other devs. You should either include a real value or, if the data is sensitive (e.g. credentials) or personal (e.g. points to your personal database) include a dummy value that explains the structure, e.g. `MY_DATABASE_URL=postgres://user:password@some.server.aws.com:5432/ops_your_name

```
DJANGO_SETTINGS_MODULE=core_app.settings
DJANGO_CONFIGURATION=DevLoc
```

## Signing in to Docker and AWS

### *Docker*
To sign into docker using your github credentials create a PAT (Personal Access Token) with the relevant access appropriate on your GitHub account and use it in place of `$GITHUB_TOKEN` and your username for `$GITHUB_USER`:

`echo $GITHUB_TOKEN | docker login docker.pkg.github.com -u GITHUB_USER --password-stdin`


### *AWS Steps*
1. Install **AWS CLI v2** 
2. Run `aws configure sso`
3. Paste https://chetwood.awsapps.com/start/#/ as the start url
4. Select `eu-west-1` 
5. Select `Yobota-Master, cloudmaster+master@yobota.xyz (822386150620)`
6. Select `developers-y`
7. Parameters are `eu-west-2`, `json`, *(your profile name but pressing enter will default it to)* `developers-y-822386150620`
8. Log in to google sso when it shows up and authorise access.
9. Configure the developer environment variables in your *.aws/credentials* file or run `aws configure` and copy them in based off the variables when following the link provided and doing the steps: 

- (*AWS Account (4) -> Yobota-Master -> developers-y -> Command line or programmatic access -> Option 2*)

> After doing this initially and your *.aws/config* and *.aws/credentials* are correct, you can just use your profile tag to log in with the command `aws sso login --profile $YOUR_PROFILE without the need of repeating these steps.` 


10. Finally run `aws ecr get-login-password --region eu-west-2 --profile $YOUR_PROFILE | docker login --username AWS --password-stdin http://822386150620.dkr.ecr.eu-west-2.amazonaws.com/` where *$YOUR_PROFILE* will be stated in the config file. 

*Example:* `aws ecr get-login-password --region eu-west-2 --profile developers-y-822386150620 | docker login --username AWS --password-stdin http://822386150620.dkr.ecr.eu-west-2.amazonaws.com/`



## Docker (pulling the containers and running them)

Once you have logged in to both Docker with GitHub and set up AWS credentials to get access to refdata, you should be able to pull all of the containers without errors.

To do this we can run `docker-compose up` or `docker-compose up -d` if we would like it to run in the background.


## Testing

### *Docker*
To run the scripts to use a test look at the *scripts* file to see which one you would like to run. An example of this is to run the unit tests by running:
`docker-compose exec -T web sh ./scripts/run_unit_tests.sh`


### *PyCharm*
Use the PyCharm extension **EnvFile** to edit the configuration on the test you are trying to run. Select your *.env* file to use (Press the eye symbol to show hidden files) so that the test uses the environment variables you have configured.


## Developing
This section has useful information for during the development process.

## Git
We use git for version control. This allows easy development of the code.

To start working on the code, checkout a new branch:
`
git checkout -b <branch_name>
`

### Naming branches
We've found it useful to use ticket numbers from the JIRA system where possible (e.g. APP-921, CP-1234)

Some branch_names cannot use tickets, especially when merging or releasing to uat, or performing hot bugfixes.
Branches should then be called by saying what it is, the date and then a short description.

So, a uat release branch will look like uat_release_090518_overpayments

## MISC

Running the tests on github
To trigger the workflow on any PR you will have to make a commit that includes 'run tests' in the commit message. This can be done with

`git commit --allow-empty -m 'run tests'` 
which makes an empty commit so that we don't mess with the messages of the normal commits.

If you would like to run only some of the tests you can do:

`git commit --allow-empty -m 'run tests lending/savings/distributors'` 
or u can combine them. e.g:

`git commit --allow-empty -m 'run tests savings distributors'`
For the following branches the workflow will be triggered automatically when a pull request is merged:

future
chetwood-uat
chetwood-production
Unit Tests


Tests can be run internally on PyCharm too. However we have weird and patchy Django support. We're trying to fix this and the easiest way for now is to ask someone how to do it.

The PyCharm test runner at the moment is Unittest.

Important notes
Testing
The settings.TEST_RUNNER value has been deliberately overridden to core_app.setup_helpers.NoDbTestRunner which stops the typical django test database being set up and torn down when manage.py test is called. This is because, in general, Yobota apps should only be using the platform database for functional usecases


## Configuration
Using S3 for Static (served) and Media (uploaded) content
Two further environment variables can be set up to capture S3 buckets used for content management

however the preference is to use WhiteNoise to serve Static files (per the current set up) and S3 for Media

CLIENT_SAVINGS_APP_DOCS_URL : S3 bucket name, used to store static content served by the web page
AWS_ACCESS_KEY_ID: required to access the S3 buckets
AWS_SECRET_ACCESS_KEY: required to access the S3 buckets
reference here:

http://agiliq.com/blog/2014/06/heroku-django-s3-for-serving-media-files/
https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
http://whitenoise.evans.io/en/stable/
https://devcenter.heroku.com/articles/s3
https://devcenter.heroku.com/articles/s3-upload-python
Using Auth0 for access controls
Important
USE_AUTH0_WORKFLOW is required in order to use auth0 as an identity provider.
The following keys are required if the application needs Auth0 for login support

host_organisation_name_AUTH0_CLIENT_ID
host_organisation_name_AUTH0_CLIENT_SECRET
host_organisation_name_AUTH0_DOMAIN
host_organisation_name_AUTH0_CONNECTION The name of the Auth0 remote database for API calls
host_organisation_name_AUTH0_CUST_CALLBACK_URL customer specific callback
These are found on your auth0 application settings. Additionally, the following are useful:

Host_organisation_name_AUTH0_JWT -- required to call the auth0 management API (for user CRUD scopes only)
the AUTH0_CALLBACK_URL must be a full URL: https://app.domain.uk/callback that is set up within your application

Each Host organisation name in order to facilitate different branded emails and branded auth0 widgets, have their own separate Auth0 credentials, i.e. Host_organisation_name_AUTH0_CLIENT_ID would be LIVELEND_AUTH0_CLIENT_ID
