from flask import Flask, jsonify, request, render_template
from werkzeug import secure_filename
import json 
import datetime
app = Flask(__name__)
inputfile = 'cms_sample.txt'


@app.route('/uploader')
def upload_file():
    #rendering index file to upload text file
    return render_template('index.html')


@app.route('/api/parse', methods=['POST'])
def upload_file1():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        #calling get_json() service internally
        json_data = get_json()
        print json_data.headers
        #saving the get_json returned data to post.json
        with open('post.json', 'w') as output_file:
            json.dump(json_data.response, output_file)
        return str(json_data.headers) + str(json_data.status) + "<br> Parsing done and File Uploaded Successfully"
    else:
        return "Invalid Request type"
    

# simple function for getting relevant data
def split_and_get(item):
    item = item.split(':')
    return item[1].strip(' ')


@app.route('/api/sample', methods=['GET'])
def get_json():
    result = []
    #populating result list
    with open('cms_sample.txt') as myfile:
        for line in myfile:
            result.append(line.strip('\n'))

    result = filter(None, result)
    mydict = {}
    address_list = []
    coverage_list = []
    result_dict = {}
    if result.__contains__('Demographic'):
        start = result.index('Demographic')+2
        end = result.index('Emergency Contact')
        #populating dictionary object (mydict)
        for item in result[start:end]:
            if "Name" in item:
                item = item.split(' ')
                mydict['Name'] = {}
                mydict['Name']['first_name'] = item[1]
                mydict['Name']['last_name'] = item[2]
            elif "Date of Birth" in item:
                mydict['dob'] = split_and_get(item)
            elif "Address" in item:
                item = item.split(':')
                if item[1] is not '':
                    address_list.append(item[1])
                mydict['address'] = address_list
            elif "City" in item:
                mydict['city'] = split_and_get(item)
            elif "State" in item:
                mydict['state'] = split_and_get(item)
            elif "Zip" in item:
                mydict['zip'] = split_and_get(item)
            elif "Phone" in item:
                mydict['phone'] = split_and_get(item)
            elif "Email" in item:
                mydict['email'] = split_and_get(item)
            elif "Part" in item:
                item = item.split(' ')
                coverage_list.append({'type': item[0] + item[1], 'effective_date':item[4]})
                mydict['coverage'] = coverage_list

        #getting current time and date
        now = datetime.datetime.now()
        date_time = now.strftime("%m-%d-%Y %I:%M %p")
        #populating result dictionary
        result_dict['data'] = mydict
        result_dict['metadata'] = date_time
    #returning flask.response() that has header, status and response object
    return jsonify(result_dict)


if __name__ == '__main__':
    app.run(debug=True)

