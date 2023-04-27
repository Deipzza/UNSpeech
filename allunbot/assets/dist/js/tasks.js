var new_task = 0;

var tem_accion = [
  '<td class="accion fix_column" style="width: 100px;">',
  '<div class="Acciones">',
  `<button class="btn btn-primary blue" onclick="save_task('${new_task}')">`,
  '<svg width="16px" height="16px" viewBox="0 0 24 24" fill="none" stroke="currentColor" xmlns="http://www.w3.org/2000/svg" ><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" stroke="#CCCCCC" stroke-width="0.192"></g><g id="SVGRepo_iconCarrier"> <g id="System / Save"> <path id="Vector" d="M17 21.0002L7 21M17 21.0002L17.8031 21C18.921 21 19.48 21 19.9074 20.7822C20.2837 20.5905 20.5905 20.2843 20.7822 19.908C21 19.4806 21 18.921 21 17.8031V9.21955C21 8.77072 21 8.54521 20.9521 8.33105C20.9095 8.14 20.8393 7.95652 20.7432 7.78595C20.6366 7.59674 20.487 7.43055 20.1929 7.10378L17.4377 4.04241C17.0969 3.66374 16.9242 3.47181 16.7168 3.33398C16.5303 3.21 16.3242 3.11858 16.1073 3.06287C15.8625 3 15.5998 3 15.075 3H6.2002C5.08009 3 4.51962 3 4.0918 3.21799C3.71547 3.40973 3.40973 3.71547 3.21799 4.0918C3 4.51962 3 5.08009 3 6.2002V17.8002C3 18.9203 3 19.4796 3.21799 19.9074C3.40973 20.2837 3.71547 20.5905 4.0918 20.7822C4.5192 21 5.07899 21 6.19691 21H7M17 21.0002V17.1969C17 16.079 17 15.5192 16.7822 15.0918C16.5905 14.7155 16.2837 14.4097 15.9074 14.218C15.4796 14 14.9203 14 13.8002 14H10.2002C9.08009 14 8.51962 14 8.0918 14.218C7.71547 14.4097 7.40973 14.7155 7.21799 15.0918C7 15.5196 7 16.0801 7 17.2002V21M15 7H9" stroke="currentColor" stroke-width="1.488" stroke-linecap="round" stroke-linejoin="round"></path> </g> </g></svg>',
  "</button>",

  `<button class="btn btn-danger red" onclick="$('tr#${new_task}').remove()">`,
  '<svg width="16px" height="16px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g id="Interface / Trash_Full"> <path id="Vector" d="M14 10V17M10 10V17M6 6V17.8C6 18.9201 6 19.4798 6.21799 19.9076C6.40973 20.2839 6.71547 20.5905 7.0918 20.7822C7.5192 21 8.07899 21 9.19691 21H14.8031C15.921 21 16.48 21 16.9074 20.7822C17.2837 20.5905 17.5905 20.2839 17.7822 19.9076C18 19.4802 18 18.921 18 17.8031V6M6 6H8M6 6H4M8 6H16M8 6C8 5.06812 8 4.60241 8.15224 4.23486C8.35523 3.74481 8.74432 3.35523 9.23438 3.15224C9.60192 3 10.0681 3 11 3H13C13.9319 3 14.3978 3 14.7654 3.15224C15.2554 3.35523 15.6447 3.74481 15.8477 4.23486C15.9999 4.6024 16 5.06812 16 6M16 6H18M18 6H20" stroke="currentColor" stroke-width="1.488" stroke-linecap="round" stroke-linejoin="round"></path> </g> </g></svg>',
  "</button>",
  "</div>",
  "</td>",
];

