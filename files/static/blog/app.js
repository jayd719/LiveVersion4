function InvalidForm() {
  alert("Invalid Form");
}


function ChangeCSS(from, to, class_) {
  let var1 = $(from);

  if (class_) {
    var1.removeClass(from.slice(1)).addClass(to.slice(1));
  } else {
    var1.removeClass(to.slice(1)).addClass(from.slice(1));
  }
}