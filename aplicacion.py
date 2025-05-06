from flask import Flask, render_template, request
import io
import base64
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import ast
import re

app=Flask(__name__)
# __name__ le ayuda a Flask a ubicarse dentro de tu proyecto, __name__ representa nuestro proyecto.

orden_variables = ['x', 'y', 'z']

def parsear_ecuacion(ecuacion, orden_variables):
    ecuacion = ecuacion.replace(' ', '')
    izquierda, derecha = ecuacion.split('=')

    terminos = re.findall(r'([+-]?\d*\.?\d*)([a-zA-Z]+)', izquierda)
    diccionario_coef = {}

    for num, var in terminos:
        if num in ('', '+'):
            coef = 1.0
        elif num == '-':
            coef = -1.0
        else:
            coef = float(num)
        diccionario_coef[var] = coef

    coeficientes = [diccionario_coef.get(var, 0.0) for var in orden_variables]
    coeficientes.append(float(derecha))
    return coeficientes

def biseccion(f, a, b, tol, max_iter=100):
    if f(a) * f(b) >= 0:
        return "No hay cambio de signo en el intervalo.", None

    iteraciones = 0
    error = np.inf
    punto_anterior = a

    while error > tol and iteraciones < max_iter:
        punto = (a + b) / 2
        f_p = f(punto)

        if iteraciones > 0:
            error = abs((punto - punto_anterior) / punto) * 100

        if f(a) * f_p < 0:
            b = punto
        else:
            a = punto

        punto_anterior = punto
        iteraciones += 1

    return punto, error

def regula_falsi(f, a, b, tol, max_iter=100):
    pasos = []
    if f(a) * f(b) >= 0:
        return [("No hay cambio de signo en el intervalo.", None)]

    iteraciones = 0
    error = np.inf
    punto_anterior = a

    while error > tol and iteraciones < max_iter:
        fa = f(a)
        fb = f(b)

        punto = b - (fb * (b - a)) / (fb - fa)
        f_p = f(punto)

        if iteraciones > 0:
            error = abs((punto - punto_anterior) / punto) * 100

        pasos.append((iteraciones+1, a, b, punto, f_p, error))

        if fa * f_p < 0:
            b = punto
        else:
            a = punto

        punto_anterior = punto
        iteraciones += 1

    return punto, error

def jacobi(A, b, tol=1e-10, max_iter=100):
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        punto = np.zeros_like(b)  # Inicializamos la raíz en ceros
        n = len(A)

        for iteracion in range(max_iter):
            punto_nuevo = np.zeros_like(punto)
            for i in range(n):
                suma = sum(A[i][j] * punto[j] for j in range(n) if j != i)
                punto_nuevo[i] = (b[i] - suma) / A[i][i]

            # Calculamos el error de la iteración
            error = np.linalg.norm(punto_nuevo - punto, ord=np.inf)

            # Si el error es menor que la tolerancia, retornamos el punto y el error
            if error < tol:
                return punto_nuevo, error

            # Si no se cumple la tolerancia, actualizamos punto
            punto = punto_nuevo

        # Si llegamos al máximo de iteraciones, retornamos el último valor de punto y el error
        return punto, error
    except Exception as e:
        return f"Error en los datos: {str(e)}"

def metodo_gauss_jordan(matriz):
    n = len(matriz)
    for i in range(n):
        pivote = matriz[i][i]
        if pivote == 0:
            for j in range(i + 1, n):
                if matriz[j][i] != 0:
                    matriz[i], matriz[j] = matriz[j], matriz[i]
                    pivote = matriz[i][i]
                    break
            else:
                raise ValueError("No se puede resolver: matriz singular o sistema indeterminado.")
        matriz[i] = [x / pivote for x in matriz[i]]
        for j in range(n):
            if j != i:
                factor = matriz[j][i]
                matriz[j] = [a - factor * b for a, b in zip(matriz[j], matriz[i])]
    return [fila[-1] for fila in matriz]

def newton_raphson(func_str, punto0, tolerancia=1e-6, max_iter=100):
    # Definir la variable simbólica
    x = sp.symbols('x')

    # Parsear la función ingresada
    func = sp.sympify(func_str)

    # Calcular la derivada de la función
    f_derivada = sp.diff(func, x)

    # Función lambda para evaluar las expresiones en cada iteración
    f = sp.lambdify(x, func, "numpy")
    f_prime = sp.lambdify(x, f_derivada, "numpy")

    # Inicializar el valor de x
    punto = punto0

    for i in range(max_iter):
        fx = f(punto)
        fdx = f_prime(punto)

        if fdx == 0:
            return None, None, f"Error: Derivada cero en la iteración {i+1}. El método falla."

        # Método de Newton-Raphson
        punto1 = punto - fx / fdx
        error = abs(punto1 - punto)

        if error < tolerancia:
            return punto1, error, f"Raíz encontrada: {punto1} en {i+1} iteraciones con un error de {error}"

        punto = punto1

    return None, None, "No se alcanzó la convergencia."

