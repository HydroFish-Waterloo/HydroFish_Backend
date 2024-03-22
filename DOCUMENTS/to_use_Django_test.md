
Reference:
https://www.django-rest-framework.org/api-guide/testing/


To run the test, use the Django test command:
```bash
python manage.py test -v 1
```
> The `-v 1` is for more details displayed, usage: `-v {0,1,2,3}`. 




| Function to be tested|  Method | Stratage |
|:--| :--| :--|
|login| UserAccountTests| BlackBox Mostly|
|register| UserAccountTests | BlackBox Mostly|
|record_intake |WaterIntakeTests | Combined |
|get_3days_water_intake| GetWaterIntakeTests | Path Coverage |
|get_weekly_water_intake| GetWaterIntakeTests| Path Coverage|
|get_monthly_water_intake| GetWaterIntakeTests | Path Coverage |
|GetFishNumber | GetFishNumberTests | Path Coverage|
|level_up| |LevelUpTests | Path Coverage|
|set_settings| SettingsTests | Path Coverage|
|get_settings| SettingsTests |Path Coverage|