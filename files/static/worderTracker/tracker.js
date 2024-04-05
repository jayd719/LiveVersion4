updateDate();
notesColor();
updateAllCompleted();

// Delete Nav var Not Used
function deleteNavBar() {
  document.body.removeChild(document.getElementById("nav-bar"));
}

/*
-------------------------------------------------------
Checks the value of a note and assigns a corresponding 
color class to the element.
Use: checkNote(elm)
-------------------------------------------------------
Parameters:
    elm - the HTML element representing the note (HTMLElement)
Returns:
    None
-------------------------------------------------------
*/
function checkNote(elm) {
  if (elm.value == "HOLD FOR CUSTOMER") {
    elm.className = "bg-danger hold-for-customer";
  } else if (elm.value == "WAITING FOR MATERIAL") {
    elm.className = "waiting-for-material";
  } else if (elm.value == "CUSTOMER WITNESS") {
    elm.className = "customer-witness";
  } else if (elm.value == "OUTSOURCED") {
    elm.className = "alert-secondary";
  } else if (elm.value == "HOLD FOR TA") {
    elm.className = "hold-for-ta";
  } else {
    elm.className = "blank";
  }
}

/*
-------------------------------------------------------
Checks the notes for each work order and assigns a 
corresponding color class.
Use: notesColor()
-------------------------------------------------------
Parameters:
    None
Returns:
    None
-------------------------------------------------------
*/
function notesColor() {
  let notes = document.querySelectorAll(".notes");
  for (i = 0; i < notes.length; i++) {
    if (notes[i].value.toLowerCase() == "none" || notes[i].value.length < 2) {
      notes[i].value = "";
      notes[i].className = "blank";
    } else {
      checkNote(notes[i]);
    }
  }
}

/*
-------------------------------------------------------
Updates the due dates and colors for each due date in
the table based on the current date.
Use: updateDate()
-------------------------------------------------------
Parameters:
    None
Returns:
    None
-------------------------------------------------------
*/
function updateDate() {
  let dueDates = document.querySelectorAll(".dueDate");
  let dates = document.querySelectorAll("#due-in");
  for (i = 0; i < dates.length; i++) {
    const targetDate = new Date(dueDates[i].value);
    const currentDate = new Date();
    const dueIn = Math.ceil((targetDate - currentDate) / (1000 * 60 * 60 * 24));
    dates[i].innerHTML = dueIn;
    if (dueIn < 0) {
      dates[i].className = "bg-danger";
      dates[i].style.color = "white";
    } else if (dueIn >= 0 && dueIn <= 7) {
      dates[i].className = "bg-warning";
    } else {
      dates[i].className = "bg-success";
    }
  }
}

/*
-------------------------------------------------------
Writes data back to the server using AJAX.
Use: POST(data)
-------------------------------------------------------
Parameters:
    data - the data to be sent to the server (Object)
Returns:
    None
-------------------------------------------------------
*/
function POST(data) {
  var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
  let jsonData = JSON.stringify(data);
  $.ajax({
    type: "POST",
    url: "/update_data/", // Replace with your server endpoint
    data: jsonData,
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    headers: {
      "X-CSRFToken": csrfToken, // Include the CSRF token in the request headers
    },
    success: function (response) {
      console.log("Data sent successfully:", response);
    },
    error: function (error) {
      alert("COULD NOT SAVE DATA");
    },
  });
}

/*
-------------------------------------------------------
Updates the notes for a particular work order.
Use: updateNotes(elmID, wo)
-------------------------------------------------------
Parameters:
    elmID - the ID of the HTML element containing the notes (string)
    wo - the work order number (string)
Returns:
    None
-------------------------------------------------------
*/
function updateNotes(elmID, wo) {
  let dataValues = {};
  dataValues["workOrder"] = wo;
  dataValues["field"] = "notes";
  dataValues["data"] = document.getElementById(elmID).value;
  POST(dataValues);
  checkNote(document.getElementById(elmID));
}

/*
-------------------------------------------------------
Updates the shipping status for a particular work order.
Use: updateShippingThisMonth(wo, value)
-------------------------------------------------------
Parameters:
    wo - the work order number (string)
    value - the shipping status (boolean)
Returns:
    None
-------------------------------------------------------
*/
function updateShippingThisMonth(wo, value) {
  let dataValues = {};
  dataValues["workOrder"] = wo;
  dataValues["field"] = "stm";
  dataValues["data"] = value;
  POST(dataValues);
}

/*
-------------------------------------------------------
Writes the updated due date for a particular work order.
Use: writeDate(wo, elmID)
-------------------------------------------------------
Parameters:
    wo - the work order number (string)
    elmID - the ID of the HTML element containing the due date (string)
Returns:
    None
-------------------------------------------------------
*/
function writeDate(wo, elmID) {
  let dataValues = {};
  dataValues["workOrder"] = wo;
  dataValues["field"] = "dueDate";
  dataValues["data"] = document.getElementById(elmID).value;
  POST(dataValues);
  updateDate();
}

