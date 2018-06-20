$(function() {
    $('#id_captcha_1').addClass('form-control').attr('placeholder', '请输入四位验证码');     // 为插件生成的验证码表单框添加bootstrap样式
    var fmy = {
        formVarify: formVarify,
        userVarify: userVarify,
        pwdVarify: passwordVarify
    };
    fmy.formVarify();
});

function formVarify() {
    /*表单验证*/
    $('#email').on('change', function() {
        var emailPattern = /(\w+@.*?)(com)$|(cn)$|(net)$/g;
        var $value = $(this).val(),
            $tip = $(this).parents('.form-group').next('p');
        var $parentDiv = $(this).parent('div');
        if($parentDiv.hasClass('has-success')) {
            $parentDiv.removeClass('has-success');
        }
        if($value.search(emailPattern) === -1) {
            $(this).parent('div').addClass('has-error');
            clearStatus();
            $tip.text('请输入正确格式的邮箱').addClass('tip-active');
        } else {
            $(this).parent('div').removeClass('has-error').addClass('has-success');
            clearStatus();
        }
    });
    $('#id_captcha_1').on('change', function() {
        var $value = $(this).val(),
            $tip = $(this).parents('.form-group').next('p');
        var $parentDiv = $(this).parent('div');
        if($parentDiv.hasClass('has-success')) {
            $parentDiv.removeClass('has-success');
        }
        if($value.length !== 4) {
            $(this).parent('div').addClass('has-error');
            clearStatus();
            $tip.text('验证码格式错误').addClass('tip-active');
        } else {
            $(this).parent('div').removeClass('has-error').addClass('has-success');
            clearStatus();
        }
    }).on('keyup', function() {
        var $value = $(this).val(),
            $tip = $(this).parents('.form-group').next('p');
        var $parentDiv = $(this).parent('div');
        if($parentDiv.hasClass('has-success')) {
            $parentDiv.removeClass('has-success');
        }
        if($value.length > 4) {
            $(this).parent('div').addClass('has-error');
            clearStatus();
            $tip.text('验证码格式错误').addClass('tip-active');
        }  else {
            clearStatus();
        }
    });
    userVarify($('#username'));
    passwordVarify($('#password'), $('#icon-key2'), 1);
    passwordVarify($('input[name="password1"]'), $('.icon-key'));
    passwordVarify($('input[name="password2"]'), $('.icon-lock'));
}

function clearStatus() {
    /*清除状态*/
    $('.tip-left').removeClass('tip-left');
    $('.tip-active').removeClass('tip-active');
}

function setPwdScale($self, scale) {
    /*密码强度评级*/
    var $buttonInline = $self.parents('.form-group').children('.button-inline');
    if(scale <= 3) {
        $buttonInline.append('<p class="pwd-tip pwd-tip-sm">弱</p>')
    } else if(scale <= 7) {
        $buttonInline.append('<p class="pwd-tip pwd-tip-md">中</p>')
    } else if(scale <= 10) {
        $buttonInline.append('<p class="pwd-tip pwd-tip-lg md-padding">较强</p>')
    } else {
        $buttonInline.append('<p class="pwd-tip pwd-tip-xl">强</p>')
    }
}

function userVarify($selector) {
    $selector.on('keyup', function() {
        var $value = $(this).val();
        var headPattern = /^([A-Za-z]+)/g;
        var regPattern = /^([A-Za-z]+)(\w+)$/g;
        var $tip = $(this).parents('.form-group').next('p');
        var $parentDiv = $(this).parent('div');
        if($parentDiv.hasClass('has-success')) {
            $parentDiv.removeClass('has-success');
        }
        if($value.length < 4){
            $(this).parent('div').addClass('has-error');
            clearStatus();
            $tip.text('用户名不得小于四位').addClass('tip-active');
        } else if (!headPattern.test($value)) {
            $(this).parent('div').addClass('has-error');
            clearStatus();
            $tip.text('用户名只能以英文字母开头').addClass('tip-active').addClass('tip-left');
        } else if (!regPattern.test($value)) {
            $(this).parent('div').addClass('has-error');
            clearStatus();
            $tip.text('用户名只能使用英文字母, 数字, 下划线').addClass('tip-active').addClass('tip-left');
        } else if ($value.length > 26) {
            $(this).parent('div').addClass('has-error');
            clearStatus();
            $tip.text('用户名不得大于26位').addClass('tip-active');
        } else {
            $parentDiv.removeClass('has-error').addClass('has-success');
            clearStatus();
        }
    });
}

function passwordVarify ($selector, $icon, flag) {
    $selector.on('keyup', function() {
        var $value = $(this).val();
        var numPattern = /(\d+)/g;
        var smallWordPattern = /([a-z]+)/g;
        var bigWordPattern = /([A-Z]+)/g;
        var strongPattern = /([@#_]+)/g;
        var $tip = $(this).parents('.form-group').next('p');
        var $parentDiv = $(this).parent('div');
        if($parentDiv.hasClass('has-success')) {
            $parentDiv.removeClass('has-success');
        }
        if(flag){
            $('.pwd-tip').remove();
            $('.font-hidden').removeClass('font-hidden');
        } else {
            $(this).parents('.form-group').find('.pwd-tip').remove();
            if($value.length < 6 || $value.length > 30 || $value.search(/([^\w@#_]+)/) !== -1) {
                $(this).parents('.form-group').find('.font-hidden').removeClass('font-hidden');
            }
        }
        if($value.length < 6){
            $(this).parent('div').addClass('has-error');
            clearStatus();
            $tip.text('密码不得小于六位').addClass('tip-active');
        } else if ($value.length > 30) {
            $(this).parent('div').addClass('has-error');
            clearStatus();
            $tip.text('密码不得大于30位').addClass('tip-active');
        } else if ($value.search(/([^\w@#_]+)/) !== -1) {
            $(this).parent('div').addClass('has-error');
            clearStatus();
            $tip.text('密码由字母,数字,@#_这些特殊字符组成').addClass('tip-active').addClass('tip-left');
        } else {
            var strong = 0;
            if ($value.search(numPattern) !== -1) {
                strong += 1;
            }
            if ($value.search(smallWordPattern) !== -1) {
                strong += 1;
            }
            if ($value.search(bigWordPattern) !== -1) {
                strong += 1;
            }
            if ($value.search(strongPattern) !== -1) {
                strong += 1;
            }
            var len = Math.sqrt($value.length);
            $icon.addClass('font-hidden');
            setPwdScale($(this), strong * len);
            $parentDiv.removeClass('has-error').addClass('has-success');
            clearStatus();
        }
    });
}