def metodo_secante(funcion_str, punto0, punto1, tolerancia=1e-6, max_iter=100):
    x = sp.symbols('x')
    try:
        f_expr = sp.sympify(funcion_str)
        f = sp.lambdify(x, f_expr, "numpy")
    except Exception as e:
        return None, None, f"Error al procesar la función: {e}"

    for i in range(max_iter):
        f_punto0 = f(punto0)
        f_punto1 = f(punto1)

        if f_punto1 - f_punto0 == 0:
            return None, None, "Error: División por cero en la fórmula de la secante."

        punto2 = punto1 - f_punto1 * (punto1 - punto0) / (f_punto1 - f_punto0)

        if abs(punto2 - punto1) < tolerancia:
            error = abs(punto2 - punto1)
            return punto2, error, None

        punto0, punto1 = punto1, punto2

    return None, None, "No se alcanzó la convergencia."

def metodo_gauss_seidel(A, b, tol=1e-10, max_iter=100):
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        x = np.zeros_like(b)
        n = len(A)

        for _ in range(max_iter):
            x_nuevo = np.copy(x)
            for i in range(n):
                suma = sum(A[i][j] * x_nuevo[j] if j < i else A[i][j] * x[j] for j in range(n) if j != i)
                x_nuevo[i] = (b[i] - suma) / A[i][i]

            error = np.linalg.norm(x_nuevo - x, ord=np.inf)

            if error < tol:
                return x_nuevo.tolist(), error  # <<< Devuelve el vector solución y el error final

            x = x_nuevo

        return None, "No se alcanzó la tolerancia"  # <<< Si no converge
    except Exception as e:
        return None, f"Error: {e}"

##@app.route('/')
@app.route('/interpolacion')
def interpolacion():
    return render_template('interpolacion.html')
# este rempresenta la raiz principal
@app.route('/')
def index():
    return render_template('index.html')
# "Tomá el archivo index.html (que está en la carpeta templates) y mostralo en el navegador."
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/biseccion', methods=['GET', 'POST'])
def biseccion1():
    resultado = None
    error_final = None

    if request.method == 'POST':
        funcion_str = request.form['funcion']
        a = float(request.form['a'])
        b = float(request.form['b'])
        tol = float(request.form['tol'])
        x = sp.symbols('x')
        try:
            expr = sp.sympify(funcion_str)
            f = sp.lambdify(x, expr, 'numpy')
            resultado, error_final = biseccion(f, a, b, tol)
        except Exception as e:
            resultado = f"Error: {e}"
            error_final = None

    return render_template('bisección.html', resultado=resultado, error_final=error_final)
# "Tomá el archivo biseccion.html (que está en la carpeta templates) y mostralo en el navegador."

@app.route('/gauss_jordan', methods=['GET', 'POST'])
def gauss_jordan():
    soluciones = None
    cantidad = None
    if request.method == 'POST':
        try:
            cantidad = int(request.form['cantidad'])
        except:
            cantidad = None
        
        ecuaciones = [key for key in request.form.keys() if key.startswith('ecuacion')]
        
        if ecuaciones:
            # Ya mandaron las ecuaciones
            matriz = []
            for i in range(cantidad):
                ecuacion = request.form.get(f'ecuacion{i}')
                if ecuacion is None:
                    raise ValueError(f"No se encontró la ecuación {i}")
                fila = parsear_ecuacion(ecuacion, orden_variables)
                matriz.append(fila)
            soluciones = metodo_gauss_jordan(matriz)

    return render_template('Gauss-Jordan.html', cantidad=cantidad, soluciones=soluciones)
# "Tomá el archivo bss gaussjordan.html (que está en la carpeta templates) y mostralo en el navegador."

@app.route('/gauss-seidal' , methods=['GET', 'POST'])
def gauss_seidal():
    if request.method == 'POST':
        try:
            # Recibo los datos
            matriz_str = request.form['matriz']
            vector_str = request.form['vector']
            tol = float(request.form.get('tolerancia', 1e-10))

            # Parseo
            A = eval(matriz_str)
            b = eval(vector_str)

            raiz, error = metodo_gauss_seidel(A, b, tol)

            return render_template('Gauss-Seidal.html', raiz=raiz, error=error)
        except Exception as e:
            return render_template('Gauss-Seidal.html', error=f"Error en los datos: {e}")

    return render_template('Gauss-Seidal.html', raiz=None, error=None)
# "Tomá el archivo Gauss-seidal .html (que está en la carpeta templates) y mostralo en el navegador."

@app.route('/jacobiano', methods=['GET', 'POST'])
def jacobiano():
    resultado = None
    error_final = None

    if request.method == 'POST':
        try:
            # Recibiendo los datos del formulario
            A_str = request.form['A']
            b_str = request.form['b']
            tol = float(request.form['tol'])
            max_iter = int(request.form['max_iter'])
            
            # Usamos ast.literal_eval para convertir la entrada de manera segura
            A = np.array(ast.literal_eval(A_str), dtype=float)  # A es una matriz
            b = np.array(ast.literal_eval(b_str), dtype=float)  # b es un vector
            
            # Llamamos a la función de Jacobi
            resultado, error_final = jacobi(A, b, tol=tol, max_iter=max_iter)

        except Exception as e:
            # Si hay algún error, lo manejamos aquí
            resultado = f"Error: {e}"
            error_final = None

    # Convertir 'resultado' a un valor que pueda evaluarse correctamente en el template
    if isinstance(resultado, np.ndarray):
        resultado = resultado.tolist()  # Convertimos a lista para el template

    return render_template('jacobiano.html', resultado=resultado, error_final=error_final)
