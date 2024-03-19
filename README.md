# Social network

The project is a social network and has standard functionality:
- registration / authorization
- creating / deleting a group, as well as joining / leaving them
- create / delete / edit records
-system of likes, friends (subscribers), comments
- changing profile information
- etc.

P.S.
To draw rating stars, it is recommended to add a couple of instances of the RatingStar class through the admin panel.

### Launch of the project

#### 1) clone the repository
```
git clone https://github.com/Lanterman/-social-network.git
```
#### 2) Create and run docker-compose
```
docker-compose up --build
```
#### 3) Follow the link in the browser
```
http://127.0.0.1:8000/
```

P.S.

Celery is currently down due to security issues with Gmail.

P.S.S.
Work for the future

1. Include coresheaders, drf_yasg
2. Set up user JWTTokens
3. Set up OAuth2
