from flask import Flask, render_template,request, redirect, url_for, jsonify
import mysql.connector
import socket
import os
from concurrent.futures import ThreadPoolExecutor
from app import check_ports



app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="*************",
        user="*******",
        password="******",
        database="new_schema1"
    )

@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("home.html", devices=devices)

#SİL
@app.route("/delete/<int:id>")
def delete_device(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM devices WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home'))  # silme sonrası ana sayfaya dön


#DÜZENLE
@app.route("/edit", methods=["GET", "POST"])
def edit():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    id = request.form.get('id')
    name = request.form.get('name')
    marka = request.form.get('marka')
    model = request.form.get('model')
    lokasyon = request.form.get('lokasyon')
    external_IP = request.form.get('external_IP')
    internal_IP = request.form.get('internal_IP')
    external_port = request.form.get('external_port')
    internal_port = request.form.get('internal_port')
    Guest_OS = request.form.get('Guest_OS')



    # SQL UPDATE
    sql = "UPDATE devices SET name=%s, marka=%s, model=%s, lokasyon=%s, external_IP=%s, internal_IP=%s, external_port =%s , internal_port =%s, Guest_OS=%s WHERE id=%s"
    cursor.execute(sql, (name, marka, model, lokasyon, external_IP , internal_IP ,external_port , internal_port, Guest_OS, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home'))  # güncelleme sonrası ana sayfaya dön

#EKLE
@app.route("/ekle", methods=["GET", "POST"])
def ekle():
    if request.method == "POST":
        # Formdan gelen veriler
        name = request.form["name"]
        marka = request.form["marka"]
        model = request.form["model"]
        lokasyon = request.form["lokasyon"]
        external_IP = request.form["external_IP"]
        internal_IP = request.form["internal_IP"]
        external_port = request.form["external_port"]
        internal_port = request.form["internal_port"]
        Guest_OS = request.form["Guest_OS"]


        # Veritabanına ekleme
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO devices (name, marka, model, lokasyon, external_IP, internal_IP, external_port, internal_port, Guest_OS ) VALUES (%s, %s, %s, %s, %s, %s,%s,%s, %s)",
            (name, marka, model, lokasyon, external_IP, internal_IP, external_port, internal_port, Guest_OS )
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("home"))  # ekleme sonrası ana sayfaya dön

    # GET method: formu göster
    return render_template("ekle.html")



#SORGULA
@app.route("/sorgula/<int:id>")
def sorgula(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT external_IP, external_port FROM devices WHERE id = %s", (id,))
    row = cursor.fetchone()
    external_ip = row['external_IP']
    external_port = row['external_port']

    port_status=(check_ports(external_ip, external_port))
    print(port_status)
    print (external_port) 
    
    
   #Veritabanından alınan portlar ve fonksiyondan dönen port durumları karşılaştırılıyor. Çünkü fonksiyon sadece açık olanların numarasını döndürüyor. 
    
    ports = [p.strip() for p in external_port.split(",")]
    status=[p.strip() for p in port_status.split(",")]
    
    cursor.execute("SELECT name, marka, model, lokasyon , external_IP, internal_IP FROM devices WHERE id = %s", (id,))
    device = cursor.fetchone()
    
    cursor.close()
    conn.close()
    counter=0
    result=[]
    for p in ports: 
        if p==status[counter]:
            counter+=1
            result.append("Açık")
        else:
            result.append("Kapalı")
            
      
    # render_template("index.html", device=device, devices=zip(ports, result))
    return  render_template("index.html", device=device, devices=zip(ports, result))

#ARA
@app.route('/ara')
def ara():
    allowed_categories = ["name", "marka", "model", "lokasyon", "external_IP", "internal_IP"]

    category = request.args.get("category")
    input_value = request.args.get("search")

    if category not in allowed_categories:
        # güvenlik için default bir değer
        category = "name"

    query = f"SELECT * FROM devices WHERE {category} LIKE %s"
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, ('%' + input_value + '%',))
    results = cursor.fetchall()
    return render_template("home.html", devices=results)


@app.route("/autocomplete")
def autocomplete():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = request.args.get("q", "")
    category = request.args.get("category", "name")

    # Güvenlik için sadece belirlenen kolonlara izin ver
    allowed_columns = ["name", "marka", "model", "lokasyon", "external_IP", "internal_IP"]
    if category not in allowed_columns:
        category = "name"

    sql = f"SELECT {category} FROM devices WHERE {category} LIKE %s LIMIT 5"
    cursor.execute(sql, ('%' + query + '%',))
    results = [row[category] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return jsonify(results)



if __name__ == "__main__":
    app.run(debug=True)
