# MOVIELE

![Documentation](https://img.shields.io/badge/language-2-brightgreen)![Documentation](https://img.shields.io/badge/python-v3.8.2-orange)![Documentation](https://img.shields.io/badge/JS-ES6-orange)![Documentation](https://img.shields.io/badge/node-v12.7.0-orange)![Documentation](https://img.shields.io/badge/vue-@vue/cli/4.4.1-orange)![Documentation](https://img.shields.io/badge/API-2-black)![Documentation](https://img.shields.io/badge/movie-TMDB-blue)![Documentation](https://img.shields.io/badge/video-youtube-blue)

## Link

### Release

:house: MOVIELE​ : https://zen-liskov-8535a3.netlify.app/

:black_large_square: REST API server :  https://finprojectapi.herokuapp.com

### Develop

 :computer: frontend :  https://github.com/YeongbuCha/FinalProjectFront

 :computer: backend :  https://github.com/unani92/FinalProjectAPI



## Introduction

### Description

영화 데이터 기반의 서비스를 만드는 프로젝트로, 기본적인 **영화 목록/ 검색/ 추천 기능**에 더해, **평점/ 리뷰** 등 커뮤니티 기능을 함께 구현했습니다.

### 프로젝트 수행

#### 중점

1. 학습한 내용 최대한 활용 (Django, Vue JS)
2. Github Flow 를 통한 개발
3. Front / Back 업무 분장
4. 끊임없는 소통을 통한 효율적 협업 (Zoom 활용)

#### 내용

1. 모바일 퍼스트 & 반응형 웹 어플리케이션
2. Django 기반의 Class-Based View REST API 서버
3. Vue JS 기반의 Single Page Application

#### 역할분담

| 이름   | 역할분담           |
| ------ | ------------------ |
| 정윤환 | BackEnd repo 담당  |
| 차영부 | FrontEnd repo 담당 |

### 프로젝트 구조

```bash
.
├── BackEnd
│   ├── FinalProjectAPI
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── Procfile
│   ├── accounts
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_auto_20200611_1704.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── community
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_auto_20200611_1724.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── rankcalculate.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── data
│   │   ├── genredata.json
│   │   └── moviedata.json
│   ├── db.sqlite3
│   ├── manage.py
│   ├── requirements.txt
│   ├── runtime.txt
│   └── static
│       ├── admin
│       ├── django_extensions
│       └── rest_framework
├── FrontEnd
│   ├── babel.config.js
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   │   ├── favicon.ico
│   │   └── index.html
│   └── src
│       ├── App.vue
│       ├── assets
│       │   └── logo.png
│       ├── components
│       │   ├── ListView.vue
│       │   ├── PaginatedListView.vue
│       │   └── VideoDetail.vue
│       ├── main.js
│       ├── router
│       │   └── index.js
│       └── views
│           ├── Home.vue
│           ├── accounts
│           │   ├── Login.vue
│           │   ├── Logout.vue
│           │   ├── Profile.vue
│           │   └── Signup.vue
│           └── community
│               ├── articles
│               │   ├── ArticleCreate.vue
│               │   ├── ArticleDetail.vue
│               │   ├── ArticleList.vue
│               │   └── ArticleUpdate.vue
│               └── movies
│                   ├── MovieDetail.vue
│                   ├── MovieList.vue
│                   ├── MovieRecommend.vue
│                   └── MovieSearch.vue
└── README.md
```

### ERD structure
![KakaoTalk_Photo_2020-06-11-15-36-57](https://user-images.githubusercontent.com/53211781/85009825-0bd7e680-b19a-11ea-9221-1e98d1a7d02e.png)


## Development

### Data Scrap

---

> [The Movie Database API](https://developers.themoviedb.org/3/movies/get-popular-movies) 의 영화 데이터를 가져와 사용했습니다.

#### 1. Data 가져오기

- `requests` 패키지를 통해 TMDB API Server 로 요청을 보내고, 응답 결과를 모델링 구조에 맞게 바꾼 후, .json 파일로 저장했습니다.
- 요청

```python
import requests

for page in range(1, 51):
    url = "https://api.themoviedb.org/3/movie/popular?api_key=44084423a3ad71eb2acee3298e9a25e8&language=ko-KR&page=" + str(page)
    res = requests.get(url).json()
    movies = res["results"]
```

- 응답 결과 핸들링

```python
ret = []

for movie in movies:
    # 포스터가 없는 영화 데이터
    if not movie["poster_path"]:
        continue
    # inner dic 객체 내에 필요한 fields 구조로 저장
    inner = dict()
    ret.append(inner)
```

- .json 파일로 저장

```python
import json

file = open("moviedata.json", "w+")
file.write(json.dumps(ret))
```

#### :wrench: Refactoring

- TMDB API 데이터 변화에 대한 대응
  - 매번 데이터를 가져오는 방식이 아니기 때문에, 데이터 변화에 대한 대응 방안이 추가적으로 필요할 것 같습니다.  
  - [TMDB API | Changes](https://developers.themoviedb.org/3/changes/get-movie-change-list) 를 통해 최대 14일간 발생한 영화 데이터 변화를 응답받을 수 있습니다.

#### 2. Data 를 DB에 반영하기

- 반영 전 DB 스키마 생성이 완료되어 있어야 합니다.
- 반영

```
$ python manage.py loaddata data/moviedata.json
```



### Frontend

---

#### App 공통화면

##### 1. Header 및 Nav bar

- `<router-link>` 를 통해각 기능별 페이지와 연결했습니다.

##### 2. Sidebar

- `App.vue` 파일의 data 중 `isSideBar(Bool)` 와 `v-if` 디렉티브를 활용해 Sidebar를 열고 닫았습니다. 이때, Nav bar의 toggle button을 통해 이를 조작할 수 있도록 구현했습니다.
- `App.vue` 파일의 data 중 `isLoggedIn(Bool)` 과 `v-if` 디렉티브를 활용해 Sidebar 내부요소를 다르게 구현했습니다. 이때, `isLoggedIn` 은 `vue-cookies`를 통해 cookie 내에 auth-token 유무를 통해 체크합니다. 

##### :bulb: Point

- 모바일 UX 에 대한 고려
  - 앱을 모바일 상황에 맞춰 개발하려 노력했습니다.
  - 모바일에서는 작은 크기의 버튼을 통해 Sidebar를 닫는 것이 불편할 것이라고 판단하여, 버튼뿐만 아니라 여백을 클릭했을 때에도 Sidebar가 닫히도록 구현했습니다.

#### User 관련 기능

##### 1. Login

- 사용자 입력 데이터를 백엔드 서버로 전송해 로그인합니다. 
- 정상적으로 로그인 되는 경우, 응답에 담긴 토큰을 cookie에 넣고 `isLoggedIn` 데이터를 true로 바꾸며, 현재 유저에 대한 정보를 `currentUser` 데이터에 저장합니다. 

##### 2. Signup

- 사용자 입력 데이터를 백엔드 서버로 전송해 가입을 진행합니다. 
- 정상적으로 가입 되는 경우, 자동 로그인이 되도록 구현했습니다. 

##### 3. Logout 

- Request Header에 Authorization 정보를 담아 백엔드 서버로 전송해 로그아웃합니다. 이때 Authorization 정보는 cookie에 담긴 auth-token을 가져와 사용합니다.
- 정상적으로 로그아웃 되는 경우, cookie에서 auth-token을 삭제하고 `isLoggedIn` 및 `currentUser` 데이터를 초기화 합니다.

##### 4. Profile

- Profile 페이지에서는 해당 유저가 작성한 리뷰들과 좋아요를 누른 리뷰들을 모두 보여줍니다. 이때 리뷰를 클릭하면 해당 리뷰 디테일 페이지로 이동합니다. 

- Sidebar의 My Page를 통해 본인의 프로필 페이지로, 리뷰의 작성자를 클릭해 타인의 프로필 페이지로 갈 수 있습니다. 
- My Page 클릭 시 `currentUser` 의 프로필 페이지로 이동하도록 구현했습니다. 

##### :wrench: Refactoring

- Vuex
  - 앱의 구조가 크게 복잡하지 않다고 판단하여 `props & emit` 을 통해 페이지 혹은 컴포넌트 간 정보를 주고 받도록 구현했습니다. 
  - 그러나 유저 관련 기능 뿐 아니라 커뮤니티 기능 중에서도, 현재 유저 정보가 필요한 경우가 많이 있었습니다.
  - Vuex 를 통해 정보를 중앙화한다면 더 간단하게 전체 기능을 구현할 수 있을 것 같습니다. 

#### Movie 관련 기능

##### 1. 영화 리스트

- DB에 있는 모든 영화를 목록화 하여 보여줍니다. 개별 영화 클릭 시, 해당 영화의 디테일 페이지로 이동합니다.
- 개별 영화 아이템들은 포스터, 평점, 제목, 개봉일의 정보를 포함하고 있습니다. 

##### :bulb: Point

- 반응형 디자인
  - 모바일 화면 뿐 아니라, 데스크탑 등 화면이 커지는 경우에 대해 반응형 디자인을 구현했습니다.
  - 특히 영화 리스트 페이지에서는, 화면이 커지면 row 당 영화 아이템 수가 2개에서 3개로 늘어나도록 구현했습니다. 
- 무한 스크롤 구현
  - 1만 개의 데이터를 초기에 모두 불러오는 경우, 불필요한 데이터 전송으로 인해 비용과 시간이 낭비된다고 판단했습니다.
  - `scrollMonitor` 패키지를 통해, 유저가 현재 데이터들을 모두 본 이후에 새로운 데이터를 요청하여 가져오도록 구현했습니다. 
  - 페이지 최하단에 `bottomSensor` 를 두고, 이 sensor 가 viewport에 들어올 때마다 새로운 axios 요청을 보내는 방식으로 구현했습니다. 

##### :wrench: Refactoring

- 정렬 기준
  - 현재는 `pk` 를 기준으로 영화들을 정렬합니다.
  - 정렬 기준을 유저가 선택할 수 있도록 한다면 더 나은 UX가 가능할 것 같습니다. 

##### 2. 영화 디테일

- 개별 영화의 예고 영상 및 정보들과 해당 영화에 대한 리뷰들을 모아볼 수 있는 페이지입니다. 
- 영화 리뷰들 좌상단에 있는 새글쓰기 버튼을 통해, 해당 영화에 대한 리뷰를 작성할 수 있습니다. 

##### :bulb: Point

- Youtube Data API 활용
  - 영화의 예고 영상을 표시하기 위해 Youtube Data APi를 활용했습니다. 
  - `movie.title` + `"예고편"` 으로 검색한 후 첫번째 영상을 가져오는 방식으로 구현했습니다. 
  - 이때 API KEY는 환경변수에 저장하여 사용했습니다. 

- Pagination 활용
  - 사용자 편의성을 위해 영화 리뷰들의 목록을 Pagination을 통해 구현했습니다.

##### :wrench: Refactoring

- 리뷰 작성 경로
  - 데이터 구조 상, 리뷰 클래스에는 영화가 필수 값으로 지정되어 있습니다. 때문에 영화를 선택한 후에 리뷰를 작성하도록, 영화 디테일 화면에서 리뷰 작성이 가능하도록 경로를 설계했습니다.
  - 리뷰를 작성하는 경로가 리뷰를 읽는 경로와 크게 다르다면 사용자에게 혼란을 줄 수 있다고 생각하지만, 데이터 구조 한계를 해결하는 방법을 찾지 못했습니다.
  - 영화를 포함한 리뷰와 일반 글을 분리하여 모델링하는 방법이 일차적인 해결법이 될 수 있다고 생각합니다. 

##### 3. 영화 추천

- 로그인 한 유저에 한해, 한 편의 영화를 추천해줍니다. 클릭 시 개별 영화 페이지로 이동합니다. 
- 유저의 리뷰 기록을 바탕으로 선호 장르를 파악한 후, 선호 장르 내 영화 한 편을 추천하는 알고리즘을 구현했습니다. 리뷰 기록이 없는 유저의 경우에는 평점이 8점 이상인 영화 중 한 편을 추천합니다. 

##### :wrench: Refactoring

- 추천 퀄리티
  - 추천 알고리즘 상, 리뷰 기록이 없는 유저에게는 커스터마이징 된 추천을 제공할 수 없는 문제가 있습니다.
  - 영화에도 좋아요를 누를 수 있도록 만들고, 가입 직후 단계에서 선호하는 영화에 대한 데이터를 얻는다면 리뷰 기록이 없는 신규회원 등에 대해서도 커스터마이징 된 추천을 제공할 수 있을 것 같습니다.

#### Review 관련 기능

##### 1. 리뷰 리스트

- 전체 리뷰들에 대한 목록 페이지입니다. 개별 리뷰를 클릭하면 해당 리뷰의 디테일 페이지로 이동합니다. 
- Pagination을 통해 구현했습니다. 

##### 2. 리뷰 디테일

- 리뷰 제목, 내용, 영화 제목, 좋아요 개수 등 리뷰 정보와 댓글 목록 및 생성 버튼을 포함합니다.
- `currentUser` 와 `review.user` 가 동일하다면 수정 및 삭제 버튼이 표시됩니다. 이때, 댓글도 마찬가지로 작성자의 경우 삭제 버튼이 표시됩니다.

##### :bulb: Point

- ajax 요청을 통해 좋아요를 구현했습니다. 
- 현재 유저가 좋아요를 아직 누르지 않았다면 좋아요를, 이미 눌렀다면 좋아요 취소를 실행합니다. 



### Backend

---

#### Library

##### JSON serializer

- django rest framework

##### Oauth: Token based Authroization 

- django rest auth
- django all auth

##### CORS policy

- django corsheader

###### API documentation

- drf yasg

#### :bulb: point Class Based View

- django rest framework가 제공하는 `APIView` 클래스를 상속받음으로써 `GET`, `POST`, `PUT`, `DELETE` 요청에 따라 각기 다른 응답을 구현했습니. 
- drf가 제공하는 또 다른 클래스인 `PageNumberPagination` 클래스를 상속받아 pagination과 관련된 기능을 구현했습니다.
- Function Based View에 비해 간결하게 코드를 작성할 수 있었으며, 더욱 **restful한 url 구성**이 가능했습니다.
- exapmle 

```python
from rest_framework.decorators import permission_classes, APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

class ArticleDetail(APIView):
    def get(self, request):
        pass
    @permission_classes([IsAuthenticated])
    def post(self,request,pk):
        pass
```

#### API Guide

:home: https://finprojectapi.herokuapp.com/swagger/

##### 1. Movies: 전체 영화 조회하기, Search: 영화 검색하기

- request : `GET` `/api/v1/community/movies/[?q="keyworkd"]`
- default : 영화의 pk 순서대로 10개의 영화가 출력됩니다. 
- search: 키워드 존재 시(사용자가 search 메뉴를 통해 영화를 검색 시) 파라미터에 담긴 키워드가 제목에 포함된 영화를 출력합니다.
- :bulb: Point pagination
  -  `/?page=<int:pk>` : 한 페이지에 10개씩 영화를 담았고 스크롤이 아래로 내려갈 때 마다 페이지 수가 1씩 늘어나면서 새로운 영화 10개가 조회됩니다. 
- response : 

```json
[
  {
    "id": 339095,
    "genres": [{"id": 1,"name": "horror"},{"id": 3,"name": "adventure"},{...}...],
    "title": "The Last Days of American Crime",
    "overview": "일주일 후면 ...",
    "poster_path": "/ygCQnDEqUEIamBpdQdDYnFfxvgM.jpg",
    "release_date": "2020-06-05",
    "popularity": 122.637,
    "vote_count": 114,
    "vote_average": 5.6,
    "adult": false,
    "articles": []
  },
  {...},
  {...},
   ...
]
```

##### 2. Home: Best 2 Movies, 2 Articles

- request: `GET` `/api/v1/community/movies/home/` , `/api/v1/community/articles/home/`
- usage
  - 요청 시 `popularity`를 기준으로 **가장 높은 순위를 기록한 영화 2개를 추출**해 홈 화면에 노출시키기 위해 영화 2개를 응답한다. 
  - 요청 시 **"좋아요"를 가장 많이 기록한 게시글 3개**를 홈 화면에 노출시키기 위해 게시글 3개를 응답한다.  

##### 3. Community: 모든 게시글 조회하기

- request: `GET`  `/api/v1/community/articles/`
- response

```json
[
    {
      "id": 4,
      "movie": {...},
      "user": {...},
      "title": "좋아요 2개",
      "content": "달린 글을\r\n작\r\n성\r\n중\r\n입\r\n니\r\n다",
      "rank": 3,
      "created_at": "2020-06-14T15:06:48.704752+09:00",
      "updated_at": "2020-06-14T15:06:48.704798+09:00",
      "like_users": [{...}],
      "comments": [{...},{...},...]
    }, {...}, {...}, {...}
]
```

##### 3-1. Community: 개별 게시글 조회하기

- request: `GET` `/api/v1/community/articles/<int:article_pk>/`
- usage: 개별 **아티클의** id 넘버를 통해 개별 아티클의 모든 정보를 조회 가능

##### 3-2. 개별 게시글 생성하기 

- request: `POST` `/api/v1/community/articles/<int:movie_pk>/`
- usage: 해당 영화에 대한 리뷰를 작성하기 위해 **영화의** id 넘버를 통해 POST 요청을 전송

##### 3-3. 개별 게시글 수정하기

- request: `PUT` `/api/v1/community/articles/<int:article_pk>/`
- usage: 해당 영화에 대한 리뷰를 작성하기 위해 **게시글의** id 넘버를 통해 PUT 요청을 전송

##### 3-4. 개별 게시글 삭제하기

- request: `DELETE` `/api/v1/community/articles/<int:article_pk>/`
- usage: 해당 영화에 대한 리뷰를 작성하기 위해 **게시글의** id 넘버를 통해 PUT 요청을 전송

##### :bulb: Point 3-5. 아티클 생성,수정,삭제 시 평점 업데이트

- usage
  - 사용자가 새로운 게시글을 작성하거나 수정 및 삭제 시 영화의 평점에 반영되는 구조입니다. 
  - 게시글과 관련된 영화의 평점 정보와 평점에 참여한 사람 수를 불러와 사용자가 새롭게 업데이트 하는 내용을 반영해 영화 데이터를 수정하는 방식입니다. 
- `rankcalculate.py`

```python
class RankCalculate:
    def __init__(self, query, request):
        self.query = query
        self.request = request

    def AddNewRank(self):
        pass
    def UpdateNewRank(self,prev_rank):
        pass
    def DeleteRank(self,prev_rank):
        pass
```

- 사용 예시

```python
# 새 글 작성 
new_rank = RankCalculate(movie,request)
new_rank.AddNewRank()

# 기존 글 수정 및 삭제 
article = get_object_or_404(Article, pk=pk)
prev_rank = article.rank
new_rank = RankCalculate(article,request)
new_rank.UpdateNewRank(prev_rank) # 수정
new_rank.DeleteRank(prev_rank) # 삭
```

##### :bulb: Point 3.6. 게시글(댓글) 작성자 본인만 수정 및 삭제 허용하기

> 프론트 단에서 게시글 및 댓글 작성자가 본인이 아닐 경우 사용자 뷰에서 보이지 않게 로직을 구현했으나
> 포스트맨이나 swagger 등을 통해 요청을 보낼 경우 막을 수 없다는 문제가 발생한다. 
> 이를 보완하기 위해 백앤드에서 게시글 작성자가 **본인이 아닐 경우 401 unauthorized 메시지를 출력**하게 구현하였다. 

- 사용 예시

```python
if request.user.username == article.user.username:
            ...
    return Response(serializer.data)
else :
    return Response({
        "msg":"401 unAuthorized 잘못된 접근입니다.",
        "articleUser": article.user.username,
        "requestUser": request.user.username
    })
```

##### 4. Community: 댓글 작성하기

- request: `POST` `/api​/v1​/community​/articles​/<int:article_pk>​/comments​/`
- usage: **게시글** id 넘버를 통해 게시글에 달리는 댓글 작성 요청 가능

##### 4-1. Community: 댓글 삭제하기

- request: `DELETE` `/api​/v1​/community​/articles​/<int:comment_pk>​/comments​/`
- usage: **댓글** id 넘버를 통해 게시글에 달리는 댓글 삭제 요청 가능

##### 5. Community: 좋아요 및 취소

- request: `GET` `/api/v1/community/articles/<int:article_pk>/likes/`
- usage: GET 요청 전송 시 좋아요를 누른 유저인지 확인을 한 이후 좋아요를 눌렀을 경우 눌렀음을, 반대의 경우도 마찬가지의 정보를 응답
- response

```json
{
    "liked": boolean,
    "count": Number
}
```

##### 6. For You : 영화 추천 알고리즘

- request: `GET` `/api/v1/community/movies/recommend/`
- description
  - 요청을 보내면, 백엔드에서 추천 알고리즘을 통해 **한 편의 영화**를 응답
  - :bulb: Point
    - 선호 장르 기반의 영화 추천
      - 유저의 리뷰 기록을 통해 선호 장르를 파악
      - 선호 장르의 영화 중 하나를 추천
      - 리뷰 기록이 없는 유저의 경우, 평점이 8 이상인 영화 중 하나를 추천

##### 7. 회원정보 조회하기

- request: `GET` `/api/v1/accounts/`
- description : GET 요청을 통해 현재 로그인한 유저의 정보를 응답
- :bulb: Point

> 요청을 통해 받은 응답을 Vue instance의 데이터에 담아둔다. 
> 이를 통해 로그인 시와 비로그인 시의 사용자 뷰를 다르게 보여줄 수 있으며
> 게시글(댓글)을 본인만 수정 및 삭제 기능에 접근할 수 있게 한다.

##### 7-1. MyPage: 개별 회원정보 조회하기

- request: `GET` `/api/v1/accounts/<int:user_pk>/`
- description : GET 요청을 통해 해당 id 넘버를 가진 유저의 정보를 응답
- :bulb: Point

> 마이페이지에서 해당 유저가 작성한 게시글과 좋아요를 남긴 글들을 모두 불러올 수 있게 한다.

#### :wrench: Refactoring

##### 1. 정교한 모델링의 필요성

JSON resopnse에 넣어서 보내주어야 할 것들에 대한 정리가 명확하지 못하였기 때문에 프론트엔드 측의 요구사항을
처음부터 다 반영하지 못하는 일이 자주 발생하였습니다. 
예를 들어 프론트에서 영화정보를 요청 영화정보를 담아서 응답을 받을 수 있도록 serializer를 설계했지만,
프론트는 영화정보 안의 게시글도 원하는 상황이었습니다. 하지만 응답 JSON에는 게시글 정보가 들어있지 않았던 것과 같은 문제들의 연속이었습니다. 

따라서 프론트 측의 요청에 따라 serializer를 재설계해야 했고 이러한 일들이 프로젝트 내내 발생했습니다. 
헤로쿠 배포를 몇번 업데이트 했나 보았더니 프로젝트 6일차 기준으로 22번의 업데이트를 해야 했습니다. 

이를 통해 프론트엔드 개발자와 백앤드 개발자가 협업을 할 때 **어느 부분에 중점을 두고 소통을 해야 하는지**를 배울 수 있었습니다. 

##### 2. JWT 인증 방식의 사용

OAUTH 방식의 인증 방식을 통해 유저 정보를 가져오고 로그인 여부를 식별했지만 JWT 인증 방식을 시도하지 못했다는 점이 아쉬웠습니다. 
프론트에서 사용자 정보를 응답받는 GET 요청을 보내면 유저 정보를 JSON에 담아서 보냈지만 JWT 방식을 통해 더욱 보안이 우수한 응답을 구현하지 못했기 때문입니다. 