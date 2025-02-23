from flask import Flask, jsonify
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/dbtest')
def test_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        
        if conn.is_connected():
            db_info = conn.get_server_info()
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return jsonify({
                'status': 'success',
                'message': f'Connected to MySQL Server version {db_info}',
                'database': db_name
            })
            
    except Error as e:
        return jsonify({
            'status': 'error',
            'message': f'Error connecting to database: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 