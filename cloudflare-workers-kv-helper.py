#!/usr/bin/python

import sys
import json
import getpass
import requests
from builtins import input

API_BASE = 'https://api.cloudflare.com/client/v4/accounts/'

def select_namespace(account_id, headers) :

    namespaces = requests.get(
        API_BASE + account_id + '/storage/kv/namespaces',
        headers=headers
    ).json()


    print('Here are your KV namespaces: ')

    for namespace in namespaces['result']:
        print(namespace['title'] + ' - ID: ' + namespace['id'])

    namespace_id = input("Enter your namespace ID: ")

    print('Namespace is set to: ' + namespace_id)

    print('---')

    return namespace_id

def get_keys(account_id, namespace_id, headers) :

    get_keys = requests.get(
        'https://api.cloudflare.com/client/v4/accounts/' + account_id + '/storage/kv/namespaces/' + namespace_id + '/keys',
        headers=headers
    ).json()

    keys = get_keys['result']

    return keys

def list_keys(account_id, namespace_id, headers) :

    keys = get_keys(account_id, namespace_id, headers)

    for key in keys:

        key_name = key['name']

        print(key['name'])

        print('---')

def list_keys_values(account_id, namespace_id, headers) :

    keys = get_keys(account_id, namespace_id, headers)

    for key in keys:

        key_name = key['name']

        get_key_value = requests.get(
            API_BASE + account_id + '/storage/kv/namespaces/' + namespace_id + '/values/' + key_name,
            headers=headers
        )

        print(key['name'] + ' - ' + get_key_value.text)

        print('---')

def delete_all(account_id, namespace_id, headers) :

    keys = get_keys(account_id, namespace_id, headers)

    for key in keys:

        key_name = key['name']

        get_key_value = requests.delete(
            'https://api.cloudflare.com/client/v4/accounts/' + account_id + '/storage/kv/namespaces/' + namespace_id + '/values/' + key_name,
            headers=headers
        )

    print('All keys deleted')
    print('---')

def run(account_id, namespace_id, headers) :
    print('How you want to proceed?')
    print('0 - Exit')
    print('1 - List Keys')
    print('2 - List Keys/Values')
    print('3 - Switch Namespace')
    print('4 - Delete All Keys')
    print('---')

    choice = input("Enter your choice: ")

    if( choice == '1' ) :

        list_keys(account_id, namespace_id, headers)

    if( choice == '2' ) :

        list_keys_values(account_id, namespace_id, headers)

    elif( choice == '3' ) :

        namespace_id = select_namespace(account_id, headers)

    elif( choice == '4' ) :

        delete_all(account_id, namespace_id, headers)

    elif( choice == '0' ) :

        exit()

    if( choice != '0' ) :

        run(account_id, namespace_id, headers)

def main():

    account_id = input("Enter your Cloudflare account ID: ")
    print('Account ID is set to: ' + account_id)

    account_email = input("Enter your Cloudflare account Email: ")
    print('Account Email is set to: ' + account_email)

    api_key = getpass.getpass("Enter your Global API Key: ")

    headers = {
        'X-Auth-Email': account_email,
        'X-Auth-Key': api_key,
    }

    namespace_id = select_namespace(account_id, headers)

    run(account_id, namespace_id, headers)

if __name__ == '__main__':
    main()
