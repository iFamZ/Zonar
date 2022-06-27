# Zonar

## Publisher class
- Several additional paramters and functions have been added to the publisher class, going beyond what was initially requested. Specifically, the class has two class member variables, namely `data_dict`, a dictionary which is passed to the `publish` function for printing, and another variable `last_ts`, used to hold the last known timestamp prior to `publish` because the `data_dict` is reset after publish. `last_ts` allows us to ensure that data coming in after publish still maintains order.

- In addition to these member variables, several helper methods have been added to print error messages and check for valid data.

## Unittests
- I utilized the Python `unittest` framework to run tests. I have the basic `setUp` and `tearDown` to make some directories, define some paths, and remove them when we are done. In addition, I also utilized additional helper functions:
-- `new_publish` - calls to `publish` are directed here so they can be written to our temp file to be checked against expected output
-- `run_translate` - since we need to constantly call translate and check files, we can instead use this function to not duplicate code
-- `assert_files_match` - function to ensure that the output matches the expected - used mainly in `run_translate`
-- `get_input_data` - reads the input data and returns a python dict

- The input data files are `json` which are structured as `{"type": '[comment on the data]', "data": [{},{},...,{}]}`. The data is a list of `json` objects used to run the unit tests.
- An expected data file should also be written so that the output can be checked against it.
- Note: It is crucial that the expected output looks exactly like the output file, including new line characters. Otherwise, the assertion will not pass and the unit test would be recorded as a failure.

### Cases Tested
- normal, timely data - basic case
- nothing to publish
- out of order data
- overwrite timestamp of old data with new data
- speed first with out of order data, then correct data
- test corrupted data
- test interrupted data (simulated by calling translate function twice with 2 sets of data for before and after the interruption) - also checks the corner case of out of order input data after a published message

## Run/Development Environment
- The code was developed using VSCode2 on macOS Big Sur, along with Python 3.6.10. The development is done with only standard Python packages.

## Class Behavior/Development Notes
- In addition to the notes provided, some assumptions were made in the development as listed below:

-- One Publisher object should be used per device, this ensures that even if messages are interrupted, they can still work as expected.

-- The message will print with either 'None' for speed, or the last known speed, even if it was many messages ago.

-- A speed's timestamp will be used to ensure that newer messages are not out of order.

-- When faced with corrupted data, the message 'Error detected' will be printed out before stopping further stream data processing.