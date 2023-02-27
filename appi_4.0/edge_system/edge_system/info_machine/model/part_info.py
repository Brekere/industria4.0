from edge_system import db


class Part(db.Model):
    """
    This class is used to display the information of the OK and NOK parts/pieces
    """
    __tablename__ = "parts"
    id = db.Column(db.Integer, primary_key = True)
    id_machine = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    status = db.Column(db.Boolean)
    working_time = db.Column(db.BigInteger)

    def __init__(self, id_machine, timestamp, status, working_time):
        self.id_machine = id_machine
        self.timestamp = timestamp
        self.status = status
        self.working_time = working_time

    def __repr__(self):
        return '<id Machine: {}> \n\t\t ok: {} \n\t\t Time {} ms'.format(self.id_machine, self.status, self.working_time)

## crear clase última subida al servidor, para que se guarde el indice yu la fecha de la última vez que se subio la información 
#### al servidor y cuantos registros se subieron y  a lo mejor guardar de que a que indice se subió



class UploadPartsHist(db.Model):
    """
    This class is used to track the upload records from the parts
    """
    __tablename__ = "upload_parts_hist"
    id = db.Column(db.Integer, primary_key = True)
    upload_date = db.Column(db.DateTime)
    start_idx = db.Column(db.Integer, db.ForeignKey('parts.id'))
    end_idx = db.Column(db.Integer, db.ForeignKey('parts.id'))
    tot_records = db.Column(db.Integer)
    
    def __init__(self, upload_date, start_idx, end_idx, tot_records):
        self.upload_date = upload_date
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.tot_records = tot_records

    def __repr__(self):
        return 'Upload (part) date :: {}, last idx = {}'.format(self.upload_date, self.end_idx)