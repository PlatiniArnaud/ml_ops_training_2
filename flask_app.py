from flask import Flask, jsonify, request
from pickle import dump, load
from logzero import logger, logfile
from datetime import datetime

logfile('app.log', maxBytes = 1e6, backupCount = 3, disableStderrLogger = True)

model = load(open("model.pkl", 'rb'))

app = Flask(__name__)
logger.info(f'Flask app started.')
@app.route('/')
def health_check():
    return "OK"

@app.route('/predict', methods = ['POST'])
def predict():
    try:
        input_data = request.json
        if not input_data:
            return jsonify({'message': 'No input data provided!'}), 400
        
        values_list = [list(input_data.values())]
        prediction = model.predict(values_list)

        if prediction[0] == 0:
            prediction_result = 'Not likely to purchase.'
        elif prediction[0] == 1:
            prediction_result = 'Likely to prurchase.'

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f" A request was made at {current_datetime} with an INPUT DATA {input_data} and the response was {prediction_result}")

        return jsonify({'prediction': prediction_result}), 200
    
    except Exception as e:
        logger.info(f" A request was made at {current_datetime} with an INPUT DATA {input_data} and the response was {prediction_result}")
        #logger.error(f"{current_datetime} - Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
        app.run(host = "0.0.0.0", port = 5000, debug=True)