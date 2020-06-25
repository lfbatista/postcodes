import json

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
API_URL = 'http://api.postcodes.io/postcodes/'


@app.route('/')
def home():
    result = sort_helper(get_geolocation(), 'name')
    return jsonify(result)


@app.route('/stores')
def stores():
    # radius and postcode query parameters
    radius = request.args.get('radius', default='25000')
    postcode = request.args.get('postcode', default='BN16 3RT')

    result = get_stores(postcode, radius)
    return jsonify(result)


def stores_helper():
    return dict((store['name'], store['postcode']) for store in data)


def sort_helper(lst, d_key, reverse=False):
    return sorted(lst, key=lambda d: d[d_key], reverse=reverse)


def get_geolocation():
    """ :return a list of dictionaries containing the store's name, postcode, and geolocation """
    # bulk postcode request
    payload = json.dumps({'postcodes': list(stores_helper().values())})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(API_URL, data=payload, headers=headers)

    if response.status_code == 200:
        content = json.loads(response.content)
        stores_geoloc = [{
            'name': list(stores_helper().keys())[i].replace('_', ' '),
            'postcode': res['result']['postcode'],
            'latitude': res['result']['latitude'],
            'longitude': res['result']['longitude']}
                    for i, res in enumerate(content['result']) if res['result'] is not None]
    else:
        print(json.loads(response.content))

    return stores_geoloc


def get_stores(postcode='BN16 3RT', radius='200'):
    """ :return a list of stores in a given radius of a given postcode sorted from north to south """
    limit = '100'
    url = API_URL + postcode + '/nearest?radius=' + radius + '&limit=' + limit
    response = requests.get(url)

    if response.status_code == 200:
        content = json.loads(response.content)

        # content response sorted from north to south
        sorted_response = sort_helper(content['result'], 'northings')

        stores = [{
            'name': f'{res["admin_ward"]} {res["incode"]}',
            'postcode': res['postcode'],
        } for res in sorted_response]

        return stores
    else:
        print(json.loads(response.content))
        return None


with open('stores.json') as f:
    data = json.load(f)

if __name__ == '__main__':
    app.run()
