# (SRS) Requirement for backend


- [(SRS) Requirement for backend](#srs-requirement-for-backend)
  - [1. for history page](#1-for-history-page)
  - [2. for login](#2-for-login)
  - [3. for registering](#3-for-registering)
  - [4. for set fish level/score](#4-for-set-fish-levelscore)
    - [case 1](#case-1)
    - [case 2](#case-2)
    - [case 3](#case-3)
    - [case 4](#case-4)
  

## 1. for history page
History page only get data form backend. 
Request:
```
GET http://localhost:8000/hydrofish/get_history_monthly/
```
Response: the backend will return 30 days of data in the following format.

> ![historypage](/DOCUMENTS/pictures/14.png)

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
Endpoint:
```
hydrofish\levelup
      -H "Authorization: Token YOURTOKEN" \
      -d '{"level": 2}'
```
### case 1
If you don't provide the 'level' parameter, you get an error.
>![case1](/DOCUMENTS/pictures/32.png)

### case 2
If you don't give the right 'level' data, an error raises.
> ![case21](/DOCUMENTS/pictures/22.png)

'level' must be a value >= 1.
> ![cass22](/DOCUMENTS/pictures/31.png)

### case 3
If you provide a 'level' higher than the data in database, your 'level' parameter will updata the corresponding one in database.
> ![case3](/DOCUMENTS/pictures/33.png)

### case 4
If you provide a 'level' lower than the data in database, your request will still be accepted, also backend will tell your the current level value.
> ![case4](/DOCUMENTS/pictures/34.png)
