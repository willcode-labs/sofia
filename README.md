#### Instalation

1. `$ pip install -r requirements.txt`

#### Tests

* `$ python3 manage.py test api.test --failfast --keepdb --settings api.test.testsSettings -v 3`
* `$ coverage run --source='.' manage.py test api.test --failfast --keepdb --settings api.test.testsSettings -v 3`