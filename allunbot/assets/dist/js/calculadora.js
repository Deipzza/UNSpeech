function add_subject(id) {
  var tr = ""
  var template = '<td><input type="text" class="form-control" aria-describedby="emailHelp" value=""></td>'

  for (let index = 0; index < 3; index++) {
    tr += template
  }

  $("table#" + id + " tbody").append(`<tr>${tr}</tr>`);
}

var calificaciones = "";

$(document).ready(
  async function name(params) {
    await get_subjects();
    calcular_metricas();
  }
)

async function save_values(id) {
  var subject_item = calificaciones[id];
  var nota = 0;
  var porcentaje = 0;
  var error = { "status": false, "title": "", "text": "" }

  $("#" + id + " tbody tr").each(function (element) {
    parcial = 1;
    $(this).find("input").each(function (i_cell) {
      item = $(this).val();
      if (!isNaN(item)) {
        value = parseFloat(item);
        if (i_cell == 0) {

          if (value > 100) {
            error = { "status": true, "title": "Valores fuera de rango", "text": "Ha puesto un porcentaje por encima del 100%, por favor corrigalo e intente nuevamente." }
            return false;
          }

          porcentaje += value;
          value /= 100;
        } else {
          if (value > 5) {
            error = { "status": true, "title": "Valores fuera de rango", "text": "Ha puesto un nota por encima de 5, por favor corrigala e intente nuevamente." }
            return false;
          }
        }

        if (value < 0) {
          error = { "status": true, "title": "Valores negativos", "text": "Hemos encontrado que ha ingresado valores negativos, por favor corrigalo e intente nuevamente." }
          return false;
        }

        parcial *= parseFloat(value);
      }
    });
    nota += parcial;
  });

  if (porcentaje != 100) {
    Swal.fire({
      icon: 'error',
      title: 'Porcentajes incorrectos',
      text: `La suma de los porcentajes ingresados debe ser igual a 100%, por favor corregirlos.`
    })
    reset_values(id);
  } else if (error["status"]) {
    Swal.fire({
      icon: 'error',
      title: error["title"],
      text: error["text"]
    })
  } else {
    subject_item["data_table"][3] = nota.toFixed(2);
    $(`#row_${id} td`)[3].innerHTML = nota.toFixed(2);

    $(`.modal#${id}`).modal('hide');
    Swal.fire({
      icon: 'success',
      title: 'Los datos han sido guardados',
      showConfirmButton: false,
      timer: 1500
    })
  }
}

async function calcular_metricas() {
  initial_metrics = calificaciones["initial_metrics"]
  var plan_estudios = initial_metrics["plan_estudios"];
  plan_estudios = plan_estudios.charAt(0).toUpperCase() + plan_estudios.slice(1).toLowerCase();
  var username = initial_metrics["username"];
  $("#plan_estudios").text(`${plan_estudios} ~ ${username}`);

  var creditos = initial_metrics["creditos"];
  var ponderado = initial_metrics["ponderado"];
  var suma = initial_metrics["suma"];
  var size = initial_metrics["size"];

  Object.keys(calificaciones).forEach(key => {
    if (key != "initial_metrics") {

      var row = calificaciones[key]["data_table"];
      var credito = parseInt(row[1]);
      var nota = row[3];
      console.log(row, credito, nota);

      if (!isNaN(nota)) {
        nota = parseFloat(nota);
        ponderado += nota * credito;
        creditos += credito;
        suma += nota;
        size++;
      }
    }

  });

  var papa = (ponderado / creditos).toFixed(2);
  var promedio = (suma / size).toFixed(2);
  $("#metric_papa").text(papa);
  $("#metric_promedio").text(promedio);
}

async function get_subjects() {
  const formData = new FormData();
  formData.append("token", token);
  await $.ajax({
    url: "../calculadora",
    data: formData,
    type: "POST",
    processData: false,
    contentType: false,
    dataType: "json"
  }).done(function (response) {
    calificaciones = response;
    localStorage.setItem("subjects", JSON.stringify(calificaciones))
  });
  calificaciones = JSON.parse(localStorage.getItem('subjects'));
}

function reset_values(id) {
  initial_values = calificaciones[id]["grades"];
  
  $("table#"+id+" tbody").html("");

  initial_values.forEach(element => {
      var template = [
          '<td>',
          `<p>${element[0]}</p>`,
          '</td>',
          '<td>',
          `<input type="text" class="form-control" aria-describedby="emailHelp" value="${element[1]}">`,
          '</td>',
          '<td>',
          `<input type="text" class="form-control" aria-describedby="emailHelp" value="${element[2]}">`,
          '</td>',
      ].join('')
  
      $("table#"+id+" tbody").append(`<tr>${template}</tr>`);

  });
}