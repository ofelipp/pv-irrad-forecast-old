# What is it?

Module "forecast" destinated to make predictions irradiance from photovoltaic
modules based on metereological features.

This can be used on two types of prediction:
* Hour prediction
* Day prediction

In any of these scenarios, will be received a `json` file containing the hour
to be predicted or the list of the hour.

# How it works?

The forecast service will receive a `Data` object containing the values from
each meteorological feature for hour in predict range. The processed Data
object will look like:

```python
Data(
    data=[[0, 1, 2, 3, 4, 5]],
    name="hour_x",
    description="description for this data"
)
```