# "Tomá el jacobianoiseccion.html (que está en la carpeta templates) y mostralo en el navegador."


@app.route('/regula-falsi', methods=['GET', 'POST'])
def regula_falsi():
    resultado = None
    error_final = None

    if request.method == 'POST':
        funcion_str = request.form['funcion']
        a = float(request.form['a'])
        b = float(request.form['b'])
        tol = float(request.form['tol'])
        x = sp.symbols('x')
        try:
            expr = sp.sympify(funcion_str)
            f = sp.lambdify(x, expr, 'numpy')
            resultado, error_final = regula_falsi(f, a, b, tol)
        except Exception as e:
            resultado = f"Error: {e}"
            error_final = None
    return render_template('regula-falsi.html', resultado=resultado, error_final=error_final)

@app.route('/newton', methods=['GET', 'POST'])
def newton():
    if request.method == 'POST':
        funcion_str = request.form['funcion']
        punto_inicial = float(request.form['punto'])
        tolerancia = float(request.form['tolerancia'])
        max_iter = int(request.form['max_iter'])

        x = sp.symbols('x')
        try:
            funcion = sp.sympify(funcion_str)
            derivada = sp.diff(funcion, x)

            f = sp.lambdify(x, funcion, 'numpy')
            f_derivada = sp.lambdify(x, derivada, 'numpy')

            punto = punto_inicial
            for i in range(max_iter):
                fx = f(punto)
                fdx = f_derivada(punto)

                if fdx == 0:
                    return render_template('newton.html', funcion=funcion_str, derivada=str(derivada), mensaje="Error: Derivada cero. El método falla.")

                nuevo_punto = punto - fx / fdx

                if abs(nuevo_punto - punto) < tolerancia:
                    error = abs(nuevo_punto - punto)


                    # Generar gráfico
                    x_vals = np.linspace(punto_inicial - 5, punto_inicial + 5, 400)
                    y_vals = f(x_vals)

                    plt.figure()
                    plt.plot(x_vals, y_vals, label=str(funcion))
                    plt.axhline(0, color='gray', linestyle='--')
                    plt.axvline(punto_inicial, color='red', linestyle='--', label=f'p0 = {punto_inicial}')
                    plt.scatter(nuevo_punto, f(nuevo_punto), color='green', label=f'Raíz ≈ {nuevo_punto:.4f}')
                    plt.title("Gráfico de la función")
                    plt.legend()
                    plt.grid(True)

                    img = io.BytesIO()
                    plt.savefig(img, format='png')
                    img.seek(0)
                    grafico_base64 = base64.b64encode(img.getvalue()).decode()
                    plt.close()

                    return render_template('newton.html', funcion=funcion_str, derivada=str(derivada), raiz=nuevo_punto, error=error, grafico=grafico_base64)

                punto = nuevo_punto

            return render_template('newton.html', funcion=funcion_str, derivada=str(derivada), mensaje="No se alcanzó la convergencia.")
        except Exception as e:
            return render_template('newton.html', mensaje=f"Error: {e}")

    return render_template('newton.html')

# "Tomá el newtoniseccion.html (que está en la carpeta templates) y mostralo en el naveggauss_jordanador."

@app.route('/secante', methods=['GET', 'POST'])
def secante():
    resultado = None
    error = None
    funcion = None

    if request.method == 'POST':
        funcion = request.form['funcion']
        punto0 = float(request.form['punto0'])
        punto1 = float(request.form['punto1'])

        raiz, error_valor, mensaje_error = metodo_secante(funcion, punto0, punto1)

        if raiz is not None:
            resultado = {
                'raiz': raiz,
                'error': error_valor
            }
        else:
            error = mensaje_error

    return render_template('secante.html', resultado=resultado, error=error, funcion=funcion)
if __name__ == '__main__':
    app.run(debug=True)






"""
# Crear rango de x centrado en la raíz
x_vals = np.linspace(punto - 5, punto + 5, 400)

# Calcular y
try:
    y_vals = f(x_vals)
except Exception as e:
    return render_template('newton.html', mensaje=f"Error al graficar: {e}")

plt.figure()
plt.plot(x_vals, y_vals, label='f(x)')
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(punto, color='red', linestyle='--', label='Raíz aprox.')

# Limitar ejes para que no se explote
plt.ylim(-100, 100)  # Limita el eje Y
plt.xlim(punto - 5, punto + 5)  # Limita el eje X

plt.legend()
plt.grid(True)
plt.title("Gráfico de la función")

# Guardar imagen en base64
img = io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)
plot_url = base64.b64encode(img.getvalue()).decode()

# Pasarlo al HTML
return render_template('newton.html', funcion=funcion_str, derivada=str(derivada), raiz=punto, error=error, grafico=plot_url)

"""