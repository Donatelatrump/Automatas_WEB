// Timestamp: 2021-05-25T18:22:04.000Z

let canvasContainer = document.getElementById('canvas');

let containerWidth = canvasContainer.clientWidth;
let containerHeight = canvasContainer.clientHeight;
let caracter;
let inicio = new Set();
let salida = new Set();
let numerosDisponibles = Array.from({length: 101}, (_, i) => i);
let k=0;
let contadorCurvas = 1;
let contadorPaths = 1;

function asignarNumeroEstado() {
    if (numerosDisponibles.length > 0) {
        return numerosDisponibles.shift();
    }
    return null; // En caso de que no haya números disponibles
}

function liberarNumeroEstado(numero) {
    numerosDisponibles.push(numero);
    numerosDisponibles.sort((a, b) => a - b); // Ordenar el arreglo para mantener los números en orden
}
// Crear el stage con las dimensiones del contenedor
canvasContainer.willReadFrequently = true; // Activa la optimización

let stage = new Konva.Stage({
    container: 'canvas',
    width: containerWidth,
    height: containerHeight,
});

let layer = new Konva.Layer({
    willReadFrequently: true, // Activa la optimización
});

stage.add(layer);

let objetos = [];
let inicioConexion = null;
let checkboxActivo = null;
let contadorEstados = 0;

// Asegúrate de tener un vector global para almacenar los estados seleccionados
let estadosSeleccionados = [];

function crearEstado(x, y) {
    let numeroEstado = asignarNumeroEstado();
    if (numeroEstado === null) {
        return null;
    }
    let grupo = new Konva.Group({
        x: x,
        y: y,
        draggable: false,
    });

    let estado = new Konva.Circle({
        x: 0,
        y: 0,
        radius: 20,
        fill: 'white',
        stroke: 'black',
        strokeWidth: 2,
        willReadFrequently: true,
    });

    let texto = new Konva.Text({
        x: -10,
        y: -7,
        text: `q${numeroEstado}`,
        fontSize: 14,
        fill: 'black',
        class: 'texto', // Asegúrate de asignar la clase 'texto' aquí
        willReadFrequently: true,
    });

    grupo.add(estado);
    grupo.add(texto);
    contadorEstados++;
    let pos = estado.getAbsolutePosition();
    grupo.datos = {
        nombre: texto.text(),
        x: pos.x,
        y: pos.y,
        numeroEstado: numeroEstado
    };

    // Añadir eventos de clic tanto al círculo como al texto
    estado.on('click', function() {
        if (checkboxActivo === null) {
            handleSeleccion(grupo);
        } else if (checkboxActivo === 'checkAgregarConexion') {
            if (inicioConexion === null) {
                inicioConexion = grupo.getChildren()[0].getAbsolutePosition(); // Obtiene la posición del círculo
            } else {
                let finConexion = grupo.getChildren()[0].getAbsolutePosition(); // Obtiene la posición del círculo
                let caracter = prompt('Agregar Caracter:');
                if (caracter !== null) {
                    crearConexion(inicioConexion, finConexion, caracter);
                }
                inicioConexion = null;}
        }
    });

    texto.on('click', function() {
        if (checkboxActivo === null) {
            handleSeleccion(grupo);
        } else if (checkboxActivo === 'checkAgregarConexion') {
            if (inicioConexion === null) {
                inicioConexion = grupo.getChildren()[0].getAbsolutePosition(); // Obtiene la posición del círculo
            } else {
                let finConexion = grupo.getChildren()[0].getAbsolutePosition(); // Obtiene la posición del círculo
                let caracter = prompt('Agregar Caracter:');
                if (caracter !== null) {
                    crearConexion(inicioConexion, finConexion, caracter);
                }
                inicioConexion = null;
            }
        }else if (checkboxActivo === 'checkEliminarEstado') {
            objetos.forEach(objeto => {
                let estado = objeto.find('Circle')[0];
                if (estado ===  grupo.getChildren()[0]) {
                    eliminarEstadoYConexiones(objeto);
                }
            });}
    });


    layer.add(grupo);
    objetos.push(grupo);
    return grupo;
}



