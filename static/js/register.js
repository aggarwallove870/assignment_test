
  $('#eye').click(function(){
     
      if($(this).hasClass('fa-eye-slash')){
         
        $(this).removeClass('fa-eye-slash');
        
        $(this).addClass('fa-eye');
        
        $('#password').attr('type','text');
          
      }else{
       
        $(this).removeClass('fa-eye');
        
        $(this).addClass('fa-eye-slash');  
        
        $('#password').attr('type','password');
      }
  });


  $('#eyes').click(function(){
     
      if($(this).hasClass('fa-eye-slash')){
         
        $(this).removeClass('fa-eye-slash');
        
        $(this).addClass('fa-eye');
        
        $('#confirm_password').attr('type','text');
          
      }else{
       
        $(this).removeClass('fa-eye');
        
        $(this).addClass('fa-eye-slash');  
        
        $('#confirm_password').attr('type','password');
      }
  });
