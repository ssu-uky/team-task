
## Skills
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/SQLite-003B57?style=flat&logo=SQLite&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=SQLite&logoColor=white"/>

<br>

## Installation
가상환경 진입 후, 패키지 다운로드

```
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

root 폴더에 `.env` 파일 추가

https://djecrety.ir/ 에서 SECRET_KEY 생성 후 
.env/SECRET_KEY 에 복사

```py
SECRET_KEY="secret-key"
```

<br>

Team 정보 등록하기
```py
python manage.py shell

>>> from tasks.models import Team
>>> from users.models import User

>>> for team_name in User.TeamChoices.values:
...     Team.objects.get_or_create(name=team_name) -> 여기서 탭 하고 써야함
... 
(<Team: Danbi>, True)
(<Team: Darae>, True)
(<Team: BlahBlah>, True)
(<Team: Cheolro>, True)
(<Team: Ddange>, True)
(<Team: Haetae>, True)
(<Team: Supie>, True)

>>> Team.objects.all()

<QuerySet [<Team: Danbi>, <Team: Darae>, <Team: BlahBlah>, <Team: Cheolro>, <Team: Ddange>, <Team: Haetae>, <Team: Supie>]>

>>> exit()
```

<br>

## Test Code

```
pytest
```

<details>

<summary> Test Code - click </summary>

#### user test
```
pytest users/tests.py
```

#### board test
```
pytest tasks/tests.py
```

</details>

<br>