function obtenerInicioYSalida() {
    return {
        inicio: inicio,
        salida: salida
    };
}



function handleSeleccion(grupo) {
    let estadoSeleccionado = grupo.datos;
    let circulo = grupo.getChildren()[0]; // Obtiene el círculo

    // Verifica si el estado ya está seleccionado
   ;
    let index = estadosSeleccionados.findIndex(estado => estado.nombre === estadoSeleccionado.nombre);
  
    if (index !== -1) {
        // Si el estado ya está seleccionado, deselecciónalo
        estadosSeleccionados.splice(index, 1);
        circulo.fill('white'); // Cambia el color de fondo a blanco
        ocultarInformacionEstado();
    } else {
        // Si el estado no está seleccionado, selecciónalo
        if (estadosSeleccionados.length > 0) {
            // Si hay otro estado seleccionado, intercambia la selección
            let grupoAnterior = objetos.find(obj => obj.datos.nombre === estadosSeleccionados[0].nombre);
            let circuloAnterior = grupoAnterior.getChildren()[0];
            circuloAnterior.fill('white'); // Cambia el color de fondo a blanco
            estadosSeleccionados = [];
            ocultarInformacionEstado();
        }

        estadosSeleccionados.push(estadoSeleccionado);
        mostrarInformacionEstado(estadoSeleccionado);
        circulo.fill('lightgreen'); // Cambia el color de fondo a verde claro
    }

    layer.draw(); // Actualiza la capa
}
function ocultarInformacionEstado() {
    document.getElementById('nombre').value = '';
    document.getElementById('coordenadaX').value = '';
    document.getElementById('coordenadaY').value = '';
    document.getElementById('inicio').checked = false;
    document.getElementById('salida').checked = false;
    
    document.querySelector('.info-container').style.display = 'none';
}
function mostrarInformacionEstado(estadoSeleccionado) {
    if (estadosSeleccionados.length > 0 && estadosSeleccionados[0] !== undefined) {
        document.getElementById('nombre').value = estadoSeleccionado.nombre;
        document.getElementById('coordenadaX').value = estadoSeleccionado.x;
        document.getElementById('coordenadaY').value = estadoSeleccionado.y;
        document.getElementById('inicio').disabled = false;
        document.getElementById('salida').disabled = false;

        if (inicio.has(estadoSeleccionado)) {
            document.getElementById('inicio').checked = true;
        } else {
            document.getElementById('inicio').checked = false;
        }

        if (salida.has(estadoSeleccionado)) {
            document.getElementById('salida').checked = true;
        } else {
            document.getElementById('salida').checked = false;
        }
    }

    document.querySelector('.info-container').style.display = 'block';
}



document.getElementById('inicio').addEventListener('change', function() {
    if (this.checked) {
        document.getElementById('salida').checked = false;

        if (estadosSeleccionados.length > 0) {
            estadosSeleccionados.forEach(estado => {
                inicio.add(estado);
                salida.delete(estado);
            });
        }
    } else {
        estadosSeleccionados.forEach(estado => {
            inicio.delete(estado);
        });
    }
});
document.getElementById('salida').addEventListener('change', function() {
    if (this.checked) {
        document.getElementById('inicio').checked = false;

        if (estadosSeleccionados.length > 0) {
            estadosSeleccionados.forEach(estado => {
                salida.add(estado);
                inicio.delete(estado);
            });
        }
    } else {
        estadosSeleccionados.forEach(estado => {
            salida.delete(estado);
        });
    }
});




// Añade un evento de clic al área de Konva para deseleccionar los estados
stage.on('click', function(e) {
    if (checkboxActivo === null) {
        // Verifica si se hizo clic fuera de un estado y sin ningún checkbox activo
        let target = e.target;

        if (target === stage) {
            // Deselecciona todos los estados
            estadosSeleccionados.forEach(estado => {
                let grupo = objetos.find(obj => obj.datos.nombre === estado.nombre);
                let circulo = grupo.getChildren()[0];
                circulo.fill('white'); // Cambia el color de fondo a blanco
                ocultarInformacionEstado();
            });

            estadosSeleccionados = [];
            layer.draw(); // Actualiza la capa
        }
    }
});



