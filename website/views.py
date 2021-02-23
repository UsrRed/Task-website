from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Tasks, TRdv, Tskrepet
from . import db
import datetime as dt


views = Blueprint('views', __name__)

days_name = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
month_name = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre",
              "Octobre", "Novembre", "Décembre"]


@views.route('/', methods=['GET', 'POST'])
def home():
    # Checker if the task is passed
    for tsk in db.session.query(Tasks):
        if int((tsk.date - dt.datetime.now()).total_seconds()) < 0:
            db.session.query(Tasks).filter_by(id=tsk.id).delete()
    for Rdv in db.session.query(TRdv):
        if int((Rdv.date - dt.datetime.now()).total_seconds()) < 0:
            db.session.query(TRdv).filter_by(id=Rdv.id).delete()

    if request.method == 'POST':
        db.session.query(Tasks).update({"state": False})
        db.session.query(TRdv).update({"state": False})
        db.session.query(Tskrepet).update({"state": False})
        for a_task in request.form:
            elements = a_task.split("-")
            his_type = elements[0]
            his_id = elements[1]
            if his_type == "Task":
                db.session.query(Tasks).filter_by(id=his_id).update({"state": True})
            if his_type == "Repet":
                db.session.query(Tskrepet).filter_by(id=his_id).update({"state": True})
            if his_type == "Rdv":
                db.session.query(TRdv).filter_by(id=his_id).update({"state": True})

        db.session.commit()
        flash('Mise à jour réussi', category='success')

    return render_template("index.html", tasks=db.session.query(Tasks), repet=db.session.query(Tskrepet),
                           rdv=db.session.query(TRdv), now=dt.datetime.now(), dt=dt, days_name=days_name,
                           month_name=month_name)


@views.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        db.session.query(Tasks).update({"to_delete": False})
        db.session.query(Tskrepet).update({"to_delete": False})
        db.session.query(TRdv).update({"to_delete": False})
        for a_task in request.form:
            elements = a_task.split("-")
            his_type = elements[0]
            his_id = elements[1]
            if his_type == "Task":
                db.session.query(Tasks).filter_by(id=his_id).update({"to_delete": True})
            if his_type == "Repet":
                db.session.query(Tskrepet).filter_by(id=his_id).update({"to_delete": True})
            if his_type == "Rdv":
                db.session.query(TRdv).filter_by(id=his_id).update({"to_delete": True})

        db.session.query(Tasks).filter_by(to_delete=True).delete()
        db.session.query(TRdv).filter_by(to_delete=True).delete()
        db.session.query(Tskrepet).filter_by(to_delete=True).delete()
        db.session.commit()
        flash('destruction réussi', category='success')
        return redirect(url_for('views.home'))

    return render_template("Delete.html", tasks=db.session.query(Tasks), repet=db.session.query(Tskrepet),
                           rdv=db.session.query(TRdv), now=dt.datetime.now(), dt=dt, days_name=days_name,
                           month_name=month_name)


@views.route('/Task', methods=['GET', 'POST'])
def ftask():
    if request.method == 'POST':
        # if sending data get the context and date
        context = request.form.get("context")
        date = dt.datetime(year=int(request.form.get("year")), month=int(request.form.get("month")),
                           day=int(request.form.get("day")), hour=int(request.form.get("hour")),
                           minute=int(request.form.get("minute")))
        # test the date/context
        if not context:
            flash("Vous devez mettre un contexte/titre", category='error')
        elif (date - dt.datetime.now()).total_seconds() <= 0:
            flash("Vous devez mettre une date future", category='error')
        else:
            # if all ok create a new task
            new_task = Tasks(context=context, date=date)
            try:
                # insert it in the database
                db.session.add(new_task)
                db.session.commit()
                flash("Création de la tâche réussie", category="success")
                # Go back to home
                return redirect(url_for('views.home'))
            except:
                flash("Une erreur est survenue lors de l'enregistrement des informations", category="error")
                raise Exception

    return render_template("Task.html", tasks=db.session.query(Tasks), now=dt.datetime.now(), month_name=month_name)


@views.route('/RDV', methods=['GET', 'POST'])
def frdv():
    if request.method == 'POST':
        # if sending data get the context and date
        context = request.form.get("context")
        date = dt.datetime(year=int(request.form.get("year")), month=int(request.form.get("month")),
                           day=int(request.form.get("day")), hour=int(request.form.get("hour")),
                           minute=int(request.form.get("minute")))
        # test the date/context
        if not context:
            flash("Vous devez mettre un contexte/titre", category='error')
        elif (date - dt.datetime.now()).total_seconds() <= 0:
            flash("Vous devez mettre une date future", category='error')
        else:
            # if all ok create a new task
            new_rdv = TRdv(context=context, date=date)
            try:
                # insert it in the database
                db.session.add(new_rdv)
                db.session.commit()
                flash("Création du rendez-vous réussie", category="success")
                # Go back to home
                return redirect(url_for('views.home'))
            except:
                flash("Une erreur est survenue lors de l'enregistrement des informations", category="error")

    return render_template("Rdv.html", rdv=db.session.query(TRdv), now=dt.datetime.now(), month_name=month_name)


@views.route('/Repet', methods=['GET', 'POST'])
def frepet():

    if request.method == 'POST':
        # if sending data get the context and date
        context = request.form.get("context")
        day = request.form.get("day")
        # test the date/context
        if not context:
            flash("Vous devez mettre un contexte/titre", category='error')
        else:
            # if all ok create a new task
            new_rep = Tskrepet(context=context, day=day)
            try:
                # insert it in the database
                db.session.add(new_rep)
                db.session.commit()
                flash("Création de la tâche répétitive réussie", category="success")
                # Go back to home
                return redirect(url_for('views.home'))
            except:
                flash("Une erreur est survenue lors de l'enregistrement des informations", category="error")

    return render_template("Repet.html", repet=db.session.query(Tskrepet), now=dt.datetime.now(), days_name=days_name)
