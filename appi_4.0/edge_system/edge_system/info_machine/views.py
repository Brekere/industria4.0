from operator import mod
from flask import Blueprint, render_template, request, flash, jsonify, abort
import json
from flask.helpers import url_for
import numpy as np
from datetime import date, datetime, timedelta
from flask_login import login_required
from sqlalchemy.sql.elements import and_
from werkzeug.utils import redirect
import requests
from sqlalchemy import or_, and_

from edge_system import db, remote_server, max_num_records_to_upload
from edge_system.info_machine.model.machine import Machine, RegisterForm
from edge_system.info_machine.model.part_info import Part, UploadPartsHist
from edge_system.info_machine.model.rework_part_info import ReworkPart, UploadReworkPartsHist

def get_remote_informatio():
    """
    Getting the remote information to register the new machine 
    """
    data = {}

    ### getting lines ... 
    url_lines = remote_server + 'Lineas/linea/cargar/'
    try:
        response = requests.post(url_lines)
    except:
        flash('Error: not server connection','danger')
        return data 
    #print("\t JSON data: \n", response.json())
    data_lines = response.json()
    if data_lines: # por ahora no hay una opción cuando regrese vació #'' in response.json():
        data['lines'] = []
        for line in data_lines:
            info_line = ('{}'.format(line['id']), line['name'])
            data['lines'].append(info_line)
            #print(line)
        print(data['lines'])
    ### getting suppliers .. Falta este endpoint .. 
    data['suppliers'] = []
    data['suppliers'].append(('1', 'ASBajio'))
    ### getting 
    return data  

def get_id_remote_machine(nickname_machine): # no esta como unico en la base de datos pero lo manejaremos por ahora así, hasta que regrese el id el endpoint de guardado
    url_machine = remote_server + 'Maquinas/maquina/cargar'
    id = -1
    try:
        response = requests.post(url_machine)
    except:
        flash('Error: Ca not get remote machine id!!! ','danger')
        return id
    data_machines = response.json()
    if data_machines:
        #print('looking for ..... ', nickname_machine)
        for machine_ in data_machines:
            #print(machine_)
            if nickname_machine == machine_['nickname']:
                return machine_['id']
    return id 

def save_remote_info_cachine(machine_info):
    url_machine_save = remote_server + 'Maquinas/maquina/guardar'
    payload = {
        'nickname': machine_info['nickname'],
        'description': machine_info['description'],
        'brand': machine_info['brand'],
        'model': machine_info['model'],
        'voltage': machine_info['voltage'],
        'amperage': machine_info['amperage'],
        'serie': machine_info['serie'],
        'id_line': machine_info['id_line'],
        'manufacturing_date': machine_info['manufacturing_date'],
        'instalation_date': machine_info['instalation_date'],
        'id_supplier': machine_info['id_supplier'],
        'run_date': machine_info['run_date'],
    }
    try:
        response = requests.post(url_machine_save, data=payload)
        flash('Saved in remote server')
    except:
        flash('Error: not server connection','danger')
        return -1 
    id = get_id_remote_machine(machine_info['nickname']) 
    #print('::: ID ', id)
    return id   

def get_machine_info_json():
    try:
        with open("edge_system/static/tmp/machine.json", "r") as read_file:
            data = json.load(read_file)
    except:
        print("ERROR")
        return None
    return data

machine = Blueprint('machine', __name__)

@machine.before_request  # con esto, esta función se ejecuta antes de cada endpoint que tengamos definido en este documento
@login_required
def constructor():
   pass

@machine.route('/machine/register_json')
def fill_machine_register_json():
    data_json = get_machine_info_json()
    form = RegisterForm(meta={'csrf': False})
    form.id.data = 13
    form.path_image.data = 'img/tmp_workstation_01.jpeg'
    form.nickname.data = data_json['nickname']
    form.description.data = data_json['description']
    form.brand.data = data_json['brand']
    form.model.data = data_json['model']
    form.voltage.data = int(data_json['voltage'])
    form.amperage.data = float(data_json['amperage'])
    form.serie.data = data_json['serie']
    form.id_line.data = int(data_json['id_line'])
    form.manufacturing_date.data = datetime.strptime(data_json['manufacturing_date'], '%Y-%m-%dT%H:%M:%S')
    form.instalation_date.data = datetime.strptime(data_json['instalation_date'], '%Y-%m-%dT%H:%M:%S')
    form.id_supplier.data = int(data_json['id_supplier'])
    form.run_date.data = datetime.strptime(data_json['run_date'], '%Y-%m-%dT%H:%M:%S')
    
    return render_template('machine/register.html', form = form)
    #return redirect(url_for('machine.machine_register', form = form))


