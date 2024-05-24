# PROJECT : Share Price Update Project

This Django project is designed to update share prices via API hits efficiently. It utilizes various concurrency techniques such as threading, Celery, and multiprocessing to handle API requests concurrently, ensuring responsiveness and scalability.

The Share Price Update Project automates the process of updating share prices by hitting specific API endpoints. It leverages concurrency techniques to handle a large volume of API requests efficiently, ensuring timely updates and optimal performance.

# FEATURES

- Asynchronously update share prices via API hits
- Utilize threading, Celery, or multiprocessing for concurrent processing
- Monitor task progress in real-time
- Scalable architecture to handle increasing workload

# Requirements
- Django (version 5.0.11)
- Python (version 3.10.13)
- Postgres (database)

# INSTALLATION

To run the Share Price Update Project locally, follow these steps:

1. Create virutalenv
   `virtualenv <environment_name>`
   Note : If virtualenv not installed then  first run `pip install virutalenv`
2. Activate Environment
   - FOR linux 
     `source venv/bin/activate`
   - FOR windows
     `venv\Scripts\activate`
3. Navigate to the project directory: `cd projectsync`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up Django database: 
   `python manage.py makemigrations`
   `python manage.py migrate`

# USAGES

To use the Share Price Update Project:

1. Start the Django development server: `python manage.py runserver`
2. Access the API endpoints to trigger share price updates
3. Monitor task progress using provided API endpoints

# API Endpoints

The following API endpoints are available:

- `/create-shares/`: POST : Initiates the process to create 10000 share  via API hits.
- `/update-share-price/`: POST : Initiates the process to update share prices via API hits.
- `/task-status/<task_id>`: GET : Retrieves the status of a specific task identified by its ID.
- `/share/`: GET : Retrieves all shares created.
- `/share/<share_id>`: GET : Retrieves specific share created.
- `/task/`: GET : Retrieves all task created info.
- `/task/<task_id>`: GET : Retrieves specific task created info.
- `/share-price-update/`: GET : Retrieves all shares_price_updates created.
- `/share-price-update/<share_price_update_id>`: GET : Retrieves specific shares_price_updates created.

# Technologies Used

- Django: Web framework for building the project.
- Celery: Distributed task queue for asynchronous processing.
- Threading: Concurrency technique for handling parallel tasks.
- Multiprocessing: Utilized for concurrent processing of API requests.
- Python: Programming language used for development.

# Test Cases

 1) On Shares :
     This will test all the aspect of share modelviewset (CREATE,GET,UPDATE,POST,)
     `python manage.py test async_app.tests.ShareViewSetTestCase`

 2) On Tasks :
     This will test all the aspect of Task modelviewset (CREATE,GET,UPDATE,POST,)
     `python manage.py test async_app.tests.TaskViewSetTestCase`

 3) On SharePriceUpdate :
     This will test all the aspect of sharepriceupdate modelviewset (CREATE,GET,UPDATE,POST,)
     `python manage.py test async_app.tests.SharePriceUpdateViewSetTestCase`

 4) On Updatingshareprices :
     This will test on proper updating of shares (error_test,)
     `python manage.py test async_app.tests.TestSharePriceUpdate`

 5) On task status:
     This will test on status of task 
     `python manage.py test async_app.tests.TestSharePriceUpdate.test_task_status`

# Dependencies

 -- [file : requirements.txt]
