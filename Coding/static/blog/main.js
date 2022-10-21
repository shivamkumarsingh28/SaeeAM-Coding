const join = document.getElementById("joinus");

join.addEventListener('click', () => {
    console.log("click")
    if (join.textContent === 'JOIN US') {
     JOIN()
    } else {
      alert("sorry")
    }
  });
function JOIN(){
    const Name = document.createElement("input");
    Name.type = "text";
    Name.class = "form-control";
    Name.placeholder= "HEllo Check";
    document.getElementById("located").appendChild(Name);
}