$(function(){
    formBorderActive();     // 进入页面自行启动
    var timer = setInterval(formBorderActive, 5000);
    toggleForm();           // 表单切换
    hasAccount();           // 绑定已有账号事件
    buttonClick();
    window.onload = function () {
        loadSkin();
    }
});


function toggleForm() {
    /*表单切换*/
    var formActive = function($form) {
        if (!$form.hasClass('form-active')) {
            $('.form-active').removeClass('form-active');
            $form.addClass('form-active');
        }
    };
    $('#loginButton').on('click', function() {
        window.location.href = "/user/login/";
    });
    $('#registerButton').on('click', function() {
        window.location.href = "/user/register/";
    })
}

function hasAccount() {
    $('#hasaccount').on('click', function() {
        $('#loginButton').trigger('click');
    })
}

function formBorderActive() {
    /*边框特效*/
    var $form = $('.border-active');
    if($form.hasClass('border-shine')) {
        setTimeout(function(){
                $form.removeClass('border-shine');
            }, 3000);
    } else {
        $form.addClass('border-shine');
    }
}

function buttonClick() {
    /*聚焦按钮*/
    $("#userButton").on('click', function() {
        $('#username').focus();
    });
    $("#pwdButton").on('click', function() {
        $('#password').focus();
    });
    $("#pwdButton1").on('click', function() {
        $('input[name="password1"]').focus();
    });
    $("#pwdButton2").on('click', function() {
        $('input[name="password2"]').focus();
    });
    $("#emailButton").on('click', function() {
        $('#email').focus();
    });
    $("#captchaButton").on('click', function() {
        $('#id_captcha_1').focus();
    });
    $("#register_form .captcha").click({'form_id': "register_form"}, refresh_captcha);
    $("#forgetpwd_form .captcha").click({'form_id': "forgetpwd_form"}, refresh_captcha);
    $(".msg-container").on('click', msgHide);
    storage = {
        header: {
            headerbox: "header-box-primary"
        },
        container: '/static/css/container.css',
        particle: "particle-primary"
    };
    nextStorage = {
        header: {
            headerbox: "header-box-white"
        },
        container: "/static/css/container-white.css",
        particle: "particle-white"
    };
    $(".changeBg").on('click', changeSkin);
}

// 简单用户名验证
function smUserVarify($selector) {
    var $value = $selector.val();
    var regPattern = /^([A-Za-z]+)(\w+)$/g;
    var headPattern = /^([A-Za-z]+)/g;
    var $errorInput = $('.error-input');
    if($value.length < 4){
        $selector.parent('div').addClass('has-error');
        $errorInput.text('用户名必须大于4位');
        return false;
    } else if (!headPattern.test($value)) {
        $selector.parent('div').addClass('has-error');
        $errorInput.text('用户名需以英文字母开头');
    } else if (!regPattern.test($value)) {
        $selector.parent('div').addClass('has-error');
        $errorInput.text('用户名只能使用英文字母, 数字, 下划线');
    } else if ($value.length > 26) {
        $selector.parent('div').addClass('has-error');
        $errorInput.text('用户名必须小于26位');
        return false;
    } else {
        return true;
    }
}

// 简单密码验证
function smPwdVarify($selector) {
    var $value = $selector.val();
    var $errorInput = $('.error-input');
    if($value.length < 6){
        $selector.parent('div').addClass('has-error');
        $errorInput.text('密码必须大于6位');
        return false;
    } else if ($value.length > 30) {
        $selector.parent('div').addClass('has-error');
        $errorInput.text('密码必须小于30位');
        return false;
    } else {
        return true;
    }
}

// 简单邮箱验证
function smEmailVarify($selector) {
    var $value = $selector.val();
    var emailPattern = /(\w+@.*?)(com)$|(cn)$|(net)$/g;
    var $errorInput = $('.error-input');
    if($value.search(emailPattern) === -1) {
        $selector.parent('div').addClass('has-error');
        $errorInput.text('请输入正确格式的邮箱');
        return false;
    }
    return true;
}

