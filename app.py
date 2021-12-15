
# importing the necessary dependencies
import numpy as np
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST']) #'GET' route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            national_inventory=float(request.form['national_inventory'])
            lead_time = float(request.form['lead_time'])
            in_transit_qty = float(request.form['in_transit_qty'])
            forecast_3_month_values = float(request.form['forecast_3_month_value'])
            sales_1_month = float(request.form['1_month_sales'])
            sales_9_month = float(request.form['sales_9_month'])

            filename = 'model.pkl'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction=loaded_model.predict(np.array([[national_inventory,lead_time,in_transit_qty,forecast_3_month_values,sales_1_month,sales_9_month]]))
            def change (prediction):     #custom function to change the formate of result in Yes and No format
                if prediction == 1:
                    return 'Product went to back order'
                else:
                    return 'Product didnt go to back order'
            #showing the prediction results in a UI
            return render_template('Result.html',prediction=change(prediction))
        except Exception as e:
          print('The Exception message is: ',e)
        return 'something is wrong'
          #return render_template('Results.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app
