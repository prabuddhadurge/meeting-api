""" Meeting API controller """
from flask import request
from flask_restx import Namespace, Resource, inputs, reqparse
from schema.meeting import create_meetings_fields, update_meetings_fields
from service.meeting import Meeting

NS = Namespace(
    'meetings',
    description='Operations related to meetings API')

MEETING_FIELDS = NS.model(
    "MeetingFieldsModel", create_meetings_fields())
UPDATE_FIELDS = NS.model(
    "UpdateFieldsModel", update_meetings_fields())

QUERY_PARAMETER = reqparse.RequestParser()
QUERY_PARAMETER.add_argument(
    'include_rejected', default=False, type=inputs.boolean,
    help='show rejected meetings?', required=False)
QUERY_PARAMETER.add_argument(
    'user', required=True,
    type=inputs.email(check=True, domains=['gmail.com', 'ridecell.com']),
    help='fetches meetings which an user is an participant of')
QUERY_PARAMETER.add_argument(
    'startDatetime', type=inputs.datetime_from_iso8601,
    help='meeting start datetime (yyyy-mm-ddThh:mm:ss)', required=False)
QUERY_PARAMETER.add_argument(
    'endDatetime', type=inputs.datetime_from_iso8601,
    help='meeting end datetime (yyyy-mm-ddThh:mm:ss)', required=False)

QUERY_PARAMETER_TWO = reqparse.RequestParser()
QUERY_PARAMETER_TWO.add_argument(
    'accept', type=inputs.boolean,
    help='accept meeting request?', required=True)


@NS.route('')
class Meetings(Resource):
    """ Controller for Meetings API """

    @staticmethod
    @NS.doc(parser=QUERY_PARAMETER)
    def get():
        """ returns all meetings """
        participant = QUERY_PARAMETER.parse_args()['user']
        show_rejected = QUERY_PARAMETER.parse_args()['include_rejected']
        startdatetime = QUERY_PARAMETER.parse_args()['startDatetime']
        enddatetime = QUERY_PARAMETER.parse_args()['endDatetime']
        return Meeting().get_meetings(
            participant, show_rejected=show_rejected,
            start_date_time=startdatetime, end_date_time=enddatetime)

    @staticmethod
    @NS.expect(MEETING_FIELDS, validate=True)
    def post():
        """ creates a new meeting """
        payload = request.get_json()
        return Meeting().create_meeting(payload)

    @staticmethod
    def delete():
        """ deletes all meetings """
        return Meeting().delete_meetings()


@NS.route('/<string:meeting_title>')
class MeetingTitle(Resource):
    """ Controller to deal with endpoints with meeting title """

    @staticmethod
    @NS.doc(parser=QUERY_PARAMETER)
    def get(meeting_title):
        """ returns a meeting """
        participant = QUERY_PARAMETER.parse_args()['user']
        show_rejected = QUERY_PARAMETER.parse_args()['include_rejected']
        startdatetime = QUERY_PARAMETER.parse_args()['startDatetime']
        enddatetime = QUERY_PARAMETER.parse_args()['endDatetime']
        return Meeting().get_meetings(
            participant, meeting_title=meeting_title,
            show_rejected=show_rejected, start_date_time=startdatetime,
            end_date_time=enddatetime)

    @staticmethod
    @NS.expect(UPDATE_FIELDS, validate=True)
    def put(meeting_title):
        """ updates a meeting """
        payload = request.get_json()
        return Meeting().update_meeting(meeting_title, payload)

    @staticmethod
    @NS.doc(parser=QUERY_PARAMETER)
    def delete(meeting_title):
        """ deletes a meeting """
        return Meeting().delete_meetings(meeting_title=meeting_title)


@NS.route('/<string:meeting_title>/respond')
class Respond(Resource):
    """ Class to respond to meetings (accept/reject) """

    @staticmethod
    @NS.doc(parser=QUERY_PARAMETER_TWO)
    def patch(meeting_title):
        """ respond a meeting """
        accept = QUERY_PARAMETER_TWO.parse_args()['accept']
        return Meeting().respond_to_meeting(meeting_title, accept)


@NS.route('/meeting_hours')
class Hours(Resource):
    """ Class to get meeting hours """

    @staticmethod
    @NS.doc(parser=QUERY_PARAMETER)
    def get():
        """ get meeting hours """
        start = QUERY_PARAMETER.parse_args()['startDatetime']
        end = QUERY_PARAMETER.parse_args()['endDatetime']
        participant = QUERY_PARAMETER.parse_args()['user']
        return Meeting().get_meeting_hours(start, end, participant)
