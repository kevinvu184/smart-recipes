'use strict';
const loggedOutLinks = document.querySelectorAll('.logged-out');
const loggedInLinks = document.querySelectorAll('.logged-in');
const accountDetails = document.querySelector('.account-details');
const welcomeCal = document.querySelector('.welcome-cal');

const setUpNav = (user) => {
    if (user) {
        loggedInLinks.forEach(item => item.style.display = 'block');
        loggedOutLinks.forEach(item => item.style.display = 'none');
        const html_1 = `
            <div>Logged in as ${user.email}</div>
        `;
        const html_2 = `
            <span>Hi ${user.email} !</span>
        `;
        accountDetails.innerHTML = html_1;
        welcomeCal.innerHTML = html_2;
    } else {
        loggedOutLinks.forEach(item => item.style.display = 'block');
        loggedInLinks.forEach(item => item.style.display = 'none');
        accountDetails.innerHTML = '';
        welcomeCal.innerHTML = '';
    }
};

$(document).ready(function () {
    var i = 0;
    $('#btn-i0').click(function () {
       i++;
       $('#ingredient-field').append('<div class="row" id="row-i'+i+'">\n' +
           '                        <div class="col-3 mt-1 px-1">\n' +
           '                            <input required type="text" name="ingredient-quantity['+i+']" class="form-control"\n' +
           '                                   id="ingredient-quantity-'+i+'" placeholder="How much?" value="">\n' +
           '                        </div>\n' +
           '                        <div class="col-7 mt-1 px-1">\n' +
           '                            <input required type="text" name="ingredient-name['+i+']" class="form-control"\n' +
           '                                   id="ingredient-name-'+i+'"\n' +
           '                                   placeholder="List your ingredients, click button for even more steps!" value="">\n' +
           '                        </div>\n' +
           '                        <button type="button" class="col-2 btn btn-danger mt-1 px-1 btn_remove" id="'+i+'">-</button>\n' +
           '                    </div>')
    });
    $(document).on('click','.btn_remove', function () {
       var button_id_i = $(this).attr("id");
       $("#row-i"+button_id_i+"").remove();
    });

    var j = 1;
    $('#btn-c0').click(function () {
       j++;
       $('#recipe-field').append('<div class="row" id="row-c'+j+'">\n' +
           '                        <div class="col-1 mt-1 px-1">\n' +
           '                            <input required type="text" name="cook-step['+j+']" class="form-control" id="cook-step-'+j+'"\n' +
           '                                   value="'+j+'" readonly>\n' +
           '                        </div>\n' +
           '                        <div class="col-9 mt-1 px-1">\n' +
           '                            <input required type="text" name="cook-name['+j+']" class="form-control" id="cook-name-'+j+'"\n' +
           '                                   placeholder="List your step, click button for even more steps!" value="">\n' +
           '                        </div>\n' +
           '                        <button type="button" class="col-2 btn btn-danger mt-1 px-1 btn_remove" id="'+j+'">-</button>\n' +
           '                    </div>')
    });
    $(document).on('click','.btn_remove', function () {
       var button_id_c = $(this).attr("id");
       $("#row-c"+button_id_c+"").remove();
    });
    $('#btn-ing').click(function () {
        i++;
        $('#ingredient-field2').append('<div class="row" id="row-i'+i+'">\n' +
            '                        <div class="col-3 mt-1 px-1">\n' +
            '                            <input required type="text" name="newIngQty" class="form-control"\n' +
            '                                   id="ingredient-quantity-'+i+'" placeholder="How much?" value="">\n' +
            '                        </div>\n' +
            '                        <div class="col-7 mt-1 px-1">\n' +
            '                            <input required type="text" name="newIng" class="form-control"\n' +
            '                                   id="ingredient-name-'+i+'"\n' +
            '                                   placeholder="List your ingredients, click button for even more steps!" value="">\n' +
            '                        </div>\n' +
            '                        <button type="button" class="col-2 btn btn-danger mt-1 px-1 btn_remove" id="'+i+'">-</button>\n' +
            '                    </div>')
     });
     var j = 1;
     $('#btn-step').click(function () {
        j++;
        $('#recipe-field2').append('<div class="row" id="row-c'+j+'">\n' +
            '                        <div class="col-1 mt-1 px-1">\n' +
            '                            <input required type="text" name="stepNum" class="form-control" id="cook-step-'+j+'"\n' +
            '                                   value="'+j+'" readonly>\n' +
            '                        </div>\n' +
            '                        <div class="col-9 mt-1 px-1">\n' +
            '                            <input required type="text" name="stepName" class="form-control" id="cook-name-'+j+'"\n' +
            '                                   placeholder="List your step, click button for even more steps!" value="">\n' +
            '                        </div>\n' +
            '                        <button type="button" class="col-2 btn btn-danger mt-1 px-1 btn_remove" id="'+j+'">-</button>\n' +
            '                    </div>')
     });
});

// $(document).ready(function () {
//     var i = 0;
    
// });