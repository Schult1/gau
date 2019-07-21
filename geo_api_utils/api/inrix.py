"""Functions for INRIX Traffic APIs.

See the link http://docs.inrix.com for documentation.
Json usage is recommended.
"""
import os
from datetime import datetime, timedelta

import json
import requests


class ApiCall(object):
    """Use to call INRIX APIs in python.

    Vendor and consumer ids must be set as environment variables prior to use.

    Raises
    ------
    KeyError
        If environment variables INRIX_VENDOR_ID and INRIX_CONSUMER_ID are not
        set.
    """

    def __init__(self):
        try:
            self.vendor_id = os.environ['INRIX_VENDOR_ID_TGR']
            self.consumer_id = os.environ['INRIX_CONSUMER_ID_TGR']
        except KeyError as e:
            msg = 'Vendor and consumer ids must be set as environment variables with'
            msg += ' names INRIX_VENDOR_ID and INRIX_CONSUMER_ID respectively.'
            raise e
        self.ex_time = datetime.now() - timedelta(hours=1)

    @staticmethod
    def get_token_and_server_path(self, region):
        """Get authentication token and server url path for future api calls.

        Parameters
        ----------
        region : str
            Must be either 'NA' or 'EU'.

        Returns
        -------
        token : str
            Authentication token to call apis.
        server : str
            The base url used to call apis.
        ex_time : datetime
            Date when token will expire.
        """
        if hasattr(self, 'server') and hasattr(self, 'token') and self.ex_time > datetime.now():
            print('Token and server path already retrieved and are still valid.')
            return None

        if region not in ('NA', 'EU'):
            raise ValueError('This region does not exist; use NA or EU.')

        url = 'http://na-api.inrix.com/Traffic/Inrix.ashx?Action='
        url += 'GetSecurityToken&VendorId={0}&ConsumerId={1}&Format=JSON'
        url = url.format(self.vendor_id, self.consumer_id)

        token_response = requests.get(url)
        token_json = json.loads(token_response.text)

        if region.lower() == 'na':
            server = token_json['result']['serverPaths'][0]['serverPath'][0][
                'href'
            ]
        else:
            server = token_json['result']['serverPaths'][1]['serverPath'][0][
                'href'
            ]
        token = token_json['result']['token']

        ex_time = datetime.now() + timedelta(hours=1)

        self.token = token
        self.server = server
        self.ex_time = ex_time

        print('Token will become invalid in 1 hour.')
        return token, server, ex_time


    def call_standard(self, region, api_name, use_json=True, **kwargs):
        """Call a (old) standard api and return json.

        Parameters
        ----------
        api_name : str
            Name of
        kwargs
            Keyword arguments where keys are valid parameter names and values
            are valid parameter values as strings for calling <api_name>.

        Returns
        -------
        json object
            Structure of a nested dictionary.

        Examples
        --------
        >>> from tgr_trips_utils.api import inrix
        >>> api = inrix.ApiCall()

        1. Get a list of incidents within a lat-long box.
        >>> api.call_standard('EU', 'GetSegmentSpeedinRadius',
                                Radius='1.5',
                                Center='51.328444|6.568134',
                                LocRefmethod='XD')
        """
        self.get_token_and_server_path(self, region)

        url = self.server + '?Action={}'.format(api_name)
        if use_json:
            url += '&Format=JSON'

        url += '&Token={}'.format(self.token)
        done_args = set(('action', 'format'))

        for key, value in kwargs.items():
            if key.lower() in done_args:
                continue
            url += '&{}={}'.format(key, value)

        response = requests.get(url)
        if use_json:
            return json.loads(response.text)
        else:
            return response.text

    def call_parking(self, region, api_name, use_json=True, **kwargs):
        """Call a (old) standard api and return json.

        Parameters
        ----------
        api_name : str
            Name of
        kwargs
            Keyword arguments where keys are valid parameter names and values
            are valid parameter values as strings for calling <api_name>.

        Returns
        -------
        json object
            Structure of a nested dictionary.

        Examples
        --------
        >>> from tgr_trips_utils.api import inrix
        >>> api = inrix.ApiCall()

        1. Get a list of incidents within a lat-long box.
        >>> api.call_standard('EU', 'GetSegmentSpeedinRadius',
                                Radius='1.5',
                                Center='51.328444|6.568134',
                                LocRefmethod='XD')
        """
        self.get_token_and_server_path(self, region)
        self.webtoken = self.token

        url = self.server + '?Action={}'.format(api_name)
        if use_json:
            url += '&Format=JSON'

        url += '&Token={}'.format(self.token)
        done_args = set(('action', 'format'))

        for key, value in kwargs.items():
            if key.lower() in done_args:
                continue
            url += '&{}={}'.format(key, value)

        response = requests.get(url)
        if use_json:
            return json.loads(response.text)
        else:
            return response.text