function dibujarFlecha(context, inicio, fin) {
    let headLength = 10;
    let dx = fin.x - inicio.x;
    let dy = fin.y - inicio.y;
    let angle = Math.atan2(dy, dx);
    
    context.moveTo(inicio.x, inicio.y);
    context.lineTo(fin.x, fin.y);
    
    context.lineTo(fin.x - headLength * Math.cos(angle - Math.PI / 6), fin.y - headLength * Math.sin(angle - Math.PI / 6));
    context.moveTo(fin.x, fin.y);
    context.lineTo(fin.x - headLength * Math.cos(angle + Math.PI / 6), fin.y - headLength * Math.sin(angle + Math.PI / 6));
}

function dibujarParabolaConFlecha(context, inicio, control1, control2, fin) {
    let headLength = 10;

    // Dibujar la parábola
    context.beginPath();
    context.moveTo(inicio.x, inicio.y);
    context.bezierCurveTo(control1.x, control1.y, control2.x, control2.y, fin.x, fin.y);
    context.stroke();

    // Dibujar la flecha al final
    let dx = fin.x - control2.x;
    let dy = fin.y - control2.y;
    let angle = Math.atan2(dy, dx);

    context.moveTo(fin.x, fin.y);
    context.lineTo(fin.x - headLength * Math.cos(angle - Math.PI / 6), fin.y - headLength * Math.sin(angle - Math.PI / 6));
    context.moveTo(fin.x, fin.y);
    context.lineTo(fin.x - headLength * Math.cos(angle + Math.PI / 6), fin.y - headLength * Math.sin(angle + Math.PI / 6));
    context.stroke();
}
let j = 0;
function crearConexion(inicio, fin, caracter) {
    let inicioPerimetro = obtenerPuntoEnPerimetro(inicio, fin);
    let finPerimetro = obtenerPuntoEnPerimetro(fin, inicio);

    let inicioEnUso = false;
    let finEnUso = false;
    let children = layer.getChildren();
    if(inicio.x === fin.x && inicio.y === fin.y){
        inicioEnUso = true;
        finEnUso = true;
    }
    for (let i = 0; i < children.length; i++) {

        let node = children[i];

        if (node.getClassName() === 'Line') {
            let puntos = node.points();

            // Verificar si los puntos de inicio o fin coinciden con las coordenadas del estado
            if ((puntos[0] === inicio.x && puntos[1] === inicio.y) || (puntos[2] === inicio.x && puntos[3] === inicio.y)) {
                inicioEnUso = true;
            }
            if ((puntos[0] === fin.x && puntos[1] === fin.y) || (puntos[2] === fin.x && puntos[3] === fin.y)) {
                finEnUso = true;
            }
            
        }


    }



    if (inicioEnUso && finEnUso) {
        k+=1
        let control1X = 0;
        let control1Y = 0;
        let control2X = 0;
        let control2Y = 0;
        if(k%2 !== 0 ){
            control1X = inicio.x - 50;
         control1Y = inicio.y - 60; // Ajusta la altura de la curva
         control2X = fin.x + 50;
         control2Y = fin.y - 70; // Ajusta la altura de la curva

        }else{
            control1X = inicio.x + 50;
         control1Y = inicio.y + 60; // Ajusta la altura de la curva
         control2X = fin.x - 50;
         control2Y = fin.y + 70; // Ajusta la altura de la curva

        }
         
        let curva = new Konva.Line({
            id: `${contadorCurvas}`, // Asignar un ID único con contador
            points: [inicio.x, inicio.y, fin.x, fin.y],
            stroke: 'black',
            tension: 0.5,
            draggable: true, // Asegura que la línea sea draggable
            hitStrokeWidth: 10, // Asegura que la línea sea más sensible al clic
            sceneFunc: function(context) {
                context.beginPath();
                context.strokeStyle = 'black';
                dibujarParabolaConFlecha(
                    context,
                    { x: finPerimetro.x, y: finPerimetro.y },   // Punto de inicio
                    { x: control1X, y: control1Y },   // Primer punto de control
                    { x: control2X, y: control2Y },   // Segundo punto de control
                    { x: inicioPerimetro.x, y: inicioPerimetro.y }    // Punto final
                );
               
                context.lineWidth = 4;
                context.stroke();
                context.closePath();
            }
        });
        let pathData = `M${inicio.x},${inicio.y} C${control1X},${control1Y} ${control2X},${control2Y} ${fin.x},${fin.y} L${fin.x},${fin.y + 10} C${control2X},${control2Y + 10} ${control1X},${control1Y + 10} ${inicio.x},${inicio.y + 10} Z`;

let invisiblePath = new Konva.Path({
    id: `${contadorPaths}`, // Asignar un ID único con contador
    data: pathData,
    fill: 'transparent',
    stroke: 'transparent',
    strokeWidth: 0, // No es necesario un trazo
    draggable: false
});
        let puntoMedioX = (control1X + control2X) / 2;
let puntoMedioY = (control1Y + control2Y) / 2;

contadorCurvas++;
contadorPaths++;
if(caracter === ""){
    caracter = "λ";
}
let texto = new Konva.Text({
    x: puntoMedioX,
    y: puntoMedioY,
    text: caracter,
    fontSize: 25,
    fill: 'red', 
    draggable: false,
    align: 'center'
});
invisiblePath.on('click', function() {
    if (checkboxActivo === 'checkEliminarConexion') {
        let clickPosition = stage.getPointerPosition();
        let clickTarget = stage.getIntersection(clickPosition);
        if (clickTarget && clickTarget.getClassName() === 'Path') {
            eliminarConexion(clickTarget);
        }
    }
});
  
texto.offsetX(texto.width() / 2); // Centra el texto horizontalmente

        layer.add(curva);
        layer.add(texto);
        layer.add(invisiblePath);
        layer.draw();

        inicioEnUso = false;
        finEnUso = false;
        curva.datos = {
            inicio: { x: inicio.x, y: inicio.y },
            fin: { x: fin.x, y: fin.y },
            caracter: caracter,
        };
    } else {
    let linea = new Konva.Line({
        id: `${contadorCurvas}`, // Asignar un ID único con contador
        points: [inicio.x, inicio.y, fin.x, fin.y],
        draggable: true, // Asegura que la línea sea draggable
        tension: 0.5,
        hitStrokeWidth: 10, // Esto hace que la línea sea más sensible al clic
        stroke: 'transparent',
        sceneFunc: function(context) {
            context.beginPath();
            dibujarFlecha(context, {x: finPerimetro.x, y: finPerimetro.y}, {x: inicioPerimetro.x, y: inicioPerimetro.y});
            context.strokeStyle = 'black';
            context.lineWidth = 4;
            context.stroke();
            context.closePath();
        }
        
    });
    contadorCurvas++;
    contadorPaths++;
    let invisibleRect = new Konva.Rect({
        x: inicio.x,
        y: inicio.y,
        width: fin.x - inicio.x,
        height: fin.y - inicio.y,
        opacity: 0, // Hace que el rectángulo sea completamente transparente
        draggable: false
    });

    if(caracter === ""){
        caracter = "λ";
    }
    let texto = new Konva.Text({
        x: (inicio.x + fin.x) / 2,
        y: (inicio.y + fin.y) / 2,
        text: caracter,
        fontSize: 25,
        fill: 'red',
        draggable: false,
    });
    invisibleRect.on('click', function() {
      
        if (checkboxActivo === 'checkEliminarConexion') {
            let clickPosition = stage.getPointerPosition();
            let clickTarget = stage.getIntersection(clickPosition);
            if (clickTarget && clickTarget.getClassName() === 'Rect') {
                eliminarConexion(clickTarget);
            }
        }
    });
      

    layer.add(linea);
    layer.add(texto);
    layer.add(invisibleRect);
  
    layer.draw();

  
    linea.datos = {
        inicio: { x: inicio.x, y: inicio.y },
        fin: { x: fin.x, y: fin.y },
        caracter: caracter,
    };
    }
    

}



