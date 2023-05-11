// Control of submit new event
$("#event").on("submit", async function (e) {
  var formData = new FormData(document.querySelector("form#event"));

  await $.ajax({
    url: "../api/event",
    data: formData,
    type: "POST",
    processData: false,
    contentType: false,
    dataType: "json",
  }).done(function (response) {
    console.log(response);
    if (response) {
      Swal.fire({
        icon: "success",
        title: "Se ha creado el evento",
        showConfirmButton: false,
        timer: 1500,
      });
      location.reload();
    }
  });
});


// main functions

async function save_event(event_id) {
  /********************************
   * Get information and saves of event to save.
   * 
   * Inputs:
   * event_id -> string with the identifier of the event to be update/create.
  ********************************/
 
  var event_save = $(`#${event_id}`);
  var event_name = event_save.find(".event_name input").val();
  var event_status = event_save.find(".event_status select").val();
  var event_url = event_save.find(".event_url input").val();
  var event_dependency = event_save.find(".event_dependency input").val();
  var event_date = event_save.find(".event_date input").val();
  var event_start_time = event_save.find(".event_start-time input").val();
  var event_final_time = event_save.find(".event_final-time input").val();
  var event_description = event_save.find(".event_description textarea").val();

  var formData = new FormData();

  formData.append("id", event_id);
  formData.append("name", event_name);
  formData.append("status", event_status);
  formData.append("url", event_url);
  formData.append("dependency", event_dependency);
  formData.append("date", event_date);
  formData.append("start-time", event_start_time);
  formData.append("final-time", event_final_time);
  formData.append("description", event_description);

  await request_save_event(formData, event_id);
}

async function remove_event(event_id) {
  /********************************
   * Delete event.
   * 
   * Inputs:
   * event_id -> string with the identifier of the event to be delete.
  ********************************/

  var formData = new FormData();
  formData.append("id", event_id);
  await request_remove_event(formData, event_id);
}

function edit_event(event_id) {
  /********************************
   * Generetad component DOM for to edit event.
   * 
   * Inputs:
   * event_id -> string with the identifier of the event to be edit.
  ********************************/
  var content_event = template_event_edit(event_id);

  $(`#${event_id}`).html(content_event);
}

// Utils fuctions
async function request_save_event(formData) {
  /********************************
   * Request to save event to database.
   * 
   * Inputs:
   * formData -> information to save.
  ********************************/
  await $.ajax({
    url: "../api/event",
    data: formData,
    type: "PUT",
    processData: false,
    contentType: false,
    dataType: "json",
  }).done(function (response) {
    console.log(response);
    if (response) {
      Swal.fire({
        icon: "success",
        title: "El evento ha sido actualizado.",
        showConfirmButton: false,
        timer: 1500,
      });
      location.reload();
    }
  });
}

async function request_remove_event(formData) {
  /********************************
   * Delete event to database.
   * 
   * Inputs:
   * formData -> Information to delete.
  ********************************/
  await $.ajax({
    url: "../api/event",
    data: formData,
    type: "DELETE",
    processData: false,
    contentType: false,
    dataType: "json",
  }).done(function (response) {
    console.log(response);
    if (response) {
      Swal.fire({
        icon: "success",
        title: "El evento ha sido borrado.",
        showConfirmButton: false,
        timer: 1500,
      });
      location.reload();
    }
  });
}

function template_event_edit(event_id) {
  /********************************
   * Generated template for edit event.
   * 
   * Inputs:
   * event_id -> string with the identifier of the event to edit.
  ********************************/

  var event_edit = $(`#${event_id}`);
  var event_name = event_edit.find(".event_name").text();
  var event_status = event_edit.find(".event_status").text();
  var event_url = event_edit.find(".event_url div").text();
  var event_dependency = event_edit.find(".event_dependency").text();
  var event_date = event_edit.find(".event_date").text();
  var event_start_time = event_edit.find(".event_start-time").text();
  var event_final_time = event_edit.find(".event_final-time").text();
  var event_description = event_edit.find(".event_description").text();

  var tem_content = `
      <td class="event_name" style="width: 200px;">
        <input type="text" class="form-control" value='${event_name}' placeholder = 'Evento'>
      </td>
      <td class="event_status" style="width: 200px;">
        <select class="form-select" id="status" name="status" >
          <option value="activo" ${
            event_status == "activo" ? "selected" : ""
          }>Activo</option>
          <option value="cancelado" ${
            event_status == "cancelado" ? "selected" : ""
          }>Cancelado</option>
          <option value="pospuesto" ${
            event_status == "pospuesto" ? "selected" : ""
          }>Pospuesto</option>
        </select>
      </td>
      <td class="event_url" style="width: 200px;">
        <input type="text" class="form-control" value='${event_url}' placeholder = 'Estado'>
      </td>
      <td class="event_dependency" style="width: 200px;">
        <input type="text" class="form-control" value='${event_dependency}' placeholder = 'Dependencia'>
      </td>
      <td class="event_date" style="width: 100px;">
        <input type="date" class="form-control" value='${event_date}' placeholder = 'Fecha'>
      </td>
      <td class="event_start-time" style="width: 100px;">
        <input type="time" class="form-control" value='${event_start_time}' placeholder = 'Asignatura'>
      </td>
      <td class="event_final-time" style="width: 100px;">
        <input type="time" class="form-control" value='${event_final_time}' placeholder = 'Asignatura'>
      </td>
      <td class="event_description" style="width: 300px;">
        <textarea class="form-control" placeholder = 'Descripción'>${event_description}</textarea>
      </td>`;

  $(`#${event_id}`).find(".accion .btn-warning").addClass("disabled");
  var tem_accion = $(`#${event_id}`).find(".accion").html();

  var content_event =
    tem_content + "<td class='accion'>" + tem_accion + "</td>";

  return content_event;
}