updateDate();


function deleteNavBar() {
  document.body.removeChild(document.getElementById("nav-bar"));
}

// update due date color
function updateDate() {
  let dates = document.querySelectorAll("#due-in");
  for (i = 0; i < dates.length; i++) {
    const targetDate = new Date(dates[i].textContent);
    const currentDate = new Date();
    const dueIn = Math.ceil((targetDate - currentDate) / (1000 * 60 * 60 * 24));
    dates[i].innerHTML = dueIn;
    if (dueIn < 0) {
      dates[i].className = "alert-danger";
      dates[i].style.color ='white'
    } else if (dueIn >= 0 && dueIn <= 7) {
      dates[i].className = "alert-warning";
    } else {
      dates[i].className = "alert-success";
    }
  }
}




function updateValue(id,out) {
  var inputElement = document.getElementById(id);
  var spanElement = document.getElementById(out);
  spanElement.textContent = inputElement.value;
}


function updateData(workOrder,field,data) {
  let dataValues ={}
  dataValues['workOrder']=workOrder
  dataValues['Field']=field
  dataValues['data']=data

}

function updateData(workOrder,field,data) {
  let dataValues ={}
  dataValues['workOrder']=workOrder
  dataValues['Field']=field
  dataValues['data']=data
  
  // Convert data to JSON
  var jsonData = JSON.stringify(dataValues);

  // Send data to the server using AJAX
  $.ajax({
    type: 'POST',
    url: '/handle_json_data/', // Replace with your server endpoint
    data: jsonData,
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function (response) {
      console.log('Data sent successfully:', response);
    },
    error: function (error) {
     alert('COULD NOT SAVE DATA')
    }
  });
}





function convertAndSend() {
  var tableData = [];
  var headers = [];
  
  // Get table headers
  $('#data-table th').each(function () {
    headers.push($(this).text());
  });

  // Iterate over table rows
  $('#data-table tbody tr').each(function () {
    var rowData = {};
    var currentRow = $(this);

    // Iterate over each cell in the row
    currentRow.find('td').each(function (index) {
      rowData[headers[index]] = $(this).text();
    });

    tableData.push(rowData);
  });

  // Convert data to JSON
  var jsonData = JSON.stringify(tableData);

  // Send data to the server using AJAX
  $.ajax({
    type: 'POST',
    url: '/handle_json_data/', // Replace with your server endpoint
    data: jsonData,
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function (response) {
      console.log('Data sent successfully:', response);
    },
    error: function (error) {
     alert('COULD NOT SAVE DATA')
    }
  });
}