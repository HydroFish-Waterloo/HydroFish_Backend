# (SRS) Requirement for backend


- [(SRS) Requirement for backend](#srs-requirement-for-backend)
  - [1. for history page](#1-for-history-page)
  - [2. for login](#2-for-login)
  - [3. for registering](#3-for-registering)
  - [4. for set fish level/score](#4-for-set-fish-levelscore)
  

## 1. for history page
History page only get data form backend. 
Request:
```
GET http://localhost:8000/hydrofish/get_history_monthly/
```
Response: the backend will return 30 days of data in the following format.
```
    "status": "success",
    "data": [
        {
            "day": "2024-02-13T00:00:00Z",
            "total_ml": 4328
        },
        {
            ...
        },
        {
            "day": "2024-03-14T00:00:00Z",
            "total_ml": 2062
        }
    ]
```

## 2. for login
The frontend issue a post request:
```
```
The backend will response:
```
```

## 3. for registering
The frontend post a request with username and password
```
```
The backend will response
```
```

## 4. for set fish level/score
