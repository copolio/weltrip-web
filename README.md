# Weltrip

Simple website in Korean that provides various information and data about barrier-free tourism for the disabled visitors to South Korea. All of the data were taken from the Tour API, framework publicly provided by Korea Tourism Organization.

본 프로젝트는 신체적 제약 때문에 자유로운 여행이 어려운 장애인 및 노약자를 대상 으로 여행지에서 불편을 최소화하는 여행 일정을 편리하게 계획하는 것을 주 기능으로 한다. 이를 위해 장애인 및 노약자들이 여행을 하는데 있어 필요로 하는 복지 및 편의시설이 포함된 여행지들을 사용자의 기호에 맞추어 추천해주고, 선택한 여행지들에 대한 최적경 로를 출력해준 후 그곳에 할애할 시간 및 교통수단을 입력받아 일정표 작성을 간소화하여 편리한 여행 계획을 도와주는 무장애 여행 플래너 앱을 구현한다.

## 프로젝트 배경
---
- 무장애 여행이란?
    - 신체적 제약이 있는 장애인 및 노약자들이 불편없이 즐길 수 있는 여행
- 기존에 이미 Tour API의 무장애 여행 데이터셋을 활용한 다양한 포털 존재
    - 단순 여행 정보 제공 서비스
    - 사용자의 기호 등을 고려한 맞춤형 정보를 제공하며 일정 계획까지 도와주는 종합적인 여행 플래너는 전무
    - 공공데이터의 유의미한 활용방안 모색


## 프로젝트 실행
---
1. 본 리포지토리를 fork한다.
2. https://book.coalastudy.com/python-django/week-2/stage-4 <- 다음의 링크를 따라 장고 프로젝트를 빌드 후 실행한다.

## 프로젝트 기능 설명
---

![image](https://user-images.githubusercontent.com/55977034/98628640-64329f00-235a-11eb-94a3-e338a3ccdc90.png)
![image](https://user-images.githubusercontent.com/55977034/98628851-d5725200-235a-11eb-80a5-c8d3ba81117c.png)
![image](https://user-images.githubusercontent.com/55977034/98628857-d7d4ac00-235a-11eb-8633-742b48f59d3a.png)
![image](https://user-images.githubusercontent.com/55977034/98628495-14ec6e80-235a-11eb-9a24-9edeb6f403c4.png)

- 회원가입, 로그인 등 인증 기능
- 마이페이지 등 개인 프로필 관리 기능
- 무장애 여행지 검색 및 추천 기능
- 여행 장소 선택 및 일정 관리 기능
