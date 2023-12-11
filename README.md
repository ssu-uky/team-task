
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

### user test
```
pytest users/tests.py
```

### board test
```
pytest tasks/tests.py
```

</details>


<br>


## API Reference

<details>

<summary> Users - click </summary>

### 1. 회원가입 - `POST`
http://127.0.0.1:8000/api/v1/users/signup/

**Request**
```py
{
    "username":"toto",
    "password":"qpqp1010",
    "team":"Supie"
}
```

**Response**
```py
{
    "user_pk": 7,
    "username": "toto",
    "team": "Supie",
    "message": "Supie 팀의 toto님, 회원가입이 완료되었습니다."
}

# 팀을 입력하지 않으면 default 값으로 Danbi 팀으로 배정됩니다.
```

---

### 2. 로그인 - `POST`
http://127.0.0.1:8000/api/v1/users/login/

**Request**
```py
{
    "username":"toto",
    "password":"qpqp1010"
}
```

**Response**
```py
{
    "user_pk": 7,
    "username": "toto",
    "team": "Supie",
    "message": "Supie 팀의 toto님, 로그인되었습니다."
}
```

---

### 3. 로그아웃 - `POST`
http://127.0.0.1:8000/api/v1/users/logout/

```py
{
    "message": "로그아웃 하시겠습니까?"
}
```

```py
{
    "message": "로그아웃되었습니다."
}
```

</details>


<details>

<summary> Tasks - click </summary>

### 1. task 등록 (Create Task) - `POST`
http://127.0.0.1:8000/api/v1/tasks/create/

**Request**

```py
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "title과 content를 입력해주세요."
}
```

```py
{
    "title":"task 제목",
    "content":"task 내용"
}
```

**Response**
```py
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "pk": 4,
    "create_user": "toto",
    "team": "Supie",
    "title": "task 제목",
    "content": "task 내용",
    "created_at": "2023-12-12 00:42:48"
}
```

---

### 2. task list 조회 (Task List) - `GET`
(모든 task 리스트 조회- subtask 제외 / 내 팀이 포함되어있지 않더라도 조회가능)
<br>
http://127.0.0.1:8000/api/v1/tasks/

```py
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "task_pk": 1,
        "team": "Danbi",
        "title": "popo titee",
        "is_complete": false,
        "total_subtasks": 0
    },
    {
        "task_pk": 3,
        "team": "Haetae",
        "title": "두번째 제목",
        "is_complete": false,
        "total_subtasks": 4
    },
    {
        "task_pk": 4,
        "team": "Supie",
        "title": "task 제목",
        "is_complete": false,
        "total_subtasks": 0
    }
]
```

---

### 3. my task list (My Team Task List) - `GET`
#### 내 팀이 포함된 모든 task, subtask 리스트 조회
<br>
http://127.0.0.1:8000/api/v1/tasks/myteam/

```py
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "tasks": [ # task에 포함되어 있을 경우
        {
            "task_pk": 4,
            "team": "Supie",
            "title": "task 제목",
            "is_complete": false,
            "total_subtasks": 0
        }
    ],
    "subtasks": [ # subtask에 포함되어 있을 경우
        {
            "task_team": "Haetae",
            "task_pk": 3,
            "subtask_pk": 2,
            "team": [
                "Danbi",
                "Supie"
            ],
            "sub_title": "두번째 제목",
            "is_complete": false
        },
        {
            "task_team": "Haetae",
            "task_pk": 3,
            "subtask_pk": 7,
            "team": [
                "Supie"
            ],
            "sub_title": "하위 제목",
            "is_complete": true
        }
    ]
}
```

---

### 4. task 상세 조회, 수정, 삭제 (Task Detail) - `GET` , `PUT` , `DELETE`
http://127.0.0.1:8000/api/v1/tasks/<int:task_pk>/
http://127.0.0.1:8000/api/v1/tasks/3/

```py
HTTP 200 OK
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "task": {
        "task_pk": 3,
        "total_subtasks": 4, # 3번 task에 할당 된 subtask는 4개
        "team": "Haetae",
        "create_user": "happy",
        "title": "두번째 제목",
        "content": "agsdgdsdsg",
        "is_complete": false,
        "completed_date": null,
        "created_at": "2023-12-10 04:47:29",
        "modified_at": "2023-12-12 00:48:38"
    },
    "subtask": [
        {
            "task_team": "Haetae",
            "subtask_pk": 2,
            "team": [
                "Danbi",
                "Supie"
            ],
            "sub_title": "두번째 제목",
            "sub_content": "해태팀이 수정함",
            "is_complete": false,
            "completed_date": null
        },
        {
            "task_team": "Haetae",
            "subtask_pk": 3,
            "team": [
                "Danbi"
            ],
            "sub_title": null,
            "sub_content": "sagsdgds",
            "is_complete": false,
            "completed_date": null
        },
        {
            "task_team": "Haetae",
            "subtask_pk": 7,
            "team": [
                "Supie"
            ],
            "sub_title": "하위 제목",
            "sub_content": "하위 내용",
            "is_complete": true,
            "completed_date": "2023-12-10 22:34:01"
        },
        {
            "task_team": "Haetae",
            "subtask_pk": 8,
            "team": [
                "Danbi"
            ],
            "sub_title": "ddd",
            "sub_content": "eeee",
            "is_complete": false,
            "completed_date": null
        }
    ]
}
```

