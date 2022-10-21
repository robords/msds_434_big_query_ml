# msds_434_big_query_ml

To copy the files from another folder, run, for example:    
`bash copy_script.sh ../cloud_weather_predictions/cloud_weather_predictions/`


## Data
We can also get it from AWS: https://docs.opendata.aws/noaa-ghcn-pds/readme.html 

__Key Abbreviations (per AWS documentation):__
* PRCP = Precipitation (tenths of mm)
* SNOW = Snowfall (mm)
* SNWD = Snow depth (mm)
* TMAX = Maximum temperature (tenths of degrees C)
* TMIN = Minimum temperature (tenths of degrees C)


Q-FLAG is the measurement quality flag. 
There are fourteen possible values, but the following is the one I'd filter for:

* Blank = did not fail any quality assurance check

Examples for this dataset:
https://github.com/GoogleCloudPlatform/training-data-analyst/blob/master/blogs/ghcn/ghcn_on_bq.ipynb

