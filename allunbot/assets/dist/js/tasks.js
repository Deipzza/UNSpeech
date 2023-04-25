var new_task = 0;

function add_task(tab, task = null) {
  if (task == null) var content_task = template_task();
  else var content_task = template_task_by_information(task);

  $(`#${tab}`).append(content_task);
}

function remove_task(tab, task = null) {}

function template_task_by_information(task) {
  var tem_button = [
    '<div class="colapse_button col-1">',
    `<a class="collapse_table" type="button" data-bs-toggle="collapse" data-bs-target="#colapse_${task["_id"]}" aria-expanded="false" aria-controls="collapseWidthExample">`,
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-right" viewBox="0 0 16 16">',
    '<path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>',
    "</svg>",
    "</a>",
    "</div>",
  ];

  var tem_content = [
    '<div class="name_task col-5">',
    `<span class="label-text">${task["name"]}</span>`,
    "</div>",
    `<div class="subject_task col-5">${task["subject"]}</div>`,
    //`<span class="tag approved">Approved</span>`,
    `<input class="task-item task_check col-1" name="task" type="checkbox" id="item-1"/>`,
  ];

  var tem_collapse = [
    '<div class="description_task">',
    `<div class="collapse" id="colapse_${task["_id"]}">`,
    `<div class="content_body_collapse">${task["description"]}</div>`,
    "</div>",
    "</div>",
  ];

  var content_task =
    '<div class="task">' +
    tem_button.join("") +
    tem_content.join("") +
    "</div>";
  content_task += tem_collapse.join("");
  return content_task;
}

function template_task() {
  var tem_button = [
    '<div class="colapse_button col-1">',
    `<a class="collapse_table" type="button" data-bs-toggle="collapse" data-bs-target="#colapse_${new_task}" aria-expanded="true" aria-controls="collapseWidthExample">`,
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-right" viewBox="0 0 16 16">',
    '<path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>',
    "</svg>",
    "</a>",
    "</div>",
  ];

  var tem_content = [
    '<div class="name_task col-6">',
    '<input type="text" class="form-control">',
    "</div>",
    '<div class="subject_task col-4">',
    '<input type="text" class="form-control">',
    "</div>",
    //`<span class="tag approved">Approved</span>`,
    `<input class="task-item task_check col-1" name="task" type="checkbox" id="item-1" value="${new_task}" checked/>`,
  ];

  var tem_collapse = [
    `<div class="description_task" id="collapse_${new_task}">`,
    `<div class="collapse show" id="colapse_${new_task}">`,
    `<div class="content_body_collapse">
              <textarea class="form-control description_task"></textarea>
              </div>`,
    "</div>",
    "</div>",
  ];

  var content_task =
    `<div class="task" id=${new_task}>` +
    tem_button.join("") +
    tem_content.join("") +
    "</div>";
  content_task += tem_collapse.join("");
  new_task += 1;

  return content_task;
}

function template_task_edit_by_information(task_id) {
    var task_name = $(`#${task_id}`).find(".name_task span").text();
    var task_subject = $(`#${task_id}`).find(".subject_task").text();
    var task_description = $(`#${task_id}`).find(
    ".description_task textarea .content_body_collapse"
    ).text;
    var task_date = $(`#${task_id}`).find(".task_date").text();
    var task_notification_time = $(`#${task_id}`)
    .find(".task_notification_time")
    .text();

  var tem_button = [
    '<div class="colapse_button col-1">',
    `<a class="collapse_table" type="button" data-bs-toggle="collapse" data-bs-target="#colapse_${task_id}" aria-expanded="true" aria-controls="collapseWidthExample">`,
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-right" viewBox="0 0 16 16">',
    '<path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>',
    "</svg>",
    "</a>",
    "</div>",
  ];

  var tem_content = [
    '<div class="name_task col-5">',
    `<input type="text" class="form-control" value=${task_name}>`,
    "</div>",
    '<div class="subject_task col-5">',
    `<input type="text" class="form-control" value=${task_subject}>`,
    "</div>",
    //`<span class="tag approved">Approved</span>`,
    `<input class="task-item task_check col-1" name="task" type="checkbox" id="item-1" value="${task_id}" checked/>`,
  ];

  var tem_collapse = [
    `<div class="description_task" id="collapse_${task_id}">`,
    `<div class="collapse show" id="colapse_${task_id}">`,
    `<div class="content_body_collapse">
        <textarea class="form-control description_task">${task_description}</textarea>
    </div>`,
    "</div>",
    "</div>",
  ];

  var content_task =
    tem_button.join("") +
    tem_content.join("");

  return [content_task, tem_collapse.join("")];
}

function save_task() {
  $(".task_check").each(async function (check) {
    if ($(this).prop("checked") == true) {
      var task_id = $(this).val();
      var task_name = $(`#${task_id}`).find(".name_task input").val();
      var task_subject = $(`#${task_id}`).find(".subject_task input").val();
      var task_description = $(`#${task_id}`).find(
        ".description_task textarea"
      ).value;
      var task_date = $(`#${task_id}`).find(".task_date").text();
      var task_notification_time = $(`#${task_id}`)
        .find(".task_notification_time")
        .text();

      var formData = new FormData();
      formData.append("name", task_name);
      formData.append("subject", task_subject);
      formData.append("description", task_description);
      formData.append("date", task_date);
      formData.append("notification_time", task_notification_time);
      await request_save_task(formData, task_id);
    }
  });
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
      $(`#${id}`).remove();
      $(`#collapse_${id}`).remove();
      add_task("task_1", response);
    }
  });
}

function edit_task(task) {
    $(`#${task} .task_check`).each(async function (check) {
      if ($(this).prop("checked") == true) {
        var task_id = $(this).val();
        var content_task = template_task_edit_by_information(task_id)
        console.log(task_id);
        $(`#${task_id}`).html(content_task[0]);
        $(`#collapse_${task_id}`).html(content_task[1]);
      }
    });
    
}