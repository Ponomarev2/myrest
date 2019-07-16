#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for,render_template, Response

app = Flask(__name__)

subjects = [
    {
        'id': 1,
        'title': u'Computational Mathematics',
        'mark': u'Excellent!',
        'marknote_number': u'15415',
        'student_name': u'Vasily Ponomarev'
    },
    {
        'id': 2,
        'title': u'Computers and peripherals',
        'mark': u'Excellent!',
        'marknote_number': u'15415',
        'student_name': u'Vasily Ponomarev'
    },
    {
        'id': 3,
        'title': u'Electrical engineering, electronics and circuitry',
        'mark': u'Good',
        'marknote_number': u'15415',
        'student_name': u'Vasily Ponomarev'
    },
    {
        'id': 4,
        'title': u'Operating Systems',
        'mark': u'Excellent!',
        'marknote_number': u'15415',
        'student_name': u'Vasily Ponomarev'
    },
    {
        'id': 5,
        'title': u'For Delete',
        'mark': u'Excellent!',
        'marknote_number': 15416,
        'student_name': u'Vasily Ponomarev'
    }
]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



@app.route('/<int:number>', methods=['GET'])
def get_marks(number):
    subject = []
    for i in subjects:
        if i['marknote_number'] == number or i['marknote_number'] == str(number):
            subject.append(i)
    if len(subject) == 0:
        abort(404)
    else:
        return jsonify({'subjects': subject})


@app.route('/subjects', methods=['POST'])
def create_subject():
    if not request.json:
        if not 'title' in request.json:
            abort(400)
        abort(404)
    subject = {
        'id': subjects[-1]['id'] + 1,
        'title': request.json['title'],
        'mark': request.json.get('mark', ""),
        'marknote_number': request.json.get('marknote_number', ""),
        'student_name': request.json.get('student_name', "")
    }
    subjects.append(subject)
    return jsonify({'subjects': subjects}), 201


@app.route('/<int:subject_id>', methods=['PUT'])
def update_subject(subject_id):
    subject = []
    for i in subjects:
        if i['id'] == subject_id or i['id'] == str(subject_id):
            subject.append(i)
    if len(subject) == 0:
        abort(404)
    if not request.json:
        abort(400)
    subject[0]['title'] = request.json.get('title', subject[0]['title'])
    subject[0]['mark'] = request.json.get('mark', subject[0]['mark'])
    subject[0]['marknote_number'] = request.json.get('marknote_number', subject[0]['marknote_number'])
    subject[0]['student_name'] = request.json.get('student_name', subject[0]['student_name'])
    return jsonify({'subject': subject[0]})


@app.route('/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    subject = []
    for i in subjects:
        if i['id'] == subject_id or i['id'] == str(subject_id):
            subject.append(i)
    if len(subject) == 0:
        abort(404)
    subjects.remove(subject[0])
    return jsonify({'result': True})


def make_public_subject_list(subject_list):
    new_subject_list = []
    for i in subject_list:
        new_subject_list.append(make_public_subject(i))
    return new_subject_list


def make_public_subject(subject):
    new_subject = {}
    for field in subject:
        if field == 'id':
            new_subject['uri'] = url_for('get_subjects', subject_id=subject['id'], _external=True)
        else:
            new_subject[field] = subject[field]
    return new_subject


@app.route('/subjects', methods=['GET'])
def get_subjects():
    return jsonify({'subjects': subjects})


@app.route('/')
def index():
    return render_template("new.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

