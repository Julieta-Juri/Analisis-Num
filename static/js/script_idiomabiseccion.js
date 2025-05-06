const traducciones = {
    es: {
        titulo:"Bisección",
        Funcion:"Función",
        Intervalo:"Intervalo",
        Tolerancia:"Tolerancia",

  
},
    en: {
        titulo:"Bisection method",
        Funcion:"Function",
        Intervalo:"Interval",
        Tolerancia:"Tolerance",


}
};

document.addEventListener("DOMContentLoaded", function () {
    const selector = document.getElementById("idioma");

    selector.addEventListener("change", function () {
    const idioma = this.value;
      // Cambiar textos del título y los enlaces

 


    //titulo
    document.getElementById("titulobis").textContent = traducciones[idioma].titulo;
    //funcion,intervalo y tolerancia
    document.getElementById("funcion").textContent = traducciones[idioma].Funcion;
    document.getElementById("intervalo").textContent = traducciones[idioma].Intervalo;
    document.getElementById("tolerancia").textContent = traducciones[idioma].Tolerancia;
    



    });
});
