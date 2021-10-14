""" Copyright start
  Copyright (C) 2008 - 2021 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

messages_codes = {
    400: 'Invalid input',
    401: 'Unauthorized: Invalid credentials',
    500: 'Invalid input',
    404: 'Invalid input',
    'ssl_error': 'SSL certificate validation failed',
    'timeout_error': 'The request timed out while trying to connect to the remote server. Invalid Server URL.'
}

action_input_parameters = {
    "get_list": ["list_id"],
    "get_board": ["board_id"],
    "create_label": ["name", "color", "idBoard"],
    "get_label": ["label_id"],
    "create_card": ["idList", "name", "desc", "other_fields"],
    "get_card": ["card_id", "other_fields"],
    "update_card": ["card_id", "name", "desc", "other_fields"],
    "delete_card": ["card_id"]

}


