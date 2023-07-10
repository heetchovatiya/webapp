function remove_file() {
  const modal = document.getElementById("modal_form");

  const element = document.getElementById("upload_file");
  element.remove();


  var a= document.createElement("div");
  a.setAttribute("class","row");
  a.setAttribute("id","dropdown");

  var b= document.createElement("div");
  b.setAttribute("class","col-25");
  
  var c= document.createElement("label");
  c.setAttribute("for","mySelect");
  c.innerHTML="subject";
 
  var d= document.createElement("div");
  d.setAttribute("class","col-75");


  var x = document.createElement("SELECT");
  x.setAttribute("id", "mySelect");
  x.setAttribute("name","dropdown_value")
  d.appendChild(x);


  var y = document.createElement("optgroup");
  y.setAttribute("label", "SEM-II");
  

  var z = document.createElement("option");
  z.setAttribute("value", "Fee");
   
  
  var t = document.createTextNode("fee");
  z.appendChild(t);
  y.appendChild(z);
  x.appendChild(y);
  d.appendChild(x);
  b.appendChild(c);
  a.appendChild(b);
  a.appendChild(d);
  const modal_element = document.getElementById("copies");
  modal.insertBefore(a,modal_element);



}
$(document).ready(function() {
      $('.open-modal-btn').click(function() {
        // Load the modal content from the external file
        $('#modalContainer').load('modal.html', function() {
          // Display the modal once it's loaded
          $('#modal').show();
        });
      });
    });

  