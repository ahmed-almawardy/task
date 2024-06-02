# Google Driver Uploader

Simple REST Django app, which provides ability to upload a file to GOOGLE Drive

## Deploy instructions

1. Install all project-dependicies First use command ( make install ) in the bash

   ```bash
   make build
   ```
2. ./manage.py test to run all tests

   ```bash
   ./manage.py test
   ```
3. ./mange.py migrate to run all migration files

   ```bash
   ./manage.py migrate
   ```
4. ./manage.py runserver to run the dev server/ or using gunicorn

   ```bash
   ./manage.py runserver 8000
   gunicorn --threads 1 --workers 1 -b :8000 task.wsgi
   ```

note: Some SENSITIVE data are exposed in the repo as it is a task, so that i made it clear to understant how would everything would work together, in production, ALL SENSITIVE DATA ARE HIDDEN.

## Links

1. To Upload a file  /v1/api/upload-file/
3. Link to Shared Folder in GOOGLE DRIVE
   * https://drive.google.com/drive/u/4/folders/19BpNCXjvL_Abt8_j14Ot4KIvPBbLzlE9

Note:

Uploading Files happens service-less, that means using a file `credentials.json` the authentications happens with Google Drive API, for a current gmail user, the Client/Application keys are saved in file `client_secrets.json`, **the default port for running the server is 8000** you could.

The settings for PyDrive2 are saved in `settings.yaml` file

## Config files

* `settings.yaml`, are the settings for PyDrive
* `client_secrets.json`, Client keys, scope, config to authenticate with google
* `credentials.json`, Gmail user tokens
* `Makefile`, for build the project
* `requirements.in`, Dependencies are used in the project
