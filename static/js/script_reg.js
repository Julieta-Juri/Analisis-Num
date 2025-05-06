document.getElementById("mostrarNota").addEventListener("click", function() {
    // function es una funcion INTERNA 
    // cuando se haga click en el boton mostrar nota Agrega un "escuchador de eventos". O sea: cuando alguien hace clic en ese botón, se ejecuta el código que está dentro del function().
    const nota = document.getElementById("notaImportante");
    // 
    nota.classList.toggle("abierta");
});
