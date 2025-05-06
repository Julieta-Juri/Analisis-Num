const traducciones = {
    es: {

    descripcion1:"Fundada en 2025, MathInApp es una iniciativa desarrollada por un equipo de estudiantes apasionados por las ciencias exactas y la programación. Nuestro objetivo es facilitar el acceso a herramientas que ayuden a resolver métodos numéricos de manera clara, rápida y gratuita.",
    titulo:"Compañia",
    titulo1:"Dirección",
    titulo2:"Productos",
    descripcion2:"Nuestra calculadora científica está potenciada por una combinación de programación matemática y diseño intuitivo. MathInApp permite resolver problemas paso a paso, simulando el acompañamiento de un profesor, y está pensada para estudiantes de nivel secundario y universitario",
    titulo11:"Dirección",
    inicio:"Volver",
    lenguaje:"idioma",
},
    en: {

    descripcion1:"Founded in 2025, MathInApp is an initiative developed by a team of students passionate about exact sciences and programming. Our goal is to facilitate access to tools that help solve numerical methods clearly, quickly, and for free",
    titulo: "Company",
    titulo1:"Direction",
    titulo2:"Products",
    descripcion2:"Our scientific calculator is powered by a combination of mathematical programming and intuitive design. MathInApp allows you to solve problems step by step, simulating teacher guidance, and is designed for high school and college students",
    titulo11:"Direction",
    inicio:"Return",
    lenguaje:"idioma"
}
};

document.addEventListener("DOMContentLoaded", function () {
    const selector = document.getElementById("idioma");

    selector.addEventListener("change", function () {
    const idioma = this.value;
      // Cambiar textos del título y los enlaces

    //   sobre nosotros, descripciones
    document.getElementById("descripcion1").textContent = traducciones[idioma].descripcion1;
    document.getElementById("descripcion2").textContent = traducciones[idioma].descripcion2;
    
    //inicio
    document.getElementById("link-nosotros").textContent = traducciones[idioma].inicio;


    //idioma
    document.getElementById("idioma").textContent = traducciones[idioma].lenguaje;
    

    //titulos
    document.getElementById("titulo").textContent = traducciones[idioma].titulo;
    document.getElementById("titulo1").textContent = traducciones[idioma].titulo1;
    document.getElementById("titulo2").textContent = traducciones[idioma].titulo2;
    document.getElementById("titulo11").textContent = traducciones[idioma].titulo11;


    });
});
