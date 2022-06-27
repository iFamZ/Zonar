# Zonar

## Publisher class
- Several additional paramters and functions have been added to the publisher class, going beyond what was initially requested. Specifically, the class has two class member variables, namely `data_dict`, a dictionary which is passed to the `publish` function for printing, and another variable `last_ts`, used to hold the last known timestamp prior to `publish` because the `data_dict` is reset after publish. `last_ts` allows us to ensure that data coming in after publish still maintains order.

- In addition to these member variables, several helper methods have been added to print error messages and check for valid data. 