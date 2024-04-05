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
  window.open('/templates/excel/Scheduling Format.xlsx')
  
//   downloadBox()
}

function downloadBox() {
  let modal = document.createElement("div");
  modal.style.zIndex = "100";
  modal.id = "modal";
  modal.style.top = "25%";
  modal.style.left = "37.5%";
  modal.className = "pop-up-window h-auto w-25 position-absolute";
  modal.innerHTML = `<div class="card">
    <div class="d-flex justify-content-between border-bottom align-items-center bg-dark">
      <span class="mx-2 text-white">Download Report Data</span>
      <button type="button" class="btn btn-danger btn-sm" onclick="removeModal()" style="scale:.75">X</button>
    </div>
    <div class="card-body px-1 shadow-lg">
            

          <div class='mx-3 my-2'>
                <a href="/templates/excel/Scheduling Format.xlsx" onclick="removeModal()">get</a>
          </div>
      <div class="d-flex justify-content-end gap-2 mx-2">
        <a class="btn btn-sm btn-danger mt-2" onclick="removeModal()">Discard</a>
      </div>  
    </div>
  </div>`;
  document.body.appendChild(modal);
}
function removeModal() {
    document.body.removeChild(document.getElementById("modal"));
  }
  
  