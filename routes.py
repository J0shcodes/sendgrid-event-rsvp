from flask import render_template, redirect, request, url_for
from models import Event, RSVP
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ai_helper import generate_description

def create_routes(app, db, SENDGRID_API_KEY):
    @app.route("/")
    def index():
        events = Event.query.all()
        return render_template("index.html", events=events)

    @app.route("/create_event", methods=["GET", "POST"])
    def create_event():
        if request.method == "POST":
            name = request.form["name"]
            date = request.form["date"]
            description = request.form["description"]

            # If user doesn't provide description, generate one
            if not description:
                description = generate_description(name, date)

            new_event = Event(name=name, date=date, description=description)
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("create_event.html")

    @app.route("/event/<int:event_id>")
    def event_detail(event_id):
        event = Event.query.get_or_404(event_id)
        rsvps = RSVP.query.filter_by(event_id=event_id).all()
        return render_template("event_detail.html", event=event, rsvps=rsvps)

    @app.route("/send_invitations/<int:event_id>", methods=["POST"])
    def send_invitations(event_id):
        event = Event.query.get_or_404(event_id)
        emails = request.form["emails"].split(",")

        for email in emails:
            email = email.strip()
            message = Mail(
                from_email="mosesjoshua350@gmail.com",
                to_emails=email,
                subject=f"invitation to {event.name}",
                html_content=f"You are invited to {event.name} on {event.date}. <br>"
                f'<a href="{url_for("rsvp", event_id=event.id, email=email, status="yes", _external=True)}">Yes</a> '
                f'<a href="{url_for("rsvp", event_id=event.id, email=email, status="no", _external=True)}">No</a> '
                f'<a href="{url_for("rsvp", event_id=event.id, email=email, status="maybe", _external=True)}">Maybe</a>',
            )

            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                response = sg.send(message)
                print(response.status_code)
            except Exception as e:
                print(str(e))

        return redirect(url_for('event_detail', event_id=event_id))
    
    @app.route('/rsvp/<int:event_id>')
    def rsvp(event_id):
        email = request.args.get('email')
        status = request.args.get('status')

        existing_rsvp = RSVP.query.filter_by(event_id=event_id, email=email).first()
        if existing_rsvp:
            existing_rsvp.status = status
        else:
            new_rsvp = RSVP(event_id=event_id, email=email, status=status)
            db.session.add(new_rsvp)

        db.session.commit()
        return 'Thank you for your RSVP!'
