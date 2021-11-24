""" Swagger Connectivity and API definition """
from flask import url_for
from flask_restx import Api

from controller.meeting import NS

AUTHORIZATIONS = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


class CustomApi(Api):
    ''' Customization to set swagger url '''

    @property
    def specs_url(self):
        '''
        The Swagger specifications absolute url (ie. `swagger.json`)
        :rtype: str
        '''
        return url_for(self.endpoint('specs'), _external=False)


API = CustomApi(
    version='0.1.0',
    title='Meetings API',
    description='REST API for Meetings API',
    security='Bearer Auth',
    authorizations=AUTHORIZATIONS)

API.add_namespace(NS)
