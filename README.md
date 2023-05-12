# Forecast Consumption of Contraceptive products


We  predicted a model tp forecast consumption (stock_distributed from "train.csv") for 10 contraceptives across 156 health service delivery sites in the public sector health system in Côte D’Ivore. 

The model trained with the best results on the validation set is:

|Model|MSE|mean absolute error|median absolute error| R2 score|
|:----:|:----:|:--------:|:--------------:|:-------:|
|LR|407.33|7.48|1.65|0.49|
|RFR|381.69|6.79|0.14|0.52|

The whole analysis can be encountered in this [notebook](/notebooks/notebook_contraceptives.ipynb)

To forecast the [sample_submission](/data/SampleSubmission.csv) file run this [script](/forecast_submission_sample.py)
## Data 

- **contraceptive_logistics_data.csv**: The main dataset, it contains the target to predict: **stock_distributed** other information as the date, the product_code, the site_code and other variables as the stock ordered that day of the product in the site etc....

- **product.csv**:: This dataset maps the product codes to its type of product. For example the product: **AS17005** is a Female Condom.

- **service_delivery_site_data.csv**: This dataset maps the site codes to the type of service, region and district. For example the site code C1399 is a Health Center in Abidjan 2 

## Models

Summary of results of the different models trained: 

|Model|MSE|mean absolute error|median absolute error| R2 score|
|:----:|:----:|:--------:|:--------------:|:-------:|
|LR1_exp_1|545.06|9.71|3.66|0.32|
|LR2_exp_1|545.07|9.71|3.66|0.32|
|LR_district_exp_1|545.07|9.71|3.66|0.32|
||
|LR_exp_2|398.68|7.64|2.58|0.51|
|RFR_exp_2|463.07|7.03|0.08|0.43|
|GBR_exp_2|416.98|7.14|1.77|0.48|
||
|LR_exp_3|407.33|7.48|1.65|0.49|
|RFR_exp_3|381.69|6.79|0.14|0.52|

## Next Steps

- Analysis of errors:
    - check what are the time series with the biggest error
    - Look from errors potential ways to enhance the model
- Debug the Neural Network and try more experiments.
- Try model like LSTM that works with sequential data.
- clean the repository


## Requirements


```
matplotlib==3.7.1
numpy==1.24.3
pandas==2.0.1
scikit-learn==1.2.2
scipy==1.10.1
seaborn==0.12.2
torch==2.0.1
tqdm==4.65.0
```