function smCodeVarify($captcha_0, $captcha_1) {
    var $errorInput = $('.error-input');
    if($captcha_0.val() != null && $captcha_1.val().length == 4) {
        return true;
    }
    $captcha_1.parent('div').addClass('has-error');
    $errorInput.text('请输入正确长度的验证码');
    return false;
}

function smConfPwdVarify($pwd1, $pwd2) {
    var $value1 = $pwd1.val();
    var $value2 = $pwd2.val();
    var $errorInput = $('.error-input');
    if ($value1 < 6) {
        $pwd1.parent('div').addClass('has-error');
        $errorInput.text('密码必须大于6位')
    } else if ($value1.length > 30) {
        $pwd1.parent('div').addClass('has-error');
        $errorInput.text('密码必须小于30位');
        return false;
    } else if ($value1 != $value2) {
        $pwd2.parent('div').addClass('has-error');
        $errorInput.text('两次密码必须一致');
        return false;
    } else {
        return true;
    }
}

// 刷新验证码
function refresh_captcha(event){
    $.get("/captcha/refresh/?"+Math.random(), function(result){
        $('#'+event.data.form_id+' .captcha').attr("src",result.image_url);
        $('#id_captcha_0').attr("value",result.key);
    });
    return false;
}

// 信息隐藏
function msgHide() {
    var $selector = $(".msg-container");
    if(!$selector.is(':animated')){
        var randomNum = Math.round(Math.random() * 10);
        if (randomNum < 5) {
            $selector.slideUp(500);
        } else {
            $selector.fadeOut(500);
        }
    }
}

// 更换皮肤
function changeSkin(){
    var headerBox = $('.header-box'),
        particles = $('#particles'),
        container = $('.skin');
    if (headerBox.hasClass('header-box-primary')) {
        setWhite(container, headerBox, particles);
    } else {
        setPrimary(container, headerBox, particles);
    }
}

function setWhite(container, headerBox, particles) {
    container.attr('href', nextStorage.container);
    headerBox.removeClass(storage.header.headerbox).addClass(nextStorage.header.headerbox);
    particles.removeClass(storage.particle).addClass(nextStorage.particle);
    toWhite();
    window.localStorage.setItem("skin", "nextStorage");
}

function setPrimary(container, headerBox, particles) {
    container.attr('href', storage.container);
    headerBox.removeClass(nextStorage.header.headerbox).addClass(storage.header.headerbox);
    particles.removeClass(nextStorage.particle).addClass(storage.particle);
    toPrimary();
    window.localStorage.setItem("skin", "storage");
}

function toWhite(){
    particlesJS.load('particles', '/static/js/particles/purewhitebg.json', function () {
        console.log('callback - particles.js config loaded');
    })
}

function toPrimary(){
    particlesJS.load('particles', '/static/js/particles/deepdarkbg.json', function () {
        console.log('callback - particles.js config loaded');
    })
}

// 动态加载js文件
function loadScript(url, callback) {
    var script = document.createElement("script");
    script.type = "text/javascript";
    if(typeof(callback) != "undefined"){
        if (script.readyState) {
            script.onreadystatechange = function () {
                if (script.readyState == "loaded" || script.readyState == "complete") {
                    script.onreadystatechange = null;
                    callback();
                }
            };
        } else {
            script.onload = function () {
                callback();
            };
        }
    }
    script.src = url;
    document.body.appendChild(script);
}

function loadSkin() {
    var skin = window.localStorage.getItem("skin"),
        $container = $('.skin'),
        $headerBox = $('.header-box'),
        $particles = $('#particles');
    if(skin !== null) {
        if(skin === "storage") {
            setPrimary($container, $headerBox, $particles);
        } else {
            setWhite($container, $headerBox, $particles);
        }
    } else {
        if($container.attr("href") === storage.container) {
            window.localStorage.setItem("skin", "storage");
        } else {
            window.localStorage.setItem("skin", "nextStorage");
        }
    }
}

function getQueryString(name) {
    var result = window.location.search.match(new RegExp("[\?\&]" + name + "=([^\&]+)", "i"));
    if (result == null || result.length < 1) {
        return "";
    }
    return result[1];
}