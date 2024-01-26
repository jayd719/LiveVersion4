let workorders=[]
const resultbox = document.querySelector('.result-box');
const inputbox = document.getElementById('sreachbox');

inputbox.onkeyup=function(){
    let result=[];
    let input = inputbox.value;
    if (input.length){
        result=workorders.filter((keyword)=>{
            return keyword.toLowerCase().includes(input.toLowerCase());
        });
    }
    display(result);
}

function display(result){
    const content = result.map((list)=>{
       return "<li onclick=selectInput(this)>"+list+"</li>";
    })
    resultbox.innerHTML="<ul>"+content+"<ul>";
}


function selectInput(list){
    inputbox.value= list.innerHTML;
    resultbox.innerHTML=''
}