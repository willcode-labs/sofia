#### Instalation

1. `$ pip install -r requirements.txt`
2. `$ python3 makemigrations api --check`
2. `$ python3 migrate api`

#### Tests

* `$ python3 -Wall manage.py test api.test --failfast --keepdb --settings api.test.testsSettings -v 3`
* `$ coverage run --source='.' manage.py test api.test --failfast --keepdb --settings api.test.testsSettings -v 3`
