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