@machine.route('/machine/register', methods=['GET', 'POST'])
def machine_register():
    print("HOLAAAA")
    if Machine.query.first():
        flash("Machine information already registered!!")
        return redirect(url_for('machine.info'))
    data = get_remote_informatio()
    form = RegisterForm(meta={'csrf': False})
    form.id_supplier.choices = [('0', 'unknown')]
    form.id_line.choices = [('0', 'unknown')]
    if data:
        form.id_supplier.choices = data['suppliers']
        form.id_line.choices = data['lines']
    if form.validate_on_submit():
        #if Machine.query.get(form.id.data):
        #    flash('Machine already registered!')
        #    return redirect(url_for('machine.machine_register'))
        machine_info = {
            'nickname': form.nickname.data,
            'description': form.description.data,
            'brand': form.brand.data,
            'model': form.model.data,
            'voltage': form.voltage.data,
            'amperage': form.amperage.data,
            'serie': form.serie.data,
            'id_line': int(form.id_line.data),
            'manufacturing_date': form.manufacturing_date.data,
            'instalation_date': form.instalation_date.data,
            'id_supplier': int(form.id_supplier.data),
            'run_date': form.run_date.data,
        }
        path_image = 'img/tmp_workstation_01.jpeg' #form.path_image.data
        print(machine_info)
        id_remote_machine = save_remote_info_cachine(machine_info)
        if id_remote_machine  == -1:
            return redirect(url_for('home.home_page')) 
        machine_ =  Machine(id=id_remote_machine,
        nickname=machine_info['nickname'],
        description=machine_info['description'],
        brand=machine_info['brand'],
        model=machine_info['model'],
        voltage=machine_info['voltage'],
        amperage=machine_info['amperage'],
        serie=machine_info['serie'],
        id_line=machine_info['id_line'],
        manufacturing_date=machine_info['manufacturing_date'],
        instalation_date=machine_info['instalation_date'],
        id_supplier=machine_info['id_supplier'],
        run_date=machine_info['run_date'],
        path_image= path_image)
        print(machine_)
        db.session.add(machine_)
        db.session.commit()
        flash("Machine information saved locally!!")
        return redirect(url_for('home.home_page'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('machine/register.html', form = form)

@machine.route('/machine/info')
def info():
    machine_ = Machine.query.first()
    if not machine_:
        flash("Machine information has not been registered!!", 'danger')
        return redirect(url_for('machine.machine_register'))
    print(machine_)
    return render_template("machine/machine_info.html", machine = machine_)

@machine.route('/upload')
def upload_historical():
    return render_template("machine/upload_records.html")


def from_model_to_data_parts(parts):
    data_records = []
    idx_min_max = []
    if not parts:
        return data_records
    idxs = []
    for part in parts:
        idxs.append(part.id)
        data_records.append({
            "timestamp":part.timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
            "status": "True" if part.status else "False",
            "working_time":"{}".format(part.working_time)
        })
    idx_min_max = [min(idxs), max(idxs)]
    print('----------------- ',idx_min_max)
    return data_records, idx_min_max

def upload_parts_record(data_to_upload):
    url_upload_parts = remote_server + 'Maquinas/maquina/lmi_parts'
    print('url ::::: ', url_upload_parts)
    #print(data_to_upload)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #headers = {
    #    "Cache-Control": "no-cache",
	#    "Postman-Token": "2fe1650d-a961-2c45-27b8-3f8b7d4a217c",
	#    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
    #}
    #response = requests.post(url_upload_parts, headers=headers, data=data_json)
    #response = requests.post(url_upload_parts, data=data_json)
    payload = {'datos': json.dumps(data_to_upload)}
    response = requests.post(url_upload_parts, data=payload, headers=headers)
    #print("\t Response: ", response)
    print (response.text)
    #print("\t Response headers: ", response.headers)
    if( "aviso" in response.text):
        if("Datos almacenados con" in response.text):
            print("------------------------ Datos almacenados!!!")
            return True
    return False

def get_min_max_idx(idx_min_max, idx_min_max_subset):
    print('::::::::::: min_max = {} \t ::::::::: subset_min_max = {}'.format(idx_min_max, idx_min_max_subset))
    if not idx_min_max:
        idx_min_max = [idx_min_max_subset[0], idx_min_max_subset[1]]
    else:
        idx_min_max =[
            min(idx_min_max[0], idx_min_max_subset[0]),
            max(idx_min_max[1], idx_min_max_subset[1])
        ]
    return  idx_min_max

def save_in_db_upload_record_parts(idx_min_max, offset_):
    upload_parts_hist = UploadPartsHist(
        upload_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        start_idx=idx_min_max[0],
        end_idx=idx_min_max[1],
        tot_records= offset_
    )
    db.session.add(upload_parts_hist)
    db.session.commit()


def parts_historical(id_machine, first_id, last_id):
    error_info = ''
    tot_saved = 0
    idx_min_max = []
    data_to_upload = {
        "id_machine": "{}".format(id_machine),
        "records": []
    }
    steps = int( (last_id - first_id + 1)/max_num_records_to_upload )
    residue = (last_id - first_id + 1) % max_num_records_to_upload 
    id_start, id_end = first_id, first_id + max_num_records_to_upload - 1
    for i in range(steps):
        print('id[start, end] = [{}, {}]'.format(id_start, id_end))
        parts = Part.query.filter( and_( Part.id >= id_start , Part.id <= id_end ))
        tot_i = parts.count()
        print('Total saved in {}  ---- '.format(i), tot_i)
        if tot_i > 0:
            data_to_upload["records"], idx_min_max_subset = from_model_to_data_parts(parts)
            if not upload_parts_record(data_to_upload):
                error_info = error_info + 'No uploaded (range = [{},{}], total = {}) :'.format(id_start, id_end, tot_i)
            else:
                idx_min_max = get_min_max_idx(idx_min_max, idx_min_max_subset)
                tot_saved += tot_i # verificar que si son 10 registros y no menos ( que se puede dar el caso!!)
                # save data ... 
                save_in_db_upload_record_parts(idx_min_max_subset, tot_i)
        id_start += max_num_records_to_upload
        id_end += max_num_records_to_upload
    print('Residue ---- ', residue)
    if residue:
        id_end = id_start + residue + steps*max_num_records_to_upload - 1
        print('id[start, end] = [{}, {}]'.format(id_start, id_end))
        parts = Part.query.filter( and_( Part.id >= id_start , Part.id <= id_end ))
        tot_i = parts.count()
        print('Total saved in last one  ---- '.format(i), tot_i)
        if tot_i > 0:
            data_to_upload["records"], idx_min_max_subset = from_model_to_data_parts(parts)
            if not upload_parts_record(data_to_upload):
                error_info = error_info + 'No uploaded (range = [{},{}], total = {}) :'.format(id_start, id_end, tot_i)
            else:
                idx_min_max = get_min_max_idx(idx_min_max, idx_min_max_subset)
                tot_saved += tot_i # verificar que si son 10 registros y no menos ( que se puede dar el caso!!)
                # save data ... 
                save_in_db_upload_record_parts(idx_min_max_subset, tot_i) 
    if error_info:
        flash(error_info, 'danger')
    else:
        flash('All Parts uploaded!!!')
    print('idx min max = ', idx_min_max)
    return tot_saved, idx_min_max

@machine.route('/upload/parts')
def upload_parts():
    machine_ = Machine.query.first()
    if not machine_:
        flash('No machine registered!') 
        return redirect(url_for('home.home_page'))
    print('id machine: ', machine_.id)
    last_upload = UploadPartsHist.query.order_by(UploadPartsHist.id.desc()).first()
    tot_saved = 0
    first_id = 0
    last_id = 0
    idx_min_max = []
    if last_upload:
        print(last_upload)
        idx_min_max = [0, 0]
        last_part = Part.query.order_by(Part.id.desc()).first()
        if last_part.id <= last_upload.end_idx:
            flash('[Parts] Everything is up to date!')
            return redirect(url_for('machine.upload_historical'))
        ## si no esta actualizado .. guardar lo nuevo ... 
        flash('[Parts] Saving the new data!!')
        first_id = last_upload.end_idx + 1
        last_id = last_part.id
    else:
        last_part = Part.query.order_by(Part.id.desc()).first()
        first_id = 1
        last_id = last_part.id
    print('first_id', first_id, '    last_id', last_id)
    print("version 2 ----- ")
    tot_saved, idx_min_max = parts_historical(machine_.id, first_id, last_id) 
    result = {
        'title': 'Parts',
        'total_records': tot_saved,
        'date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), #%d/%m/%Y
        'start': idx_min_max[0],
        'end': idx_min_max[1]
    }
    return render_template("machine/uploaded_records.html", result = result)


def from_model_to_data_rework_parts(rework_parts):
    data_records = []
    idx_min_max = []
    if not rework_parts:
        return data_records
    idxs = []
    for rework_part in rework_parts:
        idxs.append(rework_part.id)
        data_records.append({
            "timestamp":rework_part.timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
            "status": "True" if rework_part.status else "False",
            "working_time":"{}".format(rework_part.working_time)
        })
    idx_min_max = [min(idxs), max(idxs)]
    print('----------------- ',idx_min_max)
    return data_records, idx_min_max

def upload_rework_parts_record(data_to_upload):
    url_upload_rework_parts = remote_server + 'Maquinas/maquina/lmi_rework_parts'
    print('url ::::: ', url_upload_rework_parts)
    #print(data_to_upload)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'datos': json.dumps(data_to_upload)}
    response = requests.post(url_upload_rework_parts, data=payload, headers=headers)
    # por ahora se desactivará la llave foranea de la BD en la tabla lmi_rework_parts ya que no realizo la logica para
    #   revisar que se mande el indice correcto y no tengo indices que se junten con el id_machine para poder diferenciar
    #   el registro con id 1 de la maquina 13 de otras .... posiblemente implementarlo después ... 
    #print("\t Response: ", response)
    print (response.text)
    if( "aviso" in response.text):
        if("Datos almacenados con" in response.text):
            print("------------------------ Datos almacenados [rework]!!!")
            return True
    return False

def save_in_db_upload_record_rework_parts(idx_min_max, offset_):
    upload_rework_parts_hist = UploadReworkPartsHist(
        upload_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        start_idx=idx_min_max[0],
        end_idx=idx_min_max[1],
        tot_records= offset_
    )
    db.session.add(upload_rework_parts_hist)
    db.session.commit()


def rework_parts_historical(id_machine, first_id, last_id):
    error_info = ''
    tot_saved = 0
    idx_min_max = []
    data_to_upload = {
        "id_machine":"{}".format(id_machine),
        "records": []
    }
    steps = int( (last_id - first_id + 1)/max_num_records_to_upload )
    residue = (last_id - first_id + 1) % max_num_records_to_upload 
    id_start, id_end = first_id, first_id + max_num_records_to_upload - 1
    for i in range(steps):
        print('id[start, end] = [{}, {}]'.format(id_start, id_end))
        rework_parts = ReworkPart.query.filter( and_( ReworkPart.id >= id_start , ReworkPart.id <= id_end ))
        tot_i = rework_parts.count()
        print('Total saved in {} ---- '.format(i), tot_i)
        if tot_i > 0:
            data_to_upload["records"], idx_min_max_subset = from_model_to_data_rework_parts(rework_parts)
            if not upload_rework_parts_record(data_to_upload):
                error_info = error_info + 'No uploaded (range = [{},{}], total = {}) :'.format(id_start, id_end, tot_i)
            else:
                idx_min_max = get_min_max_idx(idx_min_max, idx_min_max_subset)
                tot_saved += tot_i # verificar que si son 10 registros y no menos ( que se puede dar el caso!!)
                # save data ... 
                save_in_db_upload_record_rework_parts(idx_min_max_subset, tot_i)
        id_start += max_num_records_to_upload
        id_end += max_num_records_to_upload
    print('Residue ---- ', residue)
    if residue:
        id_end = id_start + residue + steps*max_num_records_to_upload - 1
        print('id[start, end] = [{}, {}]'.format(id_start, id_end))
        rework_parts = ReworkPart.query.filter( and_( ReworkPart.id >= id_start , ReworkPart.id <= id_end ))
        tot_i = rework_parts.count()
        print('Total saved in last one ---- ', tot_i)
        if tot_i > 0:
            data_to_upload["records"], idx_min_max_subset = from_model_to_data_rework_parts(rework_parts)
            if not upload_rework_parts_record(data_to_upload):
                error_info = error_info + 'No uploaded (range = [{},{}], total = {}) :'.format(id_start, id_end, tot_i)
            else:
                idx_min_max = get_min_max_idx(idx_min_max, idx_min_max_subset)
                tot_saved += tot_i # verificar que si son 10 registros y no menos ( que se puede dar el caso!!)
                # save data ... 
                save_in_db_upload_record_rework_parts(idx_min_max_subset, tot_i)
    if error_info:
        flash(error_info, 'danger')
    else:
        flash('All Parts uploaded!!!')
    print('idx min max = ', idx_min_max)
    return tot_saved, idx_min_max

@machine.route('/upload/rework_parts')
def upload_rework_parts():
    machine_ = Machine.query.first()
    if not machine_:
        flash('No machine registered!') 
        return redirect(url_for('home.home_page'))
    print('id machine: ', machine_.id)
    last_upload = UploadReworkPartsHist.query.order_by(UploadReworkPartsHist.id.desc()).first()
    tot_saved = 0
    first_id = 0
    last_id = 0
    idx_min_max = []
    if last_upload:
        print(last_upload)
        idx_min_max = [0, 0]
        last_rework_part = ReworkPart.query.order_by(ReworkPart.id.desc()).first()
        if last_rework_part.id <= last_upload.end_idx:
            flash('[Rework-Parts] Everything is up to date!')
            return redirect(url_for('machine.upload_historical'))
        ## si no esta actualizado .. guardar lo nuevo ... 
        flash('[Rework-Parts] Saving the new data!!')
        first_id = last_upload.end_idx
        last_id = last_rework_part.id
    else:
        last_part = ReworkPart.query.order_by(ReworkPart.id.desc()).first()
        first_id = 1
        last_id = last_part.id
    print('first_id', first_id, '    last_id', last_id)
    tot_saved, idx_min_max = rework_parts_historical(machine_.id, first_id, last_id)
    result = {
        'title': 'Rework Parts',
        'total_records': tot_saved,
        'date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), #%d/%m/%Y
        'start': idx_min_max[0],
        'end': idx_min_max[1]
    }
    flash('Rework Parts Uploaded!')
    return render_template("machine/uploaded_records.html", result = result)

@machine.route('/machine_info')
def info2():
    try:
        with open("edge_system/static/tmp/machine.json", "r") as read_file:
            data = json.load(read_file)
        #print(data)
        # Select the main information only:
        data_filtered = data
        nickname = data['nickname']
        print('data type: ',type(data))
        del data_filtered['nickname']
    except:
        print("ERROR")
    return render_template("machine/machine_info2.html", nickname = nickname, data = data_filtered)


@machine.route('/test_get_data')
def test_get_data():
    data = {'id': [], 'working_time': []}
    metrics = {'avg': 0.0, 'min': 0.0, 'max': 0.0, 'std': 0.0}
    return render_template("test/production_test.html", mode = "Week", info = "OK-NOK", \
        data = data, metrics = metrics) 

@machine.route('/get_data/<static_period>/<type_info>', methods=['GET'])
def get_data(static_period=None, type_info = None):
    print('Period::: ', static_period, '    type info: ', type_info)
    if static_period == None:
        metrics = {'empty': 'No data for the period "{}" !'.format(static_period)}
        return jsonify(metrics)
    # get data ... 
    if type_info == "Working-Time":
        metrics = get_data_working_time_from_static_period(static_period)
    elif type_info == "OK-NOK":
        metrics = get_data_ok_nok_from_static_period(static_period)
    elif type_info == "Rework":
        metrics = get_data_rework_ok_nok_from_static_period(static_period)
    else:
        metrics = get_data_reworking_time_from_static_period(static_period) 
    return jsonify(metrics)

#### Showing the production 

@machine.route('/production_information/<static_period>/<type_info>', methods=['GET'])
def production_information(static_period=None, type_info = None):
    if static_period is None:
        mode = "Week"
    else:
        mode = static_period
    if type_info is None:
        info = "OK-NOK"
    else:
        info = type_info
    # Display a list of the different visualizations of the data over the current week
    return render_template("production/production_sidebar.html", mode = mode,  info = info) 

# Week 
@machine.route('/week_production')
def week_production():
    # Display a list of the different visualizations of the data over the current week
    return render_template("production/production_menu.html", mode = "Week") 

@machine.route('/week_production/ok')
def week_production_ok_nok():
    # Display the information about the ok and nok items/pieces
    #parts_info = Part.query.all()
    print("Hola www ")
    return render_template("production/production.html", mode = "Week", info = "OK-NOK") 

@machine.route('/week_production/time')
def week_production_time():
    # Display the information about the statistics of the time work (the ok pieces): average, max, min,
    return render_template("production/production.html", mode = "Week", info = "Working-Time") 

@machine.route('/week_production/rework')
def week_production_rework():
    return render_template("production/production.html", mode = "Week", info = "Rework")

@machine.route('/week_production/reworking-time')
def week_production_reworking_time():
    return render_template("production/production.html", mode = "Week", info = "Reworking-Time")

# day
@machine.route('/day_production')
def day_production():
    # Display a list of the different visualizations of the data over the current day
    return render_template("production/production_menu.html", mode = "Day") 

@machine.route('/day_production/ok')
def day_production_ok_nok():
    # Display the information about the ok and nok items/pieces
    return render_template("production/production.html", mode = "Day", info = "OK-NOK")  

@machine.route('/day_production/time')
def day_production_time():
    # Display the information about the statistics of the time work (the ok pieces): average, max, min,
    return render_template("production/production.html", mode = "Day", info = "Working-Time")  

@machine.route('/day_production/rework')
def day_production_rework():
    return render_template("production/production.html", mode = "Day", info = "Rework")

@machine.route('/day_production/reworking-time')
def day_production_reworking_time():
    return render_template("production/production.html", mode = "Day", info = "Reworking-Time")

# month

@machine.route('/month_production')
def month_production():
    # Display a list of the different visualizations of the data over the current month
    return render_template("production/production_menu.html", mode = "Month") 

@machine.route('/month_production/ok')
def month_production_ok_nok():
    # Display the information about the ok and nok items/pieces
    return render_template("production/production.html", mode = "Month", info = "OK-NOK")  

@machine.route('/month_production/time')
def month_production_time():
    # Display the information about the statistics of the time work (the ok pieces): average, max, min,
    return render_template("production/production.html", mode = "Month", info = "Working-Time")  

@machine.route('/month_production/rework')
def month_production_rework():
    return render_template("production/production.html", mode = "Month", info = "Rework")

@machine.route('/month_production/reworking-time')
def month_production_reworking_time():
    return render_template("production/production.html", mode = "Month", info = "Reworking-Time")


# window time

@machine.route('/time_window_production')
def time_windowproduction():
    # Display a list of the different visualizations of the data over a time_window
    return render_template("production/production_menu.html", mode = "Time window") 



##### Functions ... 

def get_parts_ok_nok_timewindow(start_datetime, end_datetime):
    parts_info = Part.query.filter(Part.timestamp <= end_datetime)\
        .filter(Part.timestamp >= start_datetime).all() 
    return parts_info

def get_parts_working_time_timewindow(start_datetime, end_datetime):
    parts_info = Part.query.filter(Part.timestamp <= end_datetime)\
        .filter(Part.timestamp >= start_datetime).filter(Part.status == False).all() 
    return parts_info

def get_parts_rework_ok_nok(start_datetime, end_datetime):
    rework_parts_info = ReworkPart.query.filter(ReworkPart.timestamp <= end_datetime)\
        .filter(ReworkPart.timestamp >= start_datetime).all() 
    return rework_parts_info

def get_parts_reworking_time_timewindow(start_datetime, end_datetime):
    rework_parts_info = ReworkPart.query.filter(ReworkPart.timestamp <= end_datetime)\
        .filter(ReworkPart.timestamp >= start_datetime).filter(ReworkPart.status == False).all() 
    return rework_parts_info

def get_rework_ok_nok_metrics(rework_parts_info):
    """
    Get the OK/NOK rework parts metrics 
    """
    data = {}
    metrics = {'tot_ok': 0, 'tot_nok': 0}
    for part in rework_parts_info:
        if part:
            data['id'] = part.id
            data['status'] = part.status
            if data['status'] == False:
                metrics['tot_ok'] += 1
            else:
                metrics['tot_nok'] += 1
    print(metrics)
    return data, metrics

def get_ok_nok_metrics(parts_info):
    """
    Get the OK/NOK parts metrics 
    """
    data = {}
    metrics = {'tot_ok': 0, 'tot_nok': 0}
    for part in parts_info:
        if part:
            data['id'] = part.id
            data['status'] = part.status
            if data['status'] == False:
                metrics['tot_ok'] += 1
            else:
                metrics['tot_nok'] += 1
    print(metrics)
    return data, metrics

def get_reworking_time_metrics(rework_parts_info):
    data = {'id': [], 'working_time': []}
    metrics = {'avg': 0.0, 'min': 0.0, 'max': 0.0, 'std': 0.0}
    if len(rework_parts_info) != 0:
        for part in rework_parts_info:
            data['id'].append(part.id)
            data['working_time'].append(part.working_time)
        dat_ = np.array(data['working_time'])
        metrics['min'] = min(data['working_time'])
        metrics['max'] = max(data['working_time'])
        metrics['avg'] = np.mean(dat_, axis=0)
        metrics['std'] = np.std(dat_, axis=0)
    return data, metrics


def get_working_time_metrics(parts_info):
    data = {'id': [], 'working_time': []}
    metrics = {'avg': 0.0, 'min': 0.0, 'max': 0.0, 'std': 0.0}
    if len(parts_info) != 0:
        for part in parts_info:
            data['id'].append(part.id)
            data['working_time'].append(part.working_time)
        dat_ = np.array(data['working_time'])
        metrics['min'] = min(data['working_time'])
        metrics['max'] = max(data['working_time'])
        metrics['avg'] = np.mean(dat_, axis=0)
        metrics['std'] = np.std(dat_, axis=0)
    return data, metrics


def get_data_ok_nok_from_static_period(period):
    metrics = {}
    # Month [Default]
    limInfDate = date.today() + timedelta(days=-30)
    if period == "Week":
        print('In week!!!')
        limInfDate = date.today() + timedelta(days=-7)
    elif period == "Day":
        limInfDate = date.today() + timedelta(days=-1)
        print('In Day!!!')

    parts_info = get_parts_ok_nok_timewindow(limInfDate, datetime.now())
    data, metrics = get_ok_nok_metrics(parts_info)
    metrics['date_start'] = limInfDate.strftime("%d/%m/%Y")
    metrics['date_end'] = datetime.now().strftime("%d/%m/%Y")
    return metrics

def get_data_working_time_from_static_period(period):
    metrics = {}
    # Month [Default]
    limInfDate = date.today() + timedelta(days=-30)
    if period == "Week":
        print('In week!!!')
        limInfDate = date.today() + timedelta(days=-7)
    elif period == "Day":
        limInfDate = date.today() + timedelta(days=-1)
        print('In Day!!!')
    
    parts_info = get_parts_working_time_timewindow(limInfDate, datetime.now())
    data, metrics = get_working_time_metrics(parts_info)
    metrics['date_start'] = limInfDate.strftime("%d/%m/%Y")
    metrics['date_end'] = datetime.now().strftime("%d/%m/%Y")
    metrics['data'] = data
    return metrics 


def get_data_rework_ok_nok_from_static_period(period):
    metrics = {}
    # Month [Default]
    limInfDate = date.today() + timedelta(days=-30)
    if period == "Week":
        print('In week!!!')
        limInfDate = date.today() + timedelta(days=-7)
    elif period == "Day":
        limInfDate = date.today() + timedelta(days=-1)
        print('In Day!!!')

    rework_parts_info = get_parts_rework_ok_nok(limInfDate, datetime.now())
    data, metrics = get_rework_ok_nok_metrics(rework_parts_info)
    metrics['date_start'] = limInfDate.strftime("%d/%m/%Y")
    metrics['date_end'] = datetime.now().strftime("%d/%m/%Y")
    return metrics

def get_lim_date(period):
    # Month [Default]
    limInfDate = date.today() + timedelta(days=-30)
    if period == "Week":
        print('In week!!!')
        limInfDate = date.today() + timedelta(days=-7)
    elif period == "Day":
        limInfDate = date.today() + timedelta(days=-1)
        print('In Day!!!')
    return limInfDate

def get_data_reworking_time_from_static_period(period):
    metrics = {}
    print(period, '::: reworking time')
    limInfDate = get_lim_date(period)
    rework_parts_info = get_parts_reworking_time_timewindow(limInfDate, datetime.now())
    data, metrics = get_reworking_time_metrics(rework_parts_info)
    metrics['date_start'] = limInfDate.strftime("%d/%m/%Y")
    metrics['date_end'] = datetime.now().strftime("%d/%m/%Y")
    metrics['data'] = data
    return metrics 
