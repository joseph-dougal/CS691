$(document).ready(function(){
    $('#confirm_password').keyup( function(e){
        var password = $('#password').val();
        var confirm_password = $('#confirm_password').val();


        if(password != confirm_password){
  
           $('#pass_response').html("The two passwords that you entered do not match.").css({'color':'red', 'text-align':'right'});
           $('#button').prop('disabled', true);
        }else{
           $("#pass_response").html("");
           $('#button').removeAttr('disabled');
        }
    })
})