function cambiarCheckboxActivo(id) {
    let checkbox = document.getElementById(id);

    if (checkbox.checked) {
        // Si el checkbox está siendo activado
        checkboxActivo = id;

        // Desactivar los otros checkboxes
        let checkboxes = ['checkAgregarEstado', 'checkAgregarConexion', 'checkEliminarEstado', 'checkEliminarConexion'];
        checkboxes.forEach(cb => {
            if (cb !== id) {
                document.getElementById(cb).checked = false;
            }
        });
    } else {
        // Si el checkbox está siendo desactivado
        checkboxActivo = null;
    }
}

function obtenerPuntoEnPerimetro(punto, centroEstado) {
    // Calcula el ángulo y la distancia entre el centro y el punto
    let dx = punto.x - centroEstado.x;
    let dy = punto.y - centroEstado.y;
    let distancia = Math.sqrt(dx * dx + dy * dy);
    let angulo = Math.atan2(dy, dx);

    // Calcula el punto en el perímetro del estado
    let radioEstado = 25; // Ajusta el radio del estado según tu diseño
    let xPerimetro = centroEstado.x + radioEstado * Math.cos(angulo);
    let yPerimetro = centroEstado.y + radioEstado * Math.sin(angulo);

    return { x: xPerimetro, y: yPerimetro };
}
stage.on('click', function(e) {
    if (checkboxActivo === 'checkAgregarEstado') {
        crearEstado(e.evt.layerX, e.evt.layerY);
    } else if (checkboxActivo === 'checkEliminarEstado') {
        objetos.forEach(objeto => {
            let estado = objeto.find('Circle')[0];
            if (estado === e.target) {
                eliminarEstadoYConexiones(objeto);
            }
        });}
});
let eliminar = false;

