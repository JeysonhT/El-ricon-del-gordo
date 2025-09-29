from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
user_ct = Blueprint("user", __name__)

@user_ct.route('/User')
def get_users():
    users = [
        {"id": 1, "nombre": "Ana", "email": "ana@example.com"},
        {"id": 2, "nombre": "Luis", "email": "luis@example.com"},
        {"id": 3, "nombre": "María", "email": "maria@example.com"},
    ]
    return render_template('users.html', users=users)

# Lista de contactos
contacts = [
    {"nombre": "Maria", "numero": 67890656, "correo": "maria@example.com"},
    {"nombre": "Luis", "numero": 89897656, "correo": "Luis@example.com"},
    {"nombre": "Petrona", "numero": 87324567, "correo": "Petrona@example.com"},
]

@user_ct.route('/contacts', methods=['GET', 'POST'])
def manage_contacts():
    if request.method == 'POST':
        contact = {
            'nombre': request.form.get('nombre'),
            'numero': request.form.get('numero'),
            'correo': request.form.get('correo'),
        }
        contacts.append(contact)
    
    return render_template('contact.html', contacts=contacts)
    
@user_ct.route('/delete-contact', methods=['POST'])
def delete_contact():
    nombre = request.form.get('nombre')
    
    global contacts
    contacts = [contact for contact in contacts if contact['nombre'] != nombre]
    
    return redirect(url_for('user.manage_contacts'))
