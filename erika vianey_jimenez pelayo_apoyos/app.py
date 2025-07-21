from flask import Flask, render_template, request, redirect, url_for
from models.pila import PilaApoyos
from models.cola import ColaTarjetas

app = Flask(__name__)

# Instancias globales (para demo, no producción)
pila = PilaApoyos()
cola = ColaTarjetas()

@app.route('/')
@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/cola', methods=['GET', 'POST'])
def vista_cola():
    mensaje = ''
    if request.method == 'POST':
        if 'agregar' in request.form:
            persona = request.form.get('persona')
            if persona:
                cola.encolar(persona)
                mensaje = f'Persona "{persona}" agregada a la cola.'
        elif 'atender' in request.form:
            atendido = cola.desencolar()
            if atendido:
                mensaje = f'Se atendió a: {atendido}'
            else:
                mensaje = 'La cola está vacía.'
    return render_template('cola.html', cola=cola.mostrar(), mensaje=mensaje)

@app.route('/pila', methods=['GET', 'POST'])
def vista_pila():
    mensaje = ''
    if request.method == 'POST':
        if 'agregar' in request.form:
            apoyo = request.form.get('apoyo')
            if apoyo:
                pila.empilar(apoyo)
                mensaje = f'Apoyo "{apoyo}" agregado al historial.'
        elif 'quitar' in request.form:
            quitado = pila.desempilar()
            if quitado:
                mensaje = f'Se quitó el apoyo: {quitado}'
            else:
                mensaje = 'El historial está vacío.'
    return render_template('pila.html', pila=pila.mostrar(), mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)
