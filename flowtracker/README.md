## Django
데이터베이스 기반 웹사이트 개발을 위한 오픈소스 파이썬 웹 프레임워크 
웹접속 : 112.216.150.163:8000 

https://user-images.githubusercontent.com/60845730/137613454-7211dcf8-c4b7-414d-8a20-940bf8e0efc8.mov

---

### home page 
📍 프로젝트 이름 입력
<br>
📍 파일선택(로컬에 위치한 input용 비디오 선택)
<br>
📍 분석(slicing code & YOLO v5 & Unet & 2D Depth Map 모델 연동)
<br>
📍 탐지된 결함 이미지 DB에 자동 업로드
<br>
<code/>
$ cd /home/blushy/flowtracker/templates/home.html
</code>
<br>
<code/>
$ cd /home/blushy/flowtracker/flowtracker
</code>
<br>
```
.
├── asgi.py
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-36.pyc
│   ├── models.cpython-36.pyc
│   ├── settings.cpython-36.pyc
│   ├── urls.cpython-36.pyc
│   ├── views.cpython-36.pyc
│   └── wsgi.cpython-36.pyc
├── settings.py
├── test.py
├── urls.py
├── views.py
└── wsgi.py
```

### history page 
📍 번호 : 영상 업로드 순서
<br>
📍 영상 타이틀 : home page에서 설정한 프로젝트 타이틀
<br>
📍 업로드 날짜 & 시간 : 영상을 업로드한 실제 시각
<br>
<code/>
$ cd /home/blushy/flowtracker/tab1/templates/tab1/
</code>
<br>
```
.
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   ├── 0001_initial.py
│   ├── __init__.py
│   └── __pycache__
│       ├── 0001_initial.cpython-36.pyc
│       └── __init__.cpython-36.pyc
├── models.py
├── __pycache__
│   ├── admin.cpython-36.pyc
│   ├── apps.cpython-36.pyc
│   ├── __init__.cpython-36.pyc
│   ├── models.cpython-36.pyc
│   ├── urls.cpython-36.pyc
│   └── views.cpython-36.pyc
├── templates
│   └── tab1
│       └── history.html
├── tests.py
├── urls.py
└── views.py
```

### upload page 
📍 하수관로 결함 분석 결과 업로드 : 해당 일자의 분석 결과를 앨범으로 만들어 한번에 업로드 가능, 유저 이름을 통해 어떤 계정으로 접속하고 있는지 확인 가능
<br>
📍 결함 이미지 업로드 : 기존 앨번에 사진의 추가하고자 할 때 사용 
<br>
<code/>
$ cd /home/blushy/flowtracker/upload
</code>
<br>
```
.
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   ├── 0001_initial.py
│   ├── __init__.py
│   └── __pycache__
│       ├── 0001_initial.cpython-36.pyc
│       └── __init__.cpython-36.pyc
├── models.py
├── __pycache__
│   ├── admin.cpython-36.pyc
│   ├── apps.cpython-36.pyc
│   ├── __init__.cpython-36.pyc
│   ├── models.cpython-36.pyc
│   ├── urls.cpython-36.pyc
│   └── views.cpython-36.pyc
├── templates
│   └── upload
│       └── upload-file.html
├── tests.py
├── urls.py
└── views.py
```

### album & photo page 
📍 앨범 페이지 : 업로드한 앨범 이름과 이미지들 적재, 이미지 클릭하여 상세 정보 확인 가능
<br>
📍 상세 페이지 : 이미지에 대한 상세한 정보 확인 가능
<br>
<code/>
$ cd /home/blushy/flowtracker/photo
</code>
<br>
```
.
├── admin.py
├── apps.py
├── fields.py
├── forms.py
├── __init__.py
├── migrations
│   ├── 0001_initial.py
│   ├── 0002_auto_20210928_2034.py
│   ├── __init__.py
│   └── __pycache__
│       ├── 0001_initial.cpython-36.pyc
│       ├── 0002_auto_20210928_2034.cpython-36.pyc
│       └── __init__.cpython-36.pyc
├── models.py
├── __pycache__
│   ├── admin.cpython-36.pyc
│   ├── apps.cpython-36.pyc
│   ├── fields.cpython-36.pyc
│   ├── forms.cpython-36.pyc
│   ├── __init__.cpython-36.pyc
│   ├── models.cpython-36.pyc
│   ├── urls.cpython-36.pyc
│   └── views.cpython-36.pyc
├── templates
│   └── photo
│       ├── album_change_list.html
│       ├── album_confirm_delete.html
│       ├── album_detail.html
│       ├── album_form.html
│       ├── album_list.html
│       ├── photo_change_list.html
│       ├── photo_confirm_delete.html
│       ├── photo_detail.html
│       └── photo_form.html
├── tests.py
├── urls.py
└── views.py

```

### Dashboard
kibana 접속 : http://112.216.150.163:5601