var tem_table =[
  [
      '<table class="table table-striped" style="width: max-content;">',
        '<thead class="table-dark">',
          '<tr>',
            '<th>Tarea</th>',
            '<th>Asignatura</th>',
            '<th>Fecha y hora</th>',
            '<th>Notificación</th>',
            '<th>Descripción</th>',
            '<th class="fix_column">Acciones</th>',
          '</tr>',
        '</thead>',
        '<tbody></tbody>',
      '</table>',
    '</div>'
  ],
  [
    '<table class="table table-striped" style="width: max-content;">',
      '<thead class="table-dark">',
        '<tr>',
          '<th>Tarea</th>',
          '<th>Asignatura</th>',
          // '<th>Fecha</th>',
          // '<th>Notificación</th>',
          '<th>Descripción</th>',
          '<th class="fix_column">Acciones</th>',
        '</tr>',
      '</thead>',
      '<tbody></tbody>',
    '</table>',
  '</div>'
]
]

function add_task(tab, task = null) {
  var type_task = tab.charAt(tab.length - 1);

  if (type_task == "1")
    var content_task = template_task();
  else if (type_task != "1")
    var content_task = templae_task_date(task);

  if(!$(`#${tab} table tbody`).length){
    if(type_task != "1")
      var table = tem_table[0].join("");
    else
      var table = tem_table[1].join("");

    $(`#${tab}`).html(table);
  }

  $(`#${tab} table tbody`).append(content_task);
}


function template_task() {
  var tem_content = [
    '<td class="name_task" style="width: 200px;">',
    `<input type="text" class="form-control" value="" placeholder = 'Tarea'>`,
    "</td>",
    '<td class="subject_task" style="width: 200px;">',
    `<input type="text" class="form-control" value="" placeholder = 'Asignatura'>`,
    "</td>",
    // '<td class="date_task" style="width: 100px;">',
    // `<input type="date" class="form-control" value=${task_date}>`,
    // '</td>',
    // '<td class="task_notification_time" style="width: 100px;">',
    // `<input type="date" class="form-control" value=${task_notification_time}>`,
    // '</td>',
    '<td class="description_task" style="width: 300px;">',
    `<textarea class="form-control" placeholder = 'Descripción'></textarea>`,
    "</td>",
  ];

  var content_task =
    "<tr class='task' id='" +
    new_task +
    "'>" +
    tem_content.join("") +
    tem_accion.join("") +
    "</tr>";

  new_task += 1;

  return content_task;
}

function templae_task_date() {

  var tem_content = [
    '<td class="name_task" style="width: 200px;">',
    `<input type="text" class="form-control" value='' placeholder = 'Tarea'>`,
    "</td>",
    '<td class="subject_task" style="width: 200px;">',
    `<input type="text" class="form-control" value='' placeholder = 'Asignatura'>`,
    "</td>",
    '<td class="date_task" style="width: 100px;">',
    `<input type="date" class="form-control" value=''>`,
    `<input type="time" class="form-control" value=''>`,
    "</td>",
    '<td class="task_notification_time" style="width: 100px;">',
    `<input type="date" class="form-control" value=''>`,
    "</td>",
    '<td class="description_task" style="width: 300px;">',
    `<textarea class="form-control" placeholder = 'Descripción'></textarea>`,
    "</td>",
  ];

  var content_task =
      "<tr class='task' id='" +
      new_task +
      "'>" +
      tem_content.join("") +
      tem_accion.join("") +
      "</tr>";

  return content_task;
}

function template_task_edit_with_date(id_table, task_id) {
  var task_edit = $(`#${id_table} #${task_id}`)
  var task_name = task_edit.find(".name_task").text();
  var task_subject = task_edit.find(".subject_task").text();
  var task_description = task_edit.find(".description_task").text();
  
  var task_date_time = task_edit.find(".date_task").text().split(" ")
  console.log(task_date_time)
  var task_date = task_date_time[0];
  var task_time = task_date_time[1];

  var task_notification_time = task_edit
    .find(".task_notification_time")
    .text();

  var tem_content = [
    '<td class="name_task" style="width: 200px;">',
    `<input type="text" class="form-control" value='${task_name}' placeholder = 'Tarea'>`,
    "</td>",
    '<td class="subject_task" style="width: 200px;">',
    `<input type="text" class="form-control" value='${task_subject}' placeholder = 'Asignatura'>`,
    "</td>",
    '<td class="date_task" style="width: 100px;">',
    `<input type="date" class="form-control" value=${task_date}>`,
    `<input type="time" class="form-control" value=${task_time}>`,
    "</td>",
    '<td class="task_notification_time" style="width: 100px;">',
    `<input type="date" class="form-control" value=${task_notification_time}>`,
    "</td>",
    '<td class="description_task" style="width: 300px;">',
    `<textarea class="form-control" placeholder = 'Descripción'>${task_description}</textarea>`,
    "</td>",
  ];
  $(`#${task_id}`).find(".accion .btn-warning").addClass("disabled");
  var tem_accion = $(`#${task_id}`).find(".accion").html();
  console.log(tem_accion);

  var content_task =
    tem_content.join("") + "<td class='accion'>" + tem_accion + "</td>";

  return content_task;
}