/*
-------------------------------------------------------
Updates the Manufacturing Engineer (ME) for a particular 
work order.
Use: updateME(elmID, wo)
-------------------------------------------------------
Parameters:
    elmID - the ID of the HTML element containing the ME (string)
    wo - the work order number (string)
Returns:
    None
-------------------------------------------------------
*/
function updateME(elmID, wo) {
  let dataValues = {};
  dataValues["workOrder"] = wo;
  dataValues["field"] = "ME";
  dataValues["data"] = document.getElementById(elmID).value;
  POST(dataValues);
}

/*
-------------------------------------------------------
Toggles the incoming inspection status for a work order.
Use: updateIncomingInspection(wo)
-------------------------------------------------------
Parameters:
    wo - the work order number (string)
Returns:
    None
-------------------------------------------------------
*/
function updateIncomingInspection(wo) {
  let info = document.getElementById(`${wo}-inc`);
  let dataValues = {};
  dataValues["workOrder"] = wo;
  dataValues["field"] = "inspection";

  if (info.innerText == "Incoming Inspection") {
    info.innerText = "";
    info.className = "bg-success";
    dataValues["data"] = "false";
  } else {
    info.innerText = "Incoming Inspection";
    info.className = "bg-warning";
    dataValues["data"] = "true";
  }
  POST(dataValues);
}

/*
-------------------------------------------------------
Updates the status of a particular operation for a work 
order.
Use: updateStatus(wo, op)
-------------------------------------------------------
Parameters:
    wo - the work order number (string)
    op - the operation number (string)
Returns:
    None
-------------------------------------------------------
*/
function updateStatus(wo, op) {
  let cell = document.getElementById(`${wo}-${op}`);
  let dataValues = {};
  let statusLabel = document.getElementById(`${wo}-completed`);

  dataValues["workOrder"] = wo;
  dataValues["field"] = "operation";
  dataValues["op"] = op;
  if (cell.className == "pending") {
    let compltedHours =
      parseFloat(statusLabel.ariaPlaceholder) +
      parseFloat(cell.ariaPlaceholder);
    statusLabel.ariaPlaceholder = compltedHours;
    cell.className = "completed";
    dataValues["data"] = "completed";
    dataValues["comp"] = compltedHours;
  } else {
    cell.className = "pending";
    let compltedHours =
      parseFloat(statusLabel.ariaPlaceholder) -
      parseFloat(cell.ariaPlaceholder);
    statusLabel.ariaPlaceholder = compltedHours;
    dataValues["data"] = "pending";
    dataValues["comp"] = compltedHours;
  }

  POST(dataValues);
  updateCompleted(`${wo}-completed`);
}

/*
-------------------------------------------------------
Updates the completed percentage for all work orders.
Use: updateAllCompleted()
-------------------------------------------------------
Parameters:
    None
Returns:
    None
-------------------------------------------------------
*/
function updateAllCompleted() {
  nodes = document.querySelectorAll(".comp-per");
  for (i = 0; i < nodes.length; i++) {
    updateCompleted(nodes[i].id);
  }
}

/*
-------------------------------------------------------
Updates the completed percentage for a specific work 
order and operation.
Use: updateCompleted(id)
-------------------------------------------------------
Parameters:
    id - the ID of the HTML element containing the completed 
    percentage (string)
Returns:
    None
-------------------------------------------------------
*/
function updateCompleted(id) {
  let textBox = document.getElementById(id);
  textBox.innerText =
    Math.round(
      (parseFloat(textBox.ariaPlaceholder) / parseFloat(textBox.ariaLabel)) *
        100
    ) + "%";
}

/*
-------------------------------------------------------
Opens a modal window for editing the work center for a 
specific operation.
Use: modal(wo, op)
-------------------------------------------------------
Parameters:
    wo - the work order number (string)
    op - the operation number (string)
Returns:
    None
-------------------------------------------------------
*/
function modal(wo, op) {
  let modal = document.createElement("div");
  modal.style.zIndex = "100";

  let elm = document.getElementById(`${wo}-${op}`);

  modal.id = "modal";
  modal.style.top = "25%";
  modal.style.left = "37.5%";
  modal.className = "pop-up-window h-auto w-25 position-absolute";
  modal.innerHTML = `<div class="card">
  <div class="d-flex justify-content-between border-bottom align-items-center bg-dark">
    <span class="mx-2 text-white">Editing Work Center</span>
    <button type="button" class="btn btn-danger btn-sm" onclick="removeModal()" style="scale:.75">X</button>
  </div>
  <div class="card-body py-2">
    <div class='mx-3 my-2'>
        <input id='list1' class="w-100 text-center mt-3" value="${elm.innerText}" type="text" list="opertaion-options">
        <figcaption class="fs-7 mt-3 text-muted">
        <textarea name="notes1" cols="50" rows="10" class="vLargeTextField w-100 p-3" id="id_notes1" style='height:auto; outline:none;'>${elm.title}</textarea>
        For Work Order <cite title="Source Title" id='wo-txt'>${wo}</cite>, Step Number <cite title="Source Title" id='wo-op'>${op}</cite>
      </figcaption>
    </div>
    
    <div class="d-flex justify-content-end gap-2 px-2 mt-3 mb-2">
      <a class="btn btn-primary btn-sm mt-2 mb-1" onclick="saveChanges()">Save Changes</a>
      <a class="btn btn-sm btn-danger mt-2 mb-1" onclick="removeModal()">Discard</a>
    </div>  
  </div>
</div>`;
  document.body.appendChild(modal);

  let selectList = document.createElement("datalist");
  selectList.id = "opertaion-options";
  // Loop through the list items
  getMachines().forEach(function (item) {
    // Create a new option element
    var option = document.createElement("option");
    // Set the text of the option to the current item in the set
    option.text = item;
    option.value = item;
    // Append the option to the select element
    selectList.appendChild(option);
  });

  let inputBox = document.getElementById("list1");
  inputBox.appendChild(selectList);
  // alert(x);
  // fetchMachineList;
}

