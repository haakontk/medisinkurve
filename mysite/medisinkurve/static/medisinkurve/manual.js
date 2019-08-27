$(document).ready(function() {

    $(".verticalunit1, .verticalunit2").hide();
    $("#cave_diagnose_div").show();
    $("#faste_medisiner_0").show();
    $("#behovs_medisiner_0").show();
    $(".verticalunit1:last").show();


//    This function shows div elements that are non-empty upon loading
    $(".verticalunit").each(function( index ) {
        if (index > 0){
            var indexInt                = index;
            var indexString             = indexInt.toString(10);
            var legemiddelnavn_id       = "id_form-" + indexString + "-legemiddelnavn";
            var legemiddelform_id       = "id_form-" + indexString + "-legemiddelform";
            var enhet_id                = "id_form-" + indexString + "-enhet";
            var administrasjonsform_id  = "id_form-" + indexString + "-administrasjonsform";
            var dose0008_id             = "id_form-" + indexString + "-dose0008";
            var dose0814_id             = "id_form-" + indexString + "-dose0814";
            var dose1420_id             = "id_form-" + indexString + "-dose1420";
            var dose2024_id             = "id_form-" + indexString + "-dose2024";
            var dosefritekst_id         = "id_form-" + indexString + "-dose_fritekst"; 

            if (document.querySelector("#" + legemiddelnavn_id).value != ''){
                $(this).show(); //Unhiding the next legemiddelrow
                var myDangerColor = "#ffc6c6";
                if (document.querySelector("#" + legemiddelform_id).value == ''){
                    $('#' + legemiddelform_id).css("background-color", myDangerColor);
                }
                if (document.querySelector("#" + enhet_id).value == ''){
                    $('#' + enhet_id).css("background-color", myDangerColor);
                }
                if (document.querySelector("#" + administrasjonsform_id).value == ''){
                    $('#' + administrasjonsform_id).css("background-color", myDangerColor);
                }
                if (index < 15){
                    if (document.querySelector('#' + dose0008_id).value == ''){
                        if (document.querySelector('#' + dose0814_id).value == ''){
                            if (document.querySelector('#' + dose1420_id).value == ''){
                                if (document.querySelector('#' + dose2024_id).value == ''){
                                    $('#' + dose0008_id).css("background-color", myDangerColor);
                                    $('#' + dose0814_id).css("background-color", myDangerColor);
                                    $('#' + dose1420_id).css("background-color", myDangerColor);
                                    $('#' + dose2024_id).css("background-color", myDangerColor);
                                }
                            }
                        }
                    }
                }
                if (index > 14 && index < 23){
                    if (document.querySelector('#' + dosefritekst_id).value == ''){
                        $('#' + dosefritekst_id).css("background-color", myDangerColor);
                    }
                }
            }
        }
    });

//    This function shows the next div element if the previous one contains field text
    $("input").change(function(){
        console.log(this);
        var divId = this.parentNode.parentNode.id;
        $('#' + divId).next().show();
    });
    $("input").focusout(function(){
        $('#' + this.id).css("background-color", "#ffffff");
    });
});

var x, i, j, selElmnt, a, b, c;
/* Look for any elements with the class "custom-select": */
x = document.getElementsByClassName("custom-select");
for (i = 0; i < x.length; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  /* For each element, create a new DIV that will act as the selected item: */
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  /* For each element, create a new DIV that will contain the option list: */
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 1; j < selElmnt.length; j++) {
    /* For each option in the original select element,
    create a new DIV that will act as an option item: */
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.addEventListener("click", function(e) {
        /* When an item is clicked, update the original select box,
        and the selected item: */
        var y, i, k, s, h;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        h = this.parentNode.previousSibling;
        for (i = 0; i < s.length; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;
            y = this.parentNode.getElementsByClassName("same-as-selected");
            for (k = 0; k < y.length; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
    /* When the select box is clicked, close any other select boxes,
    and open/close the current select box: */
    e.stopPropagation();
    closeAllSelect(this);
    this.nextSibling.classList.toggle("select-hide");
    this.classList.toggle("select-arrow-active");
  });
}

function closeAllSelect(elmnt) {
  /* A function that will close all select boxes in the document,
  except the current select box: */
  var x, y, i, arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  for (i = 0; i < y.length; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < x.length; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}

/* If the user clicks anywhere outside the select box,
then close all select boxes: */
document.addEventListener("click", closeAllSelect);
