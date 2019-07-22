"""Functions for here Traffic APIs.

See the link https://developer.here.com/documentation for documentation.
"""
import os
from datetime import datetime, timedelta

import json
import requests

class ApiCall(object):
    """Use to call here APIs in python.

    Here's app id and app code must be set as environment variables prior to use.

    Raises
    ------
    KeyError
        If environment variables HERE_APP_ID and HERE_APP_CODE are not
        set.
    """

    def __init__(self):
        try:
            self.app_id = os.environ['HERE_APP_ID']
            self.app_code = os.environ['HERE_APP_CODE']
        except KeyError as e:
            msg = 'App id and app code must be set as environment variables with'
            msg += ' names HERE_APP_ID and HERE_APP_CODE respectively.'
            raise e

    def call_traffic(self, api_name, analyse = False, **kwargs):
        """Call a (old) standard api and return json.

        Parameters
        ----------
        api_name : str
            Name of api
        kwargs
            Keyword arguments where keys are valid parameter names and values
            are valid parameter values as strings for calling <api_name>.

        Returns
        -------
        json object
            Structure of a nested dictionary.

        Examples
        --------
        call_traffic('incidents', center = '50.936123|6.976234', radius = 1)

        Acronyms
        CF: Current flow
        CN: Confidence:
            -1: road closed or unable ot calculate
            0.0-0.5: speed limit
            0.5-0.7: historical speeds
            0.7-1: real time speeds
        FI/FIS: Flow item /List of flow items contiguous in one direction
        JF: Jam factor between 0 (no jam) and 10 (closed)
        SU: Average speed uncut
        SP: Average speed (bounded by speed limit)
        """

        if api_name == 'incidents':
            url = 'https://traffic.api.here.com/traffic/6.3/incidents.json'
        if api_name == 'flow':
            url = 'https://traffic.api.here.com/traffic/6.3/flow.json'

        url += '?app_id={}&app_code={}'.format(self.app_id, self.app_code)

        for key, value in kwargs.items():
            url += '&{}={}'.format(key, value)

        print(url)
        response = requests.get(url)

        if analyse:
<<<<<<< HEAD
            return {'url': url,
                'response': response}

        else:
            return json.loads(response.text)
=======
            return json.loads(response.text)

        else:
            return {'url': url,
                'response': response}
>>>>>>> 9372433236a06152cb12ec4584dbc10aa8f5a0d9
