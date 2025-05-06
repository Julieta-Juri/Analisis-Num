const traducciones = {
    es: {
      titulo: "Calculadora de Métodos Científicos",
      nosotros: "Sobre nosotros",
      biseccion: "Bisección",
      regula_falsi: "Regula Falsi",
      gauss_seidal: "Gauss-Seidal",
      jacobiano: "Jacobiano",
      gauss_jordan: "Gauss-Jordan",
      secante: "Secante",
      newton: "Newton-Raphson",
      irMetodo: "Ir al método",
      guia: "Guia",
      descripcionbiseccion:"Guía de funciones",
    },
    en: {
      titulo: "Scientific Methods Calculator",
      nosotros: "About us",
      biseccion: "Bisection",
      regula_falsi: "Regula Falsi",
      gauss_seidal: "Gauss-Seidel",
      jacobiano: "Jacobian",
      gauss_jordan: "Gauss-Jordan",
      secante: "Secant",
      newton: "Newton-Raphson",
      irMetodo: "Go to method",
      guia: "Guide",
      descripcionbiseccion:"Guide of funcions",
    }
  };
  
  document.addEventListener("DOMContentLoaded", function () {
    const selector = document.getElementById("idioma");
  
    selector.addEventListener("change", function () {
      const idioma = this.value;
      // Cambiar textos del título y los enlaces
      document.getElementById("titulo").textContent = traducciones[idioma].titulo;
      document.getElementById("link-nosotros").textContent = traducciones[idioma].nosotros;
      
      // Cambiar los títulos de las tarjetas
      document.getElementById("biseccion-titulo").textContent = traducciones[idioma].biseccion;
      document.getElementById("regula-falsi-titulo").textContent = traducciones[idioma].regula_falsi;
      document.getElementById("gauss-seidal-titulo").textContent = traducciones[idioma].gauss_seidal;
      document.getElementById("jacobiano-titulo").textContent = traducciones[idioma].jacobiano;
      document.getElementById("gauss-jordan-titulo").textContent = traducciones[idioma].gauss_jordan;
      document.getElementById("secante-titulo").textContent = traducciones[idioma].secante;
      document.getElementById("newton-titulo").textContent = traducciones[idioma].newton;

      // Cambiar los botones de cada tarjeta
      document.getElementById("boton1").textContent = traducciones[idioma].irMetodo;
      document.getElementById("boton2").textContent = traducciones[idioma].irMetodo;
      document.getElementById("boton3").textContent = traducciones[idioma].irMetodo;
      document.getElementById("boton4").textContent = traducciones[idioma].irMetodo;
      document.getElementById("boton5").textContent = traducciones[idioma].irMetodo;
      document.getElementById("boton6").textContent = traducciones[idioma].irMetodo;
      document.getElementById("boton7").textContent = traducciones[idioma].irMetodo;

    //   sobre nosotros
    document.getElementById("descripcion1").textContent = traducciones[idioma].descripcion1;


    });
  });
  