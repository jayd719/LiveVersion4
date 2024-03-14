updateDate();
notesColor();

// Delete Nav var Not Used
function deleteNavBar() {
  document.body.removeChild(document.getElementById("nav-bar"));
}

function checkNote(elm){
  if(elm.value=='HOLD FOR CUSTOMER'){
    elm.className='alert-danger'
    elm.style.color = "white";
  }else{
    elm.className=''
  }
  

}

function notesColor() {
  let notes = document.querySelectorAll(".notes");
  for (i = 0; i < notes.length; i++) {
    if (notes[i].value.toLowerCase() == "none" || notes[i].value.length < 2) {
      notes[i].value = "";
      // className='alert-danger'
    }else{
      checkNote(notes[i])
    }
  }
}

// update due in
function updateDate() {
  let dueDates = document.querySelectorAll(".dueDate");
  let dates = document.querySelectorAll("#due-in");
  for (i = 0; i < dates.length; i++) {
    const targetDate = new Date(dueDates[i].value);
    const currentDate = new Date();
    const dueIn = Math.ceil((targetDate - currentDate) / (1000 * 60 * 60 * 24));
    dates[i].innerHTML = dueIn;
    if (dueIn < 0) {
      dates[i].className = "alert-danger";
      dates[i].style.color = "white";
    } else if (dueIn >= 0 && dueIn <= 7) {
      dates[i].className = "alert-warning";
    } else {
      dates[i].className = "alert-success";
    }
  }
}

// function to write back to server
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

function updateNotes(elmID, wo) {
  let dataValues = {};
  dataValues["workOrder"] = wo;
  dataValues["field"] = "notes";
  dataValues["data"] = document.getElementById(elmID).value;
  POST(dataValues);
  checkNote(document.getElementById(elmID))
}

function updateShippingThisMonth(wo, value) {
  let dataValues = {};
  dataValues["workOrder"] = wo;
  dataValues["field"] = "stm";
  dataValues["data"] = value;
  POST(dataValues);
}

function writeDate(wo, elmID) {
  let dataValues = {};
  dataValues["workOrder"] = wo;
  dataValues["field"] = "dueDate";
  dataValues["data"] = document.getElementById(elmID).value;
  POST(dataValues);
  updateDate();
}

function convertAndSend() {
  var tableData = [];
  var headers = [];

  // Get table headers
  $("#data-table th").each(function () {
    headers.push($(this).text());
  });

  // Iterate over table rows
  $("#data-table tbody tr").each(function () {
    var rowData = {};
    var currentRow = $(this);

    // Iterate over each cell in the row
    currentRow.find("td").each(function (index) {
      rowData[headers[index]] = $(this).text();
    });

    tableData.push(rowData);
  });

  // Convert data to JSON
  var jsonData = JSON.stringify(tableData);

  // Send data to the server using AJAX
  $.ajax({
    type: "POST",
    url: "/update_data/", // Replace with your server endpoint
    data: jsonData,
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function (response) {
      console.log("Data sent successfully:", response);
    },
    error: function (error) {
      alert("COULD NOT SAVE DATA");
    },
  });
}
