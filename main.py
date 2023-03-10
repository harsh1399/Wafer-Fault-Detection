from wsgiref import simple_server
from flask import Flask, request, render_template,send_file
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction
import json

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)
app.config['UPLOAD_FOLDER'] = "Uploaded_files"

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.method == "POST":
            file_obj = request.files['file']
            if file_obj.filename != '':
                file_obj.save(os.path.join(app.config['UPLOAD_FOLDER'],file_obj.filename))
                path = "./Uploaded_files"
            else:
                path = "./Prediction_Batch_files"
            pred_val = pred_validation(path) #object initialization
            pred_val.prediction_validation() #calling the prediction_validation function
            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path= pred.predictionFromModel()
            return render_template("prediction.html", message="Prediction file created")
            #return Response("Prediction File created at !!!"  +str(path) +'and few of the predictions are '+str(json.loads(json_predictions) ))
    except ValueError:
        return render_template("prediction.html", message="Error Occurred! %s" % ValueError)
    except KeyError:
        return render_template("prediction.html", message="Error Occurred! %s" % KeyError)
    except Exception as e:
        return render_template("prediction.html", message="Error Occurred! %s" % e)


# @app.route("/train", methods=['POST'])
# @cross_origin()
# def trainRouteClient():
#
#     try:
#         if request.json['folderPath'] is not None:
#             path = request.json['folderPath']
#
#             train_valObj = train_validation(path) #object initialization
#
#             train_valObj.train_validation()#calling the training_validation function
#
#
#             trainModelObj = trainModel() #object initialization
#             trainModelObj.trainingModel() #training the model for the files in the table
#
#
#     except ValueError:
#
#         return Response("Error Occurred! %s" % ValueError)
#
#     except KeyError:
#
#         return Response("Error Occurred! %s" % KeyError)
#
#     except Exception as e:
#
#         return Response("Error Occurred! %s" % e)
#     return Response("Training successfull!!")

@app.route("/download")
@cross_origin()
def download_file():
    path = "Prediction_Output_File/Predictions.csv"
    return send_file(path,as_attachment=True)


port = int(os.getenv("PORT",5000))
if __name__ == "__main__":
    # host = '0.0.0.0'
    # #port = 5000
    # httpd = simple_server.make_server(host, port, app)
    # # print("Serving on %s %d" % (host, port))
    # httpd.serve_forever()
    app.run()