from flask import render_template, request
from src.__init__ import create_app

app = create_app()

# ----------------- RUTAS -----------------

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    user = {'nombre': '', 'email': '', 'mensaje': ''}
    if request.method == 'GET':
        user['nombre'] = request.args.get('nombre', '')
        user['email'] = request.args.get('email', '')
        user['mensaje'] = request.args.get('mensaje', '')
    return render_template("contacto.html", usuario=user)

@app.route('/contactopost', methods=['GET', 'POST'])
def contactopost():
    user = {'nombre': '', 'email': '', 'mensaje': ''}
    if request.method == 'POST':
        user['nombre'] = request.form.get('nombre', '')
        user['email'] = request.form.get('email', '')
        user['mensaje'] = request.form.get('mensaje', '')
    return render_template("contactopost.html", usuario=user)

@app.route('/usuario')
def usuario():
    return render_template("usuario.html")

@app.route('/acercade')
def acercade():
    return render_template("acercade.html")

# ----------------- MAIN -----------------
if __name__ == '__main__':
    app.run(debug=True, port=8000)
