$(function(){
var filechooser = document.getElementById('filechooser');
var previewer = document.getElementById('previewer');
var match = document.getElementById('match')

filechooser.onchange = function() {
    var files = this.files;
    var file = files[0];
  //  filechooser.value = '';

    // 接受 jpeg, jpg, png 类型的图片
    if (!/\/(?:jpeg|jpg|png)/i.test(file.type)) {
        alert("please select the image with correct format");
        filechooser.value = '';
        return;}

    var reader = new FileReader();

    reader.onload = function() {
    
        console.log(this.result);

        previewer.src = this.result ;

        // 清空图片上传框的值
        
    };

    reader.readAsDataURL(file);
}   

match.onclick=function(){

//add progress bar

  var elem = document.getElementById("myBar");   
  elem.style.display="none";
  $('#myBar').show();
  var width = 10;
  var id = setInterval(frame, 10);
  function frame() {
    if (width >= 99) {
      clearInterval(id);
    } else {
      width++; 
      elem.style.width = width + '%'; 
      elem.innerHTML = width * 1  + '%';
    }
  }
   
            console.log("submit event");

			var form_data = new FormData($('#uploadform')[0]);
                        var starttime = new Date();
			$.ajax({
			  url: "/upload",// change to be the backend receiver
			  type: "POST",
			  data: form_data,
			  dataType: 'json',
			  processData: false,  // tell jQuery not to process the data
			  contentType: false   // tell jQuery not to set contentType
			}).done(function(data) {

				var endtime = new Date();
                elem.style.display="none";
				var reult = document.getElementById('result');
				result.src = data.result;
                alert((endtime-starttime)/1000);
                
			});
            return false;

}


});
