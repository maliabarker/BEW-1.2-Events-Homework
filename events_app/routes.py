"""Import packages and modules."""
import os
from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest, EventType
from flask import current_app as app

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)

db.init_app(app)


##########################################
#           Routes                       #
##########################################

@main.route('/')
def index():
    """Show upcoming events to users!"""

    # TODO: Get all events and send to the template
    try:
        all_events = Event.query.all()
    except:
        flash('No Events, Create One!')
        return render_template('index.html', events=None)
    # print(all_events)
    # print(all_events[0].title)
    # print(all_events[0].guests)
    return render_template('index.html', events=all_events)


@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""
    if request.method == 'POST':
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')
        # event_type = request.form.get('event_type')
        # print(event_type)
        print(date)

        try:
            date_and_time = datetime.strptime(
                f'{date} {time}',
                '%Y-%m-%d %H:%M')
            print(date_and_time)
        except ValueError:
            return render_template('create.html', 
                error='Incorrect datetime format! Please try again.')

        # TODO: Create a new event with the given title, description, & 
        # datetime, then add and commit to the database
        new_event = Event(
            title=new_event_title, 
            description=new_event_description, 
            date_and_time=date_and_time,
            # event_type=EventType.event_type
            )

        db.session.add(new_event)
        db.session.commit()

        flash('Event created.')
        return redirect(url_for('main.index'))
    else:
        return render_template('create.html')

'''ROUTE TO SHOW SINGLE EVENT'''
@main.route('/event/<event_id>', defaults={'error': None})
@main.route('/event/<event_id>/<error>', methods=['GET'])
def event_detail(event_id, error):
    """Show a single event."""
    # TODO: Get the event with the given id and send to the template
    event = Event.query.filter_by(id=event_id).one()
    print(f'error: {error}')
    return render_template('event_detail.html', event=event, error=error)

'''ROUTE TO EDIT SINGLE EVENT'''
@main.route('/event/<event_id>/edit', methods=['GET', 'POST'])
def event_edit(event_id):
    if request.method == 'POST':
        print('POSTING')
        event = Event.query.filter_by(id=event_id).one()
        updated_title = request.form.get('title')
        updated_description = request.form.get('description')
        updated_date = request.form.get('date')
        updated_time = request.form.get('time')
        try:
            updated_date_and_time = datetime.strptime(
                f'{updated_date} {updated_time}',
                '%Y-%m-%d %H:%M')

        except ValueError:
            return render_template('create.html', 
                error='Incorrect datetime format! Please try again.')
        event.title = updated_title
        event.description = updated_description
        event.date_and_time = updated_date_and_time
        db.session.commit()
        flash(f'Successfully updated {event.title}')
        return redirect(url_for('main.event_detail', event_id=event_id))

    elif request.method == 'GET':
        event = Event.query.filter_by(id=event_id).one()
        print(event)
        return render_template('event_edit.html', event=event)

'''ROUTE TO ADD GUEST TO EVENT (UPDATES GUEST_EVENTS TABLE) POSTS TO SHOW SINGLE EVENT PAGE'''
@main.route('/event/<event_id>', defaults={'error': None}, methods=['POST'])
@main.route('/event/<event_id>/<error>', methods=['POST'])
def rsvp(event_id, error):
    """RSVP to an event."""
    # TODO: Get the event with the given id from the database
    event = Event.query.filter_by(id=event_id).one()
    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')

    if is_returning_guest:
        # TODO: Look up the guest by name. If the guest doesn't exist in the 
        # database, render the event_detail.html template, and pass in an error
        # message as `error`.

        # TODO: If the guest does exist, add the event to their 
        # events_attending, then commit to the database
        try:
            guest = Guest.query.filter_by(name=guest_name).one()
            print(guest)
        except:
            print('NO USER FOUND AHHHHH')
            error = 'ERROR: No user found, please enter your email and phone on the RSVP form'
            print(error)
            return redirect(url_for('main.event_detail', event_id=event_id, error=error))
    else:
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')
        guest = Guest(name=guest_name, email=guest_email, phone=guest_phone)

        # TODO: Create a new guest with the given name, email, and phone, and 
        # add the event to their events_attending, then commit to the database.
    guest.events_attending.append(event)
    print(guest)
    print(guest.events_attending)

    db.session.add(guest)
    db.session.commit()
    
    flash('You have successfully RSVP\'d! See you there!')
    return redirect(url_for('main.event_detail', event_id=event_id))


@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    # TODO: Get the guest with the given id and send to the template
    try:
        guest = Guest.query.filter_by(id=guest_id).one()
    except:
        print('Guest was not found')
    
    return render_template('guest_detail.html', guest=guest)
