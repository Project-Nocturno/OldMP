from flask import request, send_file
from json import loads, dumps
from os import path as ospath

def register_misc_routes(app, oldmp):
    @app.route('/favicon.ico')
    def favicon():
        return send_file('data/content/images/logo.ico', mimetype='image/ico')
    
    @app.route('/clearitemsforshop', methods=['GET'])
    def cleanitemforshop():
        athena = loads(open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'r', encoding='utf-8').read())[oldmp.session.get('username')].copy()
        shop = loads(open(f'data/content/catalogconfig.json', 'r', encoding='utf-8').read())
        StatChanged = False
        
        for value in shop:
            if isinstance(shop[value]['itemGrants'], list):
                for key in athena['items']:
                    if isinstance(shop[value]['itemGrants'][0], str):
                        if len(shop[value]['itemGrants'][0]) != 0:
                            if str(shop[value]['itemGrants'][0]).lower() == str(athena['items'][key]['templateId']).lower():
                                list(athena['items']).remove(key)
                                StatChanged = True
        if StatChanged:
            athena['rvn'] += 1
            athena['commandRevision'] += 1
            
            athena[oldmp.session.get('username')] = athena
            open(f'data/profiles/{request.args.get("profileId") or "athena"}.json', 'w', encoding='utf-8').write(dumps(athena, indent=4))