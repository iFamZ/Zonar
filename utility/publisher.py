class Publisher:

    def __init__(self):
        self.data_dict = {
            'latitude': None,
            'longitude': None,
            'speed': None,
            'ts': None
        }
        self.last_ts = None

    def publish(self, message: dict) -> None:
        # publishes messages, assumming it's already implemented
        pass

    def _print_error(self, message: str) -> None:
        '''
        print the error messages as requested
        '''
        print(message)

    def _clear_data_dict(self):
        '''
        resets the class member variable, data_dict, after publishing a message
        '''
        for k in ['latitude', 'longitude', 'ts']:
            self.data_dict[k] = None

    def _valid_data(self, data: dict) -> bool:
        '''
        check that the input stream contains valid keys and data types, if not return false
        '''
        # check the keys
        for k in data.keys():
            if k not in ['ts', 'k', 'v']:
                return False
        # check the value types
        if not isinstance(data['ts'], int):
            return False
        if not isinstance(data['k'], str):
            return False
        if not isinstance(data['v'], str):
            return False
        # check the parameter spelling
        if data['k'] not in ['latitude', 'longitude', 'speed']:
            return False
        return True

    def translate(self, stream_data) -> None:
        # Complete this function. Read in stream_data, publish messages as appropriate, 
        # and store incomplete messages to use in future calls
        for data in stream_data:
            if not self._valid_data(data):
                self._print_error('Error detected')
                return
            data_type = data['k']
            if data_type == 'latitude':
                opp_data_type = 'longitude'
            elif data_type == 'longitude':
                opp_data_type = 'latitude'
            # if one exists and the other is read in
            if data_type in ['latitude', 'longitude'] and self.data_dict[opp_data_type]:
                if data['ts'] == self.data_dict['ts']:
                    # publish + clear
                    self.data_dict[data_type] = data['v']
                    self.last_ts = self.data_dict['ts']
                    self.publish(self.data_dict)
                    self._clear_data_dict()
                elif data['ts'] > self.data_dict['ts']:
                    # overwrite old data
                    self.data_dict[opp_data_type] = None
                    self.data_dict[data_type] = data['v']
                    self.data_dict['ts'] = data['ts']
                else:
                    # out of order
                    self._print_error('Out of order detected')
            elif data_type in ['latitude', 'longitude']:
                if self.last_ts and data['ts'] < self.last_ts:
                    # data coming in is older than previously processed data
                    self._print_error('Out of order detected')
                elif not self.data_dict['ts']:
                    # if no timestamp was recorded (no data has been stored yet)
                    self.data_dict[data_type] = data['v']
                    self.data_dict['ts'] = data['ts']
                elif data['ts'] >= self.data_dict['ts']:
                    # if the new data has a later timestamp - update the data and timestamp
                    # if two same type of data came in with the same ts, then data will be
                    # updated with the later one
                    self.data_dict[data_type] = data['v']
                    self.data_dict['ts'] = data['ts']
                else:
                    # data coming in is older than current data
                    self._print_error('Out of order detected')
            else:
                # data type is speed - matching latitude and longitude will print the last known
                # speed, regardless of how old it is
                if self.data_dict['ts'] and data['ts'] < self.data_dict['ts']:
                    self._print_error('Out of order detected')
                else:
                    self.data_dict[data_type] = data['v']
                    self.data_dict['ts'] = data['ts']