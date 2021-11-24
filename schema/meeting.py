""" Meetings model """
from flask_restx import fields, inputs


def create_meetings_fields():
    """ Create Fields """
    return {
        'title': fields.String(
            required=True,
            description="Meeting title",
            example="eg: DSU"
        ),
        'description': fields.String(
            required=False,
            description="Meeting description",
            example="Daily Status Call"
        ),
        'startDatetime': fields.String(
            required=True,
            type=inputs.datetime_from_iso8601,
            description="start time",
            example="yyyy-mm-ddThh:mm:ss"
        ),
        'endDatetime': fields.String(
            required=True,
            type=inputs.datetime_from_iso8601,
            description="end time",
            example="yyyy-mm-ddThh:mm:ss"
        ),
        'attendees': fields.String(
            example='example@org.com',
            type=inputs.email(check=True, domains=[
                'ridecell.com', "gmail.com"]),
            pattern=r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$',
            required=True,
            description="List of attendees"
        )
    }


def update_meetings_fields():
    """ Update Fields """
    return {
        'description': fields.String(
            required=False,
            description="Meeting description",
            example="Daily Status Call"
        ),
        'startDatetime': fields.String(
            required=True,
            type=inputs.datetime_from_iso8601,
            description="start time",
            example="YYYY-MM-DD"
        ),
        'endDatetime': fields.String(
            required=True,
            type=inputs.datetime_from_iso8601,
            description="end time",
            example="YYYY-MM-DD"
        ),
        'attendees': fields.String(
            example='example@org.com',
            type=inputs.email(check=True, domains=[
                'ridecell.com', "gmail.com"]),
            pattern=r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$',
            required=True,
            description="List of attendees"
        )
    }
