# (SRS) Requirement for backend


- [(SRS) Requirement for backend](#srs-requirement-for-backend)
  - [1. for history page \[tested\]](#1-for-history-page-tested)
  - [2. for login](#2-for-login)
  - [3. for registering](#3-for-registering)
  - [4. for set fish level/score \[tested\]](#4-for-set-fish-levelscore-tested)
    - [case 1](#case-1)
    - [case 2](#case-2)
    - [case 3](#case-3)
    - [case 4](#case-4)
  - [5. for recording intake in main page \[tested\]](#5-for-recording-intake-in-main-page-tested)
  - [6. for settings page \[tested\]](#6-for-settings-page-tested)
  

## 1. for history page [tested]
History page only `GET` data form backend. 
| Endpoint | Input | Output|
|:--|:--|:--|
|GET <br> http://localhost:8000/hydrofish/get_history_monthly/ | not needed | the backend will return 30 days of data in the following format.

Example:
> ![historypage](/DOCUMENTS/pictures/14.png)


Return data format:
```json
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
users/api/login/
    username:arthur2
    password:147258@@@
```
The backend will response:
```json
{
    "token": "dfcd5e3ace8157a95fb38c2098e5f568234e4396",
    "username": "arthur2"
}
```
>![register](/DOCUMENTS/pictures/71.png)


## 3. for registering
The frontend post a request with username and password
```
users/api/register/
    username:arthur30
    password1:147258@@@
    password2:147258@@@
```
The backend will response
```json
{
    "token": "2728cc03c4939fb103c31618e3ab2ca55392b1f2",
    "username": "arthur30"
}
```
>![register](/DOCUMENTS/pictures/72.png)

## 4. for set fish level/score [tested]
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
> ![case21](/DOCUMENTS/pictures/42.png)

'level' must be a value >= 1.
> ![cass22](/DOCUMENTS/pictures/31.png)

### case 3
If you provide a 'level' higher than the data in database, your 'level' parameter will updata the corresponding one in database.
> ![case3](/DOCUMENTS/pictures/33.png)

### case 4
If you provide a 'level' lower than the data in database, your request will still be accepted, also backend will tell you the current level value.
> ![case4](/DOCUMENTS/pictures/41.png)


## 5. for recording intake in main page [tested]

```
hydrofish\recordintake
      -H "Authorization: Token YOURTOKEN" \
      -d '{"data": 2048-03-30, "water_amount": 300}'
```

> ![record](/DOCUMENTS/pictures/51.png)


## 6. for settings page [tested]
Backend has two endpoints for frontend:
|Endpoint  | Input  | Output |
|:--|:--|:--|
|/getsettings/ | not needed | return data like: {"wakeup_time": "07:00:00", "sleep_time": "23:00:00","interval": 30 }
|/setsettings/ | new data like: {"wakeup_time": "07:00:00", "sleep_time": "23:00:00","interval": 30 } | "status": 'success' (or 'error')

**Examples**  


[1] When there is no data in database, an error will return
> ![get-error](/DOCUMENTS/pictures/61.png)

[2] Setting data to backend
> ![set-ok](/DOCUMENTS/pictures/62.png)

[3] Getting data from backend
> ![get-ok](/DOCUMENTS/pictures/63.png)

