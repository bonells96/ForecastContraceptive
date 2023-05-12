# ForecastContraceptive


We aim to predict consumption (stock_distributed from "train.csv") for 10 contraceptives across 156 health service delivery sites in the public sector health system in Côte D’Ivore. The predictions should be made monthly for three months (July, August, September from 2019). You should give the output of the model you consider to be the best approach in a file with the same format as “SampleSubmission.csv”

The model trained with the best results on the validation set is:

|Model|MSE|mean absolute error|median absolute error| R2 score|
|:----:|:----:|:--------:|:--------------:|:-------:|
|LR|407.33|7.48|1.65|0.49|
|RFR|381.69|6.79|0.14|0.52|

The whole analysis can be encountered in this [notebook](/notebooks/notebook_contraceptives.ipynb)

## Data 

- **contraceptive_logistics_data.csv**: The main dataset, it contains the target to predict: **stock_distributed** other information as the date, the product_code, the site_code and other variables as the stock ordered that day of the product in the site etc....

- **product.csv**:: This dataset maps the product codes to its type of product. For example the product: **AS17005** is a Female Condom.

- **service_delivery_site_data.csv**: This dataset maps the site codes to the type of service, region and district. For example the site code C1399 is a Health Center in Abidjan 2 

## Models

During the 


## Next Steps



## Requirements