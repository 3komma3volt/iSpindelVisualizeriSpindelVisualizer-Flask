from ispindelVisualizer import app, db
from ispindelVisualizer.models import Spindles, Spindle_data
from ispindelVisualizer.forms import LoginForm, TimespanForm, NameChangeForm, DataDeleteForm

from flask import render_template, redirect, request, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import desc
from datetime import datetime, timedelta

@app.route('/update', methods=['GET', 'POST'])
def update_spindle():
    if request.content_type != 'application/json':
        return "Error: No data provided"       
    json_post_data = request.get_json()
    key = request.args.get("key")

    if key is None:
        return "Error: No key provided"

    if json_post_data is None:
        return "Error: No data provided"
    
    required_json_fields = ["name", "ID", "angle", "temperature", "temp_units", "battery", "gravity", "interval", "RSSI"]
    for required_key in required_json_fields:
        if required_key not in json_post_data:
            return f"Error: Missing data {required_key}"
    
    stored_spindle = Spindles.query.filter_by(spindle_id=json_post_data['ID']).first()

    return_message = ""

    bc = Bcrypt()

    if stored_spindle is None:
        new_spindle = Spindles(json_post_data['ID'], key, json_post_data['name'])
        db.session.add(new_spindle)
        db.session.commit()
        return_message += f"Spindle {json_post_data['ID']} with name {json_post_data['name']} created\n"
        stored_spindle = Spindles.query.filter_by(spindle_id=json_post_data['ID']).first()
    else:
        if not bc.check_password_hash(stored_spindle.spindle_key, key):
            return "Error: Wrong key provided"
    

    creation_time = datetime.now()

    new_spindle_data = Spindle_data(json_post_data['name'], json_post_data['ID'], json_post_data['angle'], json_post_data['temperature'],
                                    json_post_data['temp_units'], json_post_data['battery'], json_post_data['gravity'], json_post_data['interval'],
                                    json_post_data['RSSI'], creation_time)
    
    db.session.add(new_spindle_data)
    db.session.commit()
    return_message += "Data inserted sucessfully\n"

    return  return_message

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():

    ts_form = TimespanForm(timespan_select=14)
    nc_form = NameChangeForm()
    ds_form = DataDeleteForm()

    if ds_form.validate_on_submit():
        if ds_form.delete_data.data:
            Spindle_data.query.filter_by(spindle_id=current_user.spindle_id).delete()
            db.session.commit()
            flash('Data deleted')

    if nc_form.validate_on_submit():
        new_name = nc_form.new_spindle_name.data  
        spindle = Spindles.query.filter_by(spindle_id=current_user.spindle_id).first()
        spindle.spindle_alias = new_name
        db.session.commit()

    nc_form.new_spindle_name.data = current_user.spindle_alias

    last_entry = Spindle_data.query.filter_by(spindle_id = current_user.spindle_id).order_by(desc(Spindle_data.created_at)).first()

    timespan = 14
    if ts_form.validate_on_submit():
        timespan = int(ts_form.timespan_select.data)
    if last_entry is None:
        return render_template("dashboard.html", timespan_form=ts_form, 
                                            name_change_form=nc_form, 
                                            data_delete_form=ds_form,
                                            spindle_alias = current_user.spindle_alias, 
                                            spindle_id = current_user.spindle_id,)
    
    last_date = last_entry.created_at - timedelta(days=timespan)

    battery = []
    gravity = []
    angle =  []
    measurement_date = []
    temperature = []

    results = Spindle_data.query.filter_by(spindle_id=current_user.spindle_id).filter(Spindle_data.created_at >= last_date).all()

    for res in results:
        battery.append(res.battery)
        gravity.append(res.gravity)
        angle.append(res.angle)
        if res.created_at is not None:
            date_short = res.created_at.strftime("%d.%m. %H:%M")
        measurement_date.append(date_short)
        temperature.append(res.temperature)
    
    return render_template("dashboard.html", timespan_form=ts_form, 
                                            name_change_form=nc_form, 
                                            data_delete_form=ds_form,
                                            spindle_alias = current_user.spindle_alias, 
                                            spindle_id = current_user.spindle_id,
                                            battery=battery, 
                                            gravity=gravity, 
                                            angle=angle, 
                                            measurement_date=measurement_date, 
                                            temperature=temperature)

@app.route("/login", methods=['GET', 'POST'])
def login():
    bc = Bcrypt()
    login_form = LoginForm()

    if login_form.validate_on_submit():
        spindle = Spindles.query.filter_by(spindle_id=login_form.login_spindle_id.data).first()
        if spindle is not None and bc.check_password_hash(spindle.spindle_key, login_form.login_spindle_key.data):
                login_user(spindle)
                next = request.args.get('next')
                if next is None or not next[0]=='/':
                    next = url_for('index')
                return redirect(next) 
        else:
            flash('Error logging in.')    

    return render_template('login.html', form = login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
