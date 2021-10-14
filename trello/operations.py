""" Copyright start
  Copyright (C) 2008 - 2021 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

import requests
import json
from connectors.core.connector import get_logger, ConnectorError
from .constants import *

logger = get_logger('trello')


class Trello():
    def __init__(self, config):
        self.server_url = config.get('server_url')
        if self.server_url.startswith('https://') or self.server_url.startswith('http://'):
            self.server_url = self.server_url.strip('/') + '/1'
        else:
            self.server_url = 'https://{0}'.format(self.server_url.strip('/')) + '/1'
        self.api_token = config.get('apiToken')
        self.api_key = config.get('apiKey')
        self.verify_ssl = config.get('verify_ssl')

    def make_api_call(self, method='GET', endpoint=None, params=None, data=None,
                      json=None, flag=False):
        if endpoint:
            url = '{0}{1}'.format(self.server_url, endpoint)
        else:
            url = '{0}'.format(self.server_url)
        logger.info('Request URL {0}'.format(url))
        headers = {"Authorization": "OAuth oauth_consumer_key={0}".format(self.api_key),
                   "oauth_token": "{0}".format(self.api_token), "Accept": "application/json",
                   "Content-Type": "application/json"}
        try:
            response = requests.request(method=method, url=url, params=params, data=data, json=json,
                                        headers=headers,
                                        verify=self.verify_ssl)
            if response.ok:
                result = response.json()
                if result.get('error'):
                    raise ConnectorError('{}'.format(result.get('error').get('message')))
                if response.status_code == 204:
                    return {"Status": "Success", "Message": "Executed successfully"}
                return result
            elif messages_codes[response.status_code]:
                logger.error('{0}'.format(messages_codes[response.status_code]))
                raise ConnectorError('{0}'.format(messages_codes[response.status_code]))
            else:
                logger.error(
                    'Fail To request API {0} response is : {1} with reason: {2}'.format(str(url),
                                                                                        str(response.content),
                                                                                        str(response.reason)))
                raise ConnectorError(
                    'Fail To request API {0} response is :{1} with reason: {2}'.format(str(url),
                                                                                       str(response.content),

                                                                                       str(response.reason)))

        except requests.exceptions.SSLError as e:
            logger.exception('{0}'.format(e))
            raise ConnectorError('{0}'.format(messages_codes['ssl_error']))
        except requests.exceptions.ConnectionError as e:
            logger.exception('{0}'.format(e))
            raise ConnectorError('{0}'.format(messages_codes['timeout_error']))
        except Exception as e:
            logger.exception('{0}'.format(e))
            raise ConnectorError('{0}'.format(e))


def build_payload(params, input_params_list):
    result = {k: v for k, v in params.items() if v is not None and v != '' and k in input_params_list}
    return result


def check_health(config):
    try:
        logger.info("Invoking check_health")
        trello = Trello(config)
        response = trello.make_api_call(method='GET', endpoint='/members/me')
        if response:
            return True
    except Exception as err:
        logger.exception('{0}'.format(err))
        raise ConnectorError('{0}'.format(err))


def get_list(config, params):
    try:
        obj = Trello(config)
        result = build_payload(params, action_input_parameters.get('get_list'))

        response = obj.make_api_call(method='GET', endpoint='/lists/{id}'.format(id=result.get('list_id')))
        return response
    except Exception as err:
        logger.exception('{0}'.format(err))
        raise ConnectorError('{0}'.format(err))


def get_board(config, params):
    try:
        obj = Trello(config)
        result = build_payload(params, action_input_parameters.get('get_board'))

        response = obj.make_api_call(method='GET', endpoint='/boards/{id}'.format(id=result.get('board_id')))
        return response
    except Exception as err:
        logger.exception('{0}'.format(err))
        raise ConnectorError('{0}'.format(err))


def create_label(config, params):
    try:
        obj = Trello(config)
        result = build_payload(params, action_input_parameters.get('create_label'))

        response = obj.make_api_call(method='POST', endpoint='/labels', params=result)
        return response
    except Exception as err:
        logger.exception('{0}'.format(err))
        raise ConnectorError('{0}'.format(err))


def get_label(config, params):
    try:
        obj = Trello(config)
        result = build_payload(params, action_input_parameters.get('get_label'))

        response = obj.make_api_call(method='GET', endpoint='/labels/{id}'.format(id=result.get('label_id')))
        return response
    except Exception as err:
        logger.exception('{0}'.format(err))
        raise ConnectorError('{0}'.format(err))


def create_card(config, params):
    try:
        obj = Trello(config)
        result = build_payload(params, action_input_parameters.get('create_card'))

        payload = {}
        if result:
            if result.get('other_fields'):
                payload.update(result.get('other_fields'))
                result.pop('other_fields')
            payload.update(result)

        response = obj.make_api_call(method='POST', endpoint='/cards', params=payload)
        return response
    except Exception as err:
        logger.exception('{0}'.format(err))
        raise ConnectorError('{0}'.format(err))


def get_card(config, params):
    try:
        obj = Trello(config)
        result = build_payload(params, action_input_parameters.get('get_card'))
        card_id = result.get('card_id')

        payload = {}
        if result:
            if result.get('card_id'):
                result.pop('card_id')
            if result.get('other_fields'):
                payload.update(result.get('other_fields'))
                result.pop('other_fields')
            payload.update(result)

        response = obj.make_api_call(method='GET', endpoint='/cards/{id}'.format(id=card_id), params=payload)
        return response
    except Exception as err:
        logger.exception('{0}'.format(err))
        raise ConnectorError('{0}'.format(err))


def update_card(config, params):
    try:
        obj = Trello(config)
        result = build_payload(params, action_input_parameters.get('update_card'))
        card_id = result.get('card_id')

        payload = {}
        if result:
            if result.get('card_id'):
                result.pop('card_id')
            if result.get('other_fields'):
                payload.update(result.get('other_fields'))
                result.pop('other_fields')
            payload.update(result)

        response = obj.make_api_call(method='PUT', endpoint='/cards/{id}'.format(id=card_id), params=payload)
        return response
    except Exception as err:
        logger.exception('{0}'.format(err))
        raise ConnectorError('{0}'.format(err))


def delete_card(config, params):
    try:
        obj = Trello(config)
        result = build_payload(params, action_input_parameters.get('delete_card'))

        response = obj.make_api_call(method='DELETE', endpoint='/cards/{id}'.format(id=result.get('card_id')))
        return response
    except Exception as err:
        logger.exception('{0}'.format(err))
        raise ConnectorError('{0}'.format(err))


operations = {
    'get_list': get_list,
    'get_board': get_board,
    'create_label': create_label,
    'get_label': get_label,
    'create_card': create_card,
    'get_card': get_card,
    'update_card': update_card,
    'delete_card': delete_card
}
