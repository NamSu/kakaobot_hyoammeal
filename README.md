# 영생 급식봇
> 이 소스는 MIT라이선스 하에 자유롭게 이용할 수 있습니다.

> Fork SerenityS 

### 개발 참고 사이트
* https://github.com/plusfriend/auto_reply
* http://throughkim.kr/2016/07/11/kakao-haksik/
* http://humit.tistory.com/248
* http://sigool.tistory.com/4
* https://github.com/SerenityS/kakaobot_hyoammeal
* etc...

### 플러스 친구 추가
* [@ysmeal](http://pf.kakao.com/_UxcCxlxl) 영생 급식봇

### 개발 환경
* Ubuntu 16.04 
* PyCharm
* Git

### 사용 언어
* Django
* Python + venv

### 필요 모듈
* beautifulsoup4
* urllib
* lxml

# 설치법
## 유의사항
EC2 우분투를 사용시 로케일 문제가 있다.
http://egloos.zum.com/killins/v/3014274를 보고 로케일을 수정하자.

HAProxy가 돌아가는 상황에서의 테스트는 하지 못하였다.
### 1. 기초 패키지 설치
<code>sudo apt-get install python3 python3-pip python3-venv</code>
### 2. Repo 클론 및 이동
<code>git clone https://github.com/NamSu/kakaobot_youngsaengmeal <working_dir> </code>

<code>cd <working_dir></code>
### 3. python 가상환경 구축 및 실행
<pre><code>python3 -m venv (하고싶은 이름)
source (하고싶은이름)/bin/activate
</code></pre>
### 4. python 추가 요구 패키지 설치
<code>pip3 install django lxml beautifulsoup4 python-dateutil</code>
### 5. 첫 마이그레이션 & 실행
<code>python3 manage.py migrate</code>

<code>python3 manage.py runserver host-ip:port</code>
### 5-1. 실행 확인
예를 들어서 실행하면,

<code>python3 manage.py runserver 172.16.0.100:1234</code>

아래와 같이 뜬다면 정상적으로 실행된 것이다.
<pre><code>Performing system checks...
System check identified no issues (0 silenced).
July 26, 2017 - 21:11:31
Django version 1.11.3, using settings 'kakaobot.settings'
Starting development server at http://172.16.0.100:1234/
Quit the server with CONTROL-C.</code></pre>
여의치 않다면 예제처럼 로컬로 실행해서 테스트해도 된다.
### 6. 동작 확인
카카오톡 플러스친구 자동응답 API에선 http://host-ip:port/keyboard/에 대한 Request를 요구한다.

터미널에 <code>curl -XGET 'http://host-ip:port/keyboard/'</code>를 입력해보자.
<pre><code>nys6635@Ubuntu-nys6635:~$ curl -XGET 'http://host-ip:port/keyboard/'
{"type": "buttons", "buttons": ["\uc870\uc2dd", "\uc911\uc2dd", "\uc11d\uc2dd", "\ub0b4\uc77c\uc758 \uc870\uc2dd", "\ub0b4\uc77c\uc758 \uc911\uc2dd", "\ub0b4\uc77c\uc758 \uc11d\uc2dd"]}</code></pre>
정상적으로 작동한다면 이와 같은 정보가 오는것을 확인할 수 있다.

**중요!** 꼭 /keyboard 까지만 입력했을때 정보가 와야한다. 아니면 무수한 에러 메세지만 받을것이다.

또한 keyboard에서 선택한 메뉴의 응답으로 message를 반환하는데 POST형태로 서버로 요구사항을 전달하고  GET으로 정보를 받는다.
 
터미널에 
```
curl -XPOST 'http://host-ip:port/message' -d '{ "user_key": "encryptedUserKey", "type" : "text", "content": "중식"}'
```
  를 입력해보자.
  
  <pre>nys6635@Ubuntu-nys6635:~$ curl -XPOST (...)
{"keyboard": {"type": "buttons", "buttons": ["\uc870\uc2dd", "\uc911\uc2dd", "\uc11d\uc2dd", "\ub0b4\uc77c\uc758 \uc870\uc2dd", "\ub0b4\uc77c\uc758 \uc911\uc2dd", "\ub0b4\uc77c\uc758 \uc11d\uc2dd"]}, "message": {"text": "07\uc6d4 19\uc77c \uc218\uc694\uc77c \uc911\uc2dd \uba54\ub274\uc785\ub2c8\ub2e4. \n \n\ub098\ubb3c\ube44\ube54\ubc25/\uc57d\uace0\ucd94\uc7a5\n\uac10\uc790\ub41c\uc7a5\uad6d\n\uc18c\uc13</pre>
와 같이 반환됨을 확인함으로서 정상 작동함을 알 수 있다.
### 7. 학교 코드 수정
타학교에서 사용하기 위해선 학교 코드 수정이 필요하다.

youngsaengmeal/views.py를 열어보자.
```python
# 타학교에서 이용시 수정
regionCode = 'jbe.go.kr'
schulCode = 'P100000427'
```
라는 코드를 발견할 수 있다.
여기서 regionCode는 각 시도교육청의 주소이며, schulCode는 [링크](http://weezzle.tistory.com/559) 를 참조하도록 하자.
  
### 8. 카카오톡 플러스 친구와 연동
타게시물들을 참조하도록 하자.

처음 입력하는 이름은 서비스 이름이 아니므로 주의 바람.

### 9. crontab을 이용한 주기적 파싱
crontab 은 주기적으로 실행을 시킬수 있도록 하는 도구이다. 자세한 설명은 구글을 찾아보자.

~~~
crontab -e 

# 매주 일요일 04시 10분에 crawl.py 실행 
30 4 * * 7 cd ~/kakaobot_youngsaengmeal &&/usr/bin/python3 ~/kakaobot_youngsaengmeal/youngsaengmeal/crawl.py
~~~

### 10. TODO
학교 시간표 추가

