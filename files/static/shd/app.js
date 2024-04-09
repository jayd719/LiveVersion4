function POST(data) {
  var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
  let jsonData = JSON.stringify(data);
  $.ajax({
    type: "POST",
    url: "download/", // Replace with your server endpoint
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
      alert("Failed To Download File");
    },
  });
}

function downloadShd(workCenter) {
  let dataValues = {};
  dataValues["workCenter"] = workCenter;
  POST(dataValues);
  loader()
  setTimeout(()=>{
    removeLoader()
    window.open(`/templates/excel/${workCenter}.xlsx`)
  }, 3000);
  
}

function loader() {
  let modal = document.createElement("div");
  modal.id = "modal";
  modal.className = "cover-container d-flex w-100 h-100 p-3 flex-column d-flex justify-content-center align-items-center position-absolute gd";
  modal.innerHTML = `
    <div class="loader border rounded-5"></div>
    <div class="loader2"></div>`;
  document.body.appendChild(modal);
}
function removeLoader() {
    document.body.removeChild(document.getElementById("modal"));
    
  }
  
  