function template_task_edit(id_table, task_id) {
  var task_edit = $(`#${id_table} #${task_id}`)

  var task_name = task_edit.find(".name_task").text();
  var task_subject = task_edit.find(".subject_task").text();
  var task_description = task_edit.find(".description_task").text();

  var tem_content = [
    '<td class="name_task" style="width: 200px;">',
    `<input type="text" class="form-control" value='${task_name}' placeholder = 'Tarea'>`,
    "</td>",
    '<td class="subject_task" style="width: 200px;">',
    `<input type="text" class="form-control" value='${task_subject}' placeholder = 'Asignatura'>`,
    "</td>",
    // '<td class="date_task" style="width: 100px;">',
    // `<input type="date" class="form-control" value=${task_date}>`,
    // "</td>",
    // '<td class="task_notification_time" style="width: 100px;">',
    // `<input type="date" class="form-control" value=${task_notification_time}>`,
    // "</td>",
    '<td class="description_task" style="width: 300px;">',
    `<textarea class="form-control" placeholder = 'Descripción'>${task_description}</textarea>`,
    "</td>",
  ];
  $(`#${task_id}`).find(".accion .btn-warning").addClass("disabled");
  var tem_accion = $(`#${task_id}`).find(".accion").html();
  console.log(tem_accion);

  var content_task =
    tem_content.join("") + "<td class='accion'>" + tem_accion + "</td>";

  return content_task;
}

async function save_task(task_id) {
  var task_name = $(`#${task_id}`).find(".name_task input").val();
  var task_subject = $(`#${task_id}`).find(".subject_task input").val();
  var task_description = $(`#${task_id}`)
    .find(".description_task textarea")
    .val();
  if($(`#${task_id}`).find(".date_task input").length == 2) {
    var task_date = $(`#${task_id}`).find(".date_task input")[0].value;
    var task_time = $(`#${task_id}`).find(".date_task input")[1].value;
    var task_date_time = task_date + " " + task_time;
  }
  else {
    var task_date_time = "";
  }

  console.log(task_time)
  var task_notification_time = $(`#${task_id}`)
    .find(".task_notification_time input")
    .val();

  var formData = new FormData();
  formData.append("id", task_id);
  formData.append("name", task_name);
  formData.append("subject", task_subject);
  formData.append("description", task_description);
  formData.append("date", task_date_time);
  formData.append("notification_time", task_notification_time);
  await request_save_task(formData, task_id);
}

async function remove_task(task_id) {
  var formData = new FormData();
  formData.append("id", task_id);
  await request_remove_task(formData, task_id);
}

async function request_save_task(formData, id) {
  await $.ajax({
    url: "../api/task",
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
        title: "La tarea ha sido guardada.",
        showConfirmButton: false,
        timer: 1500,
      });
      location.reload();
    }
  });
}
async function request_remove_task(formData, id) {
  await $.ajax({
    url: "../api/task",
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
        title: "La tarea ha sido borrada.",
        showConfirmButton: false,
        timer: 1500,
      });
      location.reload();
    }
  });
}

function edit_task(table, task_id) {
  var type_task = table.charAt(table.length - 1);
  if(type_task != "1")
    var content_task = template_task_edit_with_date(table, task_id);
  else
    var content_task = template_task_edit(table, task_id);


  $(`#${table} #${task_id}`).html(content_task);
}
