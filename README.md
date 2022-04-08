### ��� ��������� ������:

����������� ����������� � ������� � ���� � ��������� ������:

```
git clone git@github.com:anotherUser2/api_yamdb.git
```

```
cd api_yamdb
```

C������ � ������������ ����������� ���������:

```
python3 -m venv env
```

```
source env/bin/activate
```

���������� ����������� �� ����� requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

��������� ��������:

```
python3 manage.py migrate
```
��������� ���� ������:

```
python3 manage.py usecsv
```

��������� ������:

```
python3 manage.py runserver
```
�� ������ http://127.0.0.1:8000/redoc/ ����� �������� ������������ ��� YaMDb API. � ������������ �������, ��� ������ �������� ��� API. ������������ ������������ � ������� Redoc.
