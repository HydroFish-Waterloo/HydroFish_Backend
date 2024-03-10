
# How to generate date in the library 


Run this Django python command in the backend (where the `manage.py` file lies):
```
$ python manage.py generate_water_intake_data
```
It will return this if everything is ok.
```
Successfully generated water intake data for one month.
```

# Use Postman to test it

| Topic | Picture|
|:---|---|
|If there is **NO history data** in the database <br> It will return message as this.| ![nodata](./pictures/10.png)|
| You have to **login before getting any data**, first is to get the **token**.| ![gettoken](./pictures/11.png)|
| Get 3-days history data <br> Remember to put the token in Header| ![get3days](./pictures/12.png)|
|Get weekly (7days) history data  <br> Remember to put the token in Header| ![get7days](./pictures/13.png)|
|Get monthly (30days) history data  <br> Remember to put the token in Header| ![get30days](./pictures/14.png)|