const resultbox = document.querySelector(".result-box");
const inputbox = document.getElementById("sreachbox");

inputbox.onkeyup = function () {
  let result = [];
  let input = inputbox.value;
  if (input.length) {
    result = workorders.filter((keyword) => {
      return keyword.toLowerCase().includes(input.toLowerCase());
    });
  }
  display(result);
};

function display(result) {
  const content = result.map((list) => {
    return "<li onclick=selectInput(this)>" + list + "</li>";
  });

  text = "";
  for (let i = 0; i < content.length; i++) {
    text += content[i];
  }
  resultbox.innerHTML = "<ul>" + text + "</ul>";
}

function selectInput(list) {
  inputbox.value = list.innerHTML;
  resultbox.innerHTML = "";
}
