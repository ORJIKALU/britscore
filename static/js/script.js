$('.form').find('input, textarea').on('keyup blur focus', function (e) {
  
  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight'); 
			} else {
		    label.removeClass('highlight');   
			}   
    } else if (e.type === 'focus') {
      
      if( $this.val() === '' ) {
    		label.removeClass('highlight'); 
			} 
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

});

$('.tab a,.links a').on('click', function (e) {
  
  e.preventDefault();
  
  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');
  
  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();
  
  $(target).fadeIn(600);
  
});

addEventListener("load", function() { 
  setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); } 
  
addEventListener("load", function() 
{ setTimeout(hideURLbar, 0); }, false); function hideURLbar(){ window.scrollTo(0,1); } 


  function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

$(function() {
    $('#login').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('input[name="username"]').val() == ""){
    alert("you must provide a username");
  }
  
 else if($('input[name="password"]').val() ==""){
    alert("you must provide a password");
  }
 else{
      $.post( $SCRIPT_ROOT + '/login_check',{
        username: $('input[name="username"]').val(),
        password: $('input[name="password"]').val()
      }, function(data) {
          if (data == "fail"){alert("invalid username or password")}
          else{
            $("#login_form").submit();
          }
      });}
    });
  });


$(function() {
    $('#submit_registration').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('input[name="firstname"]').val() == ""){
    alert("you must provide a firstname");
  }
  
 else if($('input[name="surname"]').val() ==""){
    alert("you must provide a surname");
  }
  else if($('input[name="email"]').val() ==""){
    alert("you must provide a email");
  }
    else if(validateEmail($('input[name="email"]').val()) !=true){
    alert("email not valid");
  }

 else if($('input[name="username"]').val() ==""){
    alert("you must provide a username");
  }
 else if($('input[name="password"]').val() ==""){
    alert("you must provide a password");
  }
   else if($('input[name="password"]').val() != $('input[name="confirmation"]').val()){
    alert("password and confirmation do not match");
  }

 else{     
    
      $.post( $SCRIPT_ROOT + '/username_check',{
        username: $('input[name="username"]').val()
      }, function(data) {
          if (data == "false")
          {alert("username already taken")}
          else{ $.post( $SCRIPT_ROOT + '/email_check',{
        email: $('input[name="email"]').val()
      }, function(data) {
          if (data == "false")
          {alert("email already belongs to another account")}
          else{$("#register").submit();
};
      });};
      });

 }

    });
  });

$(function() {
    $('#client_button').bind('click', function() {
  // Stop form from submitting normally
  event.preventDefault();
  if($('input[name="client_name"]').val() == ""){
    alert("you must provide a username");
  }
  else{
      $.post( $SCRIPT_ROOT + '/client_check',{
        name: $('input[name="client_name"]').val(),
      }, function(data) {
          if (data == "fail"){alert("client already exist")}
          else{
            $("#client_form").submit();
          }
      });}
});
  });
  

