$(function(){
var filechooser = document.getElementById('filechooser');
var previewer = document.getElementById('previewer');

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
});