```py
HTTP 200 OK
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "task": {
        "task_pk": 4,
        "total_subtasks": 2,
        "team": "Supie",
        "create_user": "toto",
        "title": "task 제목",
        "content": "task 내용",
        "is_complete": true,
        "completed_date": "2023-12-12 01:17:15",
        # task에 할당 된 모든 subtask가 is_complete == true 가 되는 시점에 task의 completed_date의 시간이 생성됩니다.
        "created_at": "2023-12-12 00:42:48",
        "modified_at": "2023-12-12 01:17:15"
    },
    "subtask": [
        {
            "task_team": "Supie",
            "subtask_pk": 9,
            "team": [
                "Danbi",
                "BlahBlah"
            ],
            "sub_title": "sub title 을 지정합니다",
            "sub_content": "sub content를 작성합니다.",
            "is_complete": true,
            "completed_date": "2023-12-12 01:17:15"
        },
        {
            "task_team": "Supie",
            "subtask_pk": 10,
            "team": [
                "Cheolro",
                "Ddange"
            ],
            "sub_title": "새로운 제목을 지정합니다",
            "sub_content": "새로운 내용을 작성합니다.",
            "is_complete": true,
            "completed_date": "2023-12-12 01:12:44"
        }
    ]
}
```

#### PUT
```py
HTTP 403 Forbidden
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "작성자만 수정할 수 있습니다."
}

# "create_user": "happy" 
# 작성자는 happy이므로 happy만 수정이 가능합니다.
```

#### DELETE
```py
HTTP 403 Forbidden
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "작성자만 삭제할 수 있습니다."
}

# "create_user": "happy" 
# 작성자는 happy이므로 happy만 수정이 가능합니다.
```

---

### 5. task의 새로운 subtask 등록 (New Subtask) - `POST`
http://127.0.0.1:8000/api/v1/tasks/4/subtasks/new/
http://127.0.0.1:8000/api/v1/tasks/<int:task_pk>/subtasks/new/

**Request**
```py
{
    "sub_title":"sub title 을 지정합니다",
    "sub_content":"sub content를 작성합니다.",
    "team":[
        "Danbi","BlahBlah"
        ]
}
```

**Response**

```py
{
    "subtask_pk": 9,
    "team": [
        "Danbi",
        "BlahBlah"
    ],
    "sub_title": "sub title 을 지정합니다",
    "sub_content": "sub content를 작성합니다.",
    "is_complete": false,
    "completed_date": null
}
```

**task의 팀원이 아닌 경우**
```py
HTTP 403 Forbidden
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "팀원만 등록할 수 있습니다."
}
```

---

### task에 할당 된 subtask 목록 조회 (Subtask List) - `GET`
http://127.0.0.1:8000/api/v1/tasks/4/subtasks/
http://127.0.0.1:8000/api/v1/tasks/<int:task_pk>/subtasks/

```py
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "task_team": "Supie",
        "subtask_pk": 9,
        "team": [
            "Danbi",
            "BlahBlah"
        ],
        "sub_title": "sub title 을 지정합니다",
        "sub_content": "sub content를 작성합니다.",
        "is_complete": false,
        "completed_date": null
    },
    {
        "task_team": "Supie",
        "subtask_pk": 10,
        "team": [
            "Cheolro",
            "Ddange"
        ],
        "sub_title": "새로운 제목을 지정합니다",
        "sub_content": "새로운 내용을 작성합니다.",
        "is_complete": false,
        "completed_date": null
    }
]
```

---

### task에 할당 된 subtask의 내용 상세조회, 수정, 삭제 (Subtask Detail) - `GET`, `PUT`, `DELETE`
http://127.0.0.1:8000/api/v1/tasks/4/subtasks/9/
http://127.0.0.1:8000/api/v1/tasks/<int:task_pk>/subtasks/<int:subtask_pk>/

```py
HTTP 200 OK
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "task_team": "Supie",
    "subtask_pk": 10,
    "team": [
        "Cheolro",
        "Ddange"
    ],
    "sub_title": "새로운 제목을 지정합니다",
    "sub_content": "새로운 내용을 작성합니다.",
    "is_complete": false,
    "completed_date": null
}
```

#### PUT
**Request**
```py
{"is_complete": true}

# PUT, DELETE는 task_team, subtask team만 가능
```

**Response**
```py
HTTP 200 OK
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "task_team": "Supie",
    "subtask_pk": 10,
    "team": [
        "Cheolro",
        "Ddange"
    ],
    "sub_title": "새로운 제목을 지정합니다",
    "sub_content": "새로운 내용을 작성합니다.",
    "is_complete": true, # 수정됨
    "completed_date": "2023-12-12 01:12:44" # is_complete 가 true로 변경 된 시간으로 설정
}
```

#### DELETE
```py
HTTP 403 Forbidden
Allow: GET, PUT, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "완료된 SubTask는 삭제할 수 없습니다."
}

# task의 팀원과, subtask에 할당 된 팀원이라도 완료 된 subtask는 삭제할 수 없습니다.
```

</details>