/*
-------------------------------------------------------
Saves the changes made in the modal window.
Use: saveChanges()
-------------------------------------------------------
Parameters:
    None
Returns:
    None
-------------------------------------------------------
*/
function saveChanges() {
  let dataValues = {};
  let wo = document.getElementById("wo-txt").innerText;
  let op = document.getElementById("wo-op").innerText;
  let newWorkCenter = document.getElementById("list1").value;
  let des = document.getElementById('id_notes1').value;
  dataValues["workOrder"] = wo;
  dataValues["op"] = op;
  dataValues["field"] = "updateOperation";
  dataValues["data"] = newWorkCenter;
  dataValues['des']= des
  // update table
  document.getElementById(`${wo}-${op}`).innerText = newWorkCenter;
  POST(dataValues);
  removeModal();
}

/*
-------------------------------------------------------
Retrieves a list of machines available for operation.
Use: getMachines()
-------------------------------------------------------
Parameters:
    None
Returns:
    A set containing the list of machines (Set)
-------------------------------------------------------
*/
function getMachines() {
  let operations = document.querySelectorAll(".pending");
  let opsFinal = new Set();
  for (i = 0; i < operations.length; i++) {
    opsFinal.add(operations[i].innerText);
  }
  return opsFinal;
}

/*
-------------------------------------------------------
Removes the modal window from the DOM.
Use: removeModal()
-------------------------------------------------------
Parameters:
    None
Returns:
    None
-------------------------------------------------------
*/
function removeModal() {
  document.body.removeChild(document.getElementById("modal"));
}






/*
-------------------------------------------------------
Opens a modal window for editing the work center for a 
specific operation.
Use: modal(wo, op)
-------------------------------------------------------
Parameters:
    wo - the work order number (string)
    op - the operation number (string)
Returns:
    None
-------------------------------------------------------
*/
function workOrderOptions(wo) {
  let modal = document.createElement("div");
  modal.style.zIndex = "100";

  let elm = document.getElementById(`${wo}`);

  modal.id = "modal";
  modal.style.top = "25%";
  modal.style.left = "37.5%";
  modal.className = "pop-up-window h-auto w-25 position-absolute";
  modal.innerHTML = `<div class="card">
  <div class="d-flex justify-content-between border-bottom align-items-center bg-dark">
    <span class="mx-2 text-white">${wo}</span>
    <button type="button" class="btn btn-danger btn-sm" onclick="removeModal()" style="scale:.75">X</button>
  </div>
  <div class="card-body px-1">
        <div class='mx-3 my-2'>
              <div class='mt-2'>
              <input type="checkbox" id="label1" name="label1"/>
              <label for="label1">Label Printed</label>
                </div>

              <div class='mt-2'>
                <input type="checkbox" id="released" name="fl"/>
                <label for="released">Released</label>
              </div>

              <div class='mt-2'>
                <input type="checkbox" id="completed" name="fl"/>
                <label for="completed">completed</label>
              </div>

              <div class='mt-2'>
                <input type="checkbox" id="drop" name="fl"/>
                <label for="drop">Drop From CBB Live</label>
              </div>

              <div class='mt-2'>
                <input type="checkbox" id="released" name="fl"/>
                <label for="released">Released</label>
              </div>
        </div>
    <div class="d-flex justify-content-end gap-2 mx-2">
      <a class="btn btn-sm btn-primary mt-2" onclick="removeModal()">Save Changes</a>
      <a class="btn btn-sm btn-danger mt-2" onclick="removeModal()">Discard</a>
    </div>  
  </div>
</div>`;
  document.body.appendChild(modal);

  // alert(x);
  // fetchMachineList;
}






function fetchData(url) {
  return fetch(url)  
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      return data;
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
      throw error;
    });
}
