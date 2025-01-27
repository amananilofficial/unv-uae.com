this project requireds python-3.10.4 and redies <br>

py -3.10 -m venv myenv <br>
.\myenv\Scripts\Activate.ps1 <br>
pip install -r requirements.txt <br>
python manage.py collectstatic --clear <br>
python manage.py makemigrations <br>
python manage.py migrate <br>
python manage.py createsuperuser <br>
python manage.py runserver <br>

main url:- http://127.0.0.1:8000/ <br>
admin url:- http://127.0.0.1:8000/admin <br>
