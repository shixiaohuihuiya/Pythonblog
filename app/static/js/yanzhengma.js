// 验证码代码   初始化界面
createCode();
var code;

function createCode(){
    code = "";
    //var codeLength = 4;验证码长度
    var codeLength = Math.floor(Math.random()*(7-4)+4);//随机生成的验证码
    //Math.random()用法，取num1-num2之间的随机数，Math.random()*(num2-num1)+num1
    var yan = document.getElementsById("yan");//获取值
    var selectChar = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z');
    for(var i = 0;i < codeLength; i++){
        var charIndex = Math.floor(Math.random() * selectChar.length); //生成最大的字符串
        code += selectChar[charIndex];
        
    }
    //显示以及样式
    document.getElementsById("yan").style.fontFamily = "Fixedsys"; //字体的样式
    document.getElementsById("yan").style.color = "#b0000b"; //字体颜色
    document.getElementsById("yan").innerText = code; //显示
    
    //使用RGB显示随机颜色背景，取值范围为0-255
    var r = Math.floor(Math.random() * 256);
        g = Math.floor(Math.random() * 256);
        b = Math.floor(Math.random() * 256);
    
    var rgb = 'rgb('+ r + ',' + g + ',' + b + ')';
    yan.style.backgroundColor = rgb; 
}

//验证
