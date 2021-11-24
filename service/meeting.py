""" Meeting API """
#  pylint: disable=broad-except, wrong-import-order, consider-using-enumerate
import logging
from datetime import datetime

from flask_restx import inputs
from util.constant import DATE_FORMAT
from util.db_util import DBUtil


class Meeting:
    """ Class to handle meeting related operations """

    def __init__(self):
        self.class_name = type(self).__name__
        self.logger = logging.getLogger(self.class_name)
        self.collection = DBUtil().get_collection('meetings')

    def get_meetings(
            self, participant, meeting_title=None, show_rejected=None,
            start_date_time=None, end_date_time=None):
        """ Get Meetings """
        try:
            query = {'attendees': participant, 'accepted': True}
            if start_date_time:
                query['startDatetime'] = {'$gte': start_date_time}
            if end_date_time:
                query['endDatetime'] = {'$lte': end_date_time}
            if show_rejected:
                del query['accepted']
            if meeting_title:
                query['title'] = meeting_title
            meetings = list(self.collection.find(query, {'_id': 0}))
            if not meetings:
                return {'errorMsg': 'No meetings found'}, 404
            # Making dates Json serializable
            for meeting in meetings:
                meeting['startDatetime'] = str(meeting['startDatetime'])
                meeting['endDatetime'] = str(meeting['endDatetime'])
            return {'result': meetings}, 200
        except Exception as ex:
            self.logger.exception(
                'Exception occured while fetching meeting')
            return {'exception': str(ex)}, 500

    def create_meeting(self, payload):
        """ Create a meeting """
        try:
            if not payload:
                return {'errorMsg': 'Invalid Payload'}, 404
            title = payload.get('title')
            meet_exist = self.collection.find_one({'title': title})
            if meet_exist:
                return {
                    'errorMsg': f'meeting with title: {title} already exists'
                }, 409
            payload['startDatetime'] = inputs.datetime_from_iso8601(
                payload['startDatetime'])
            payload['endDatetime'] = inputs.datetime_from_iso8601(
                payload['endDatetime'])
            if payload['startDatetime'] == payload['endDatetime']:
                return {
                    'errorMsg': 'Invalid duration for meeting',
                    "tip": 'End datetime should be greater than start datetime'
                }, 403
            # By default a meeting is accepted unless specified
            payload.update(accepted=True)
            # self.collection.insert_one(payload)
            return {'message': 'Meeting has been created'}, 200
        except Exception as ex:
            self.logger.exception(
                'Exception occured while creating meeting')
            return {'exception': str(ex)}, 500

    def delete_meetings(self, meeting_title=None):
        """ Delete Meetings """
        try:
            query = {}
            if meeting_title:
                query['title'] = meeting_title
            meetings = list(self.collection.find(
                query, {'_id': 0, 'title': 1}))
            if not meetings:
                return {'errorMsg': 'No meetings found'}, 404
            self.collection.delete_many(query)
            return {'result': 'Meeting deleted successfully'}, 200
        except Exception as ex:
            self.logger.exception(
                'Exception occured while deleting meeting')
            return {'exception': str(ex)}, 500

    def update_meeting(self, title, payload):
        """ Update a meeting """
        try:
            if not payload:
                return {'errorMsg': 'Nothing to update'}, 200
            meet_exist = self.collection.find_one({'title': title})
            if not meet_exist:
                return {
                    'errorMsg': f'meeting with title: {title} does not exist'
                }, 404
            self.collection.update_one({'title': title}, {'$set': payload})
            return {'message': 'Meeting has been updated'}, 200
        except Exception as ex:
            self.logger.exception(
                'Exception occured while updating meeting')
            return {'exception': str(ex)}, 500

    def respond_to_meeting(self, title, accepted):
        """ Respond to a meeting """
        try:
            meet_exist = self.collection.find_one({'title': title})
            if not meet_exist:
                return {
                    'errorMsg': f'meeting with title: {title} does not exist'
                }, 404
            self.collection.update_one(
                {'title': title}, {'$set': {'accepted': accepted}})
            if accepted:
                return {'message': 'Meeting request has been accepted'}, 200
            return {'message': 'Meeting request has been rejected'}, 200
        except Exception as ex:
            self.logger.exception(
                'Exception occured while responding to meeting')
            return {'exception': str(ex)}, 500

    def get_meeting_hours(self, start, end, participant):
        """ Get meeting hours """
        try:
            filtered_meetings, status_code = self.get_meetings(
                participant, show_rejected=False)
            if status_code != 200:
                return filtered_meetings, status_code
            meetings = filtered_meetings['result']
            meetings = sorted(
                meetings,
                key=lambda k: (k['endDatetime'], k['startDatetime']))
            seconds = self.calculate_duration(
                end, start, meetings[0]['endDatetime'],
                meetings[0]['startDatetime'])
            i_indx = 0
            for j_indx in range(len(meetings)):
                if (meetings[j_indx]['startDatetime'] >=
                        meetings[i_indx]['endDatetime']):
                    seconds += self.calculate_duration(
                        end, start,
                        meetings[j_indx]['endDatetime'],
                        meetings[j_indx]['startDatetime'])
                    i_indx = j_indx
            return {
                'seconds': seconds,
                'minutes': round(seconds/60, 2),
                'hours': round(seconds/3600, 2)
            }, 200
        except Exception as ex:
            self.logger.exception(
                'Exception occured while fetching meeting duration')
            return {'exception': str(ex)}, 500

    @staticmethod
    def calculate_duration(end, start, end_datetime, start_datetime):
        """
        [Summary]:
            Calulates the duration in seconds

        [Arguments]:
            end, start (datetime object):
                queried start and end datetime

            end_datetime, start_datetime (string of datetime object):
                start and end date of meetings from database
        """
        end_time = datetime.strptime(end_datetime, DATE_FORMAT)
        start_time = datetime.strptime(start_datetime, DATE_FORMAT)
        if start > start_time:
            start_time = start
        if end < end_time:
            end_time = end
        return (end_time-start_time).seconds
