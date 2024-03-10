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
