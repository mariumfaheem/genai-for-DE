# app.py
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    column_to_impute = request.form.get('column_to_impute')
    
    if file and file.filename.endswith('.csv'):
        # Read the CSV file
        df = pd.read_csv(file)
        
        if column_to_impute not in df.columns:
            return jsonify({'error': f'Column "{column_to_impute}" not found in the CSV file'})
        
        # Impute missing values with column mean for the specified column
        df[column_to_impute] = df[column_to_impute].fillna(df[column_to_impute].mean())
        
        # Convert the imputed dataframe to CSV
        output = io.StringIO()
        df.to_csv(output, index=False)
        
        return jsonify({'data': output.getvalue(), 'columns': df.columns.tolist()})
    
    return jsonify({'error': 'Invalid file format'})

@app.route('/download', methods=['POST'])
def download_csv():
    csv_data = request.form.get('csv_data')
    if not csv_data:
        return jsonify({'error': 'No CSV data provided'})
    
    # Create a BytesIO object
    buffer = io.BytesIO()
    buffer.write(csv_data.encode())
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='imputed_data.csv',
        mimetype='text/csv'
    )

if __name__ == '__main__':
    app.run(debug=True)