document.getElementById('checkAgregarEstado').addEventListener('change', function() {
    cambiarCheckboxActivo('checkAgregarEstado');
});

document.getElementById('checkAgregarConexion').addEventListener('change', function() {
    cambiarCheckboxActivo('checkAgregarConexion');
});

document.getElementById('checkEliminarEstado').addEventListener('change', function() {
    cambiarCheckboxActivo('checkEliminarEstado');
});

document.getElementById('checkEliminarConexion').addEventListener('change', function() {
    cambiarCheckboxActivo('checkEliminarConexion');
});
function obtenerEstadoYConexiones() {
    let estados = [];
    let conexiones = [];

    objetos.forEach(objeto => {
        let estado = objeto.find('Circle')[0];
        let texto = objeto.find('Text')[0];
        let coorde = estado.getAbsolutePosition();
        estados.push({
            nombre: texto.text(),
            x: coorde.x,
            y: coorde.y
        });
    });

    let children = layer.getChildren();
   
    for (let i = 0; i < children.length; i++) {
        let node = children[i];
        if (node.getClassName() === 'Line') {
            let puntos = node.points();
          
            let caracter = node.datos.caracter;

            conexiones.push({
                inicio: { x: puntos[0], y: puntos[1] },
                fin: { x: puntos[2], y: puntos[3] },
                caracter: caracter
            });
        }
    };

    return {
        estados: estados,
        conexiones: conexiones
    };
}


function eliminarEstadoYConexiones(estado) {
    let numeroEstado = estado.datos.numeroEstado;
    liberarNumeroEstado(numeroEstado);
    let indiceEstado = objetos.indexOf(estado);
    let coorde = estado.getAbsolutePosition();
    if (indiceEstado !== -1) {
        // Almacenar las coordenadas del estado
        let estadoX = coorde.x;
        let estadoY = coorde.y;
        let numeroEstado = estado.text;
        liberarNumeroEstado(numeroEstado);
    
        // Filtrar y eliminar las conexiones relacionadas
        let children = layer.getChildren();

        for (let i = children.length - 1; i >= 0; i--) {
            let node = children[i];

            if (node.getClassName() === 'Line') {
                let puntos = node.points();

                // Verificar si los puntos de inicio o fin coinciden con las coordenadas del estado
                if (puntos[2] === estadoX && puntos[3] === estadoY || puntos[0] === estadoX && puntos[1] === estadoY) {
                    // Eliminar texto asociado a la conexión
                    let texto2 = node.datos.caracter;
                    let texto = layer.find(node => node.getClassName() === 'Text' && node.x() === (puntos[0] + puntos[2]) / 2 && node.y() === (puntos[1] + puntos[3]) / 2);
                    if (texto) {
                        texto.forEach(textoNode => {
                            if (texto2 == textoNode.text()) {
                                textoNode.destroy();
                            }
                        });
                    }

                    // Eliminar conexión
                    node.destroy();
                }
            }
        }
        // Eliminar el estado del arreglo 'objetos' y de la capa
        objetos.splice(indiceEstado, 1);
        estado.destroy();
        layer.batchDraw();
    }
}


function eliminarConexion(objeto) {
    let resultado = objeto;

    if (resultado.getClassName() === 'Rect') {
        let x = resultado.x();
        let y = resultado.y();

        // Filtrar y eliminar la conexión relacionada
        let children = layer.getChildren();
        for (let i = children.length - 1; i >= 0; i--) {
            let node = children[i];

            if (node.getClassName() === 'Line') {
                let puntos = node.points();

                // Verificar si los puntos de inicio o fin coinciden con las coordenadas del rectángulo
                if (puntos[0] === x && puntos[1] === y) {
                    // Eliminar texto asociado a la conexión
                    let texto2 = node.datos.caracter;
                    let texto = layer.find(node => node.getClassName() === 'Text' && node.x() === (puntos[0] + puntos[2]) / 2 && node.y() === (puntos[1] + puntos[3]) / 2);
                    if (texto) {
                        texto.forEach(textoNode => {
                            if (texto2 == textoNode.text()) {
                                textoNode.destroy();
                            }
                        });
                    }

                    // Eliminar conexión
                    node.destroy();
                    // Si tienes una lista de conexiones, también deberías eliminarla de esa lista aquí
                }
            }
        }

        // Finalmente, eliminar el objeto seleccionado
        resultado.destroy();
    } else if (resultado.getClassName() === 'Path') {
        let idObjeto = resultado.id(); // Obtener el ID del objeto
    
        // Filtrar y eliminar la conexión relacionada
        let children = layer.getChildren();
        for (let i = children.length - 1; i >= 0; i--) {
            let node = children[i];
    
            if (node.getClassName() === 'Line') {
                let idLinea = node.id(); // Obtener el ID de la línea
               
                let puntos = node.points();
    
                // Verificar si los puntos de inicio o fin coinciden con las coordenadas del path
                if (idLinea === idObjeto) {
                    // Eliminar texto asociado a la conexión
                    let texto2 = node.datos.caracter;
            
                    let textNodes = layer.find(node => node.getClassName() === 'Text' );
                    if (textNodes) {
                        textNodes.forEach(textoNode => {
                            
                            if (texto2 == textoNode.text()) {
                                textoNode.destroy();
                            }
                        });
                    }
                
                    // Eliminar conexión
                    node.destroy();
                    // Si tienes una lista de conexiones, también deberías eliminarla de esa lista aquí
                }
    
        // Finalmente, eliminar el objeto seleccionado
        resultado.destroy();
    }}}
    

    layer.batchDraw();
}






function mostrarDatosEnVentanaEmergente(datos) {
    let ventanaEmergente = window.open('', '_blank', 'width=600,height=400');
    ventanaEmergente.document.write('<pre>' + JSON.stringify(datos, null, 2) + '</pre>');
}

stage.on('dragstart', function() {
    inicioConexion = null;
});
