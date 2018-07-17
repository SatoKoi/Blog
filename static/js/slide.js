$(function(){
    var leftFlag=0,
        rightFlag=1,
        showFlag=1,
        hideFlag=0;
    imgContainerWidth = 750,
    imgContainerHeight = 300,
    imgCount = 5,
    imgTotalWidth = imgContainerWidth * (imgCount-1);
    var slideTimer = createSlideTimer();
    $('#img-container').on('mouseover', function() {
        arrowFade(showFlag);
    }).on('mouseout', function() {
        arrowFade(hideFlag);
    });
    $('#prev').on('click', function() {
        clearInterval(slideTimer);
        arrowClick(leftFlag);
        slideTimer = createSlideTimer();
    });
    $('#next').on('click', function() {
        clearInterval(slideTimer);
        arrowClick(rightFlag);
        slideTimer = createSlideTimer();
    });
    $('.img-button span').on('click', function (event) {
        clearInterval(slideTimer);
        buttonClick(event);
        slideTimer = createSlideTimer();
    });
    window.onresize = function() {
        resetStatus();
<<<<<<< HEAD
        // fixBottom();
=======
        fixBottom();
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
        clearInterval(slideTimer);
        var index = $('.img-button .on').attr('data-index');
        if($(window).width() > 1085) {
            imgContainerWidth = 750;
            imgTotalWidth = imgContainerWidth * (imgCount-1);
            resetImgStatus(index);
        } else if($(window).width() <= 1085) {
            imgContainerWidth = 800;
            imgTotalWidth = imgContainerWidth * (imgCount-1);
            resetImgStatus(index);
        }
        slideTimer = createSlideTimer();
    };
    window.onload = function() {
        fixBottom();
        clearInterval(slideTimer);
        var index = $('.img-button .on').attr('data-index');
        if($(window).width() > 1085) {
            imgContainerWidth = 750;
            imgTotalWidth = imgContainerWidth * (imgCount-1);
            resetImgStatus(index);
        } else if($(window).width() <= 1085) {
            imgContainerWidth = 800;
            imgTotalWidth = imgContainerWidth * (imgCount-1);
            resetImgStatus(index);
        }
        slideTimer = createSlideTimer();
    };
});

function arrowFade(flag) {
    /*箭头淡入淡出*/
    var $arrow = $('.arrow');
    if (flag){
        $arrow.fadeTo(100, 1);
    } else {
        $arrow.fadeTo(100, 0);
    }
}

function buttonSlide($buttons) {
    /*按钮滚动*/
    var $slideButton = $buttons.filter('[class="on"]');
    var index = $slideButton.attr('data-index');
    $slideButton.removeClass('on');
    if (index == 5) {
        index = 0;
    }
    $slideButton = $buttons.eq(index);
    $slideButton.addClass('on');
}

function arrowClick(flag) {
    /*箭头点击事件*/
    var $slideButton;
    var $activeButton = $('.img-button .on');
    if (flag){
        $slideButton = $activeButton.next();
        if ($slideButton.length === 0) {
            $slideButton = $('.img-button span').first();
        }
    } else {
        $slideButton = $activeButton.prev();
        if ($slideButton.length === 0) {
            $slideButton = $('.img-button span').last();
        }
    }
    if(!$('.img-list').is(':animated')){
        imgMove(flag);
        descSlide(flag);
        $activeButton.removeClass('on');
        $slideButton.addClass('on');
    }
}

function buttonClick(event) {
    /*按钮点击事件*/
    var $imgList = $('.img-list');
    if(!$imgList.is(':animated')){
        var $event = $(event.currentTarget);
        var $on = $('.img-button span[class="on"]');
        var index, step;
        index = $on.attr('data-index');
        $on.removeClass('on');
        $event.addClass('on');
        step = index - $event.attr('data-index');
        imgMove(null, step);
        descSlide(null, $event.attr('data-index'));
    }
}

function createSlideTimer() {
    /*创建定时器*/
    var $imgList = $('.img-list'),
        $buttons = $('.img-button').find('span'),
        $descs = $('.img-desc').find('p');
    return setInterval(function(){
        var left = parseInt($imgList.css('left')),
            speed;
        if (left <= -imgTotalWidth) {
            speed = imgTotalWidth;
        } else {
            speed = -imgContainerWidth;
        }
        left += speed;
        if(!$imgList.is(':animated')){
            $imgList.animate({left: left + 'px'}, 1000);
            buttonSlide($buttons);
            descToggle($descs);
        }
    }, 3000);
}

function imgMove(flag, step) {
    /*图片移动*/
    var $imgList = $('.img-list');
    var left = parseInt($imgList.css('left')),
        speed;
    /*向右*/
    if (step == undefined){
        if (flag) {
            if (left <= -imgTotalWidth) {
                speed = imgTotalWidth;
            } else {
                speed = -imgContainerWidth;
            }
        } else {
            /*向左*/
            if (left >= 0) {
                speed = -imgTotalWidth;
            } else {
                speed = imgContainerWidth;
            }
        }
    } else {
        speed = step * imgContainerWidth;
    }
    left += speed;
    $imgList.animate({left: left + 'px'}, 1000);
}


function descToggle($descs) {
    /* 自动切换描述 */
    var $desc = $descs.filter('[class="on"]');
    var index = $desc.attr('data-index');
    $desc.removeClass('on');
    $desc.hide('slide', 200);
    if (index == 5) {
        index = 0;
    }
    $desc = $descs.eq(index);
    $desc.addClass('on');
    $desc.show('fold', 500);
}

function descSlide(flag, index) {
    /* 点击切换描述 */
    var $slideDesc;
    var $activeDesc = $('.img-desc .on');
    if(index === undefined){
        if (flag){
            $slideDesc = $activeDesc.parent('a').next().find('p');
            if (!$slideDesc.is('p')) {
                $slideDesc = $('.img-desc p').first();
            }
        } else {
            $slideDesc = $activeDesc.parent('a').prev().find('p');
            if (!$slideDesc.is('p')) {
                $slideDesc = $('.img-desc p').last();
            }
        }
    } else {
        $slideDesc = $('.img-desc p').eq(index-1);
        if($slideDesc.hasClass('on')) {
            return;
        }
    }
    $activeDesc.removeClass('on');
    $activeDesc.hide('slide', 200);
    $slideDesc.addClass('on');
    $slideDesc.show('fold', 500);
}

// 重置图片状态
function resetImgStatus(index) {
    $('.img-list').css('left', -(index-1) * imgContainerWidth + 'px');
}

// 重置移动端nav状态
function resetStatus() {
    if($(window).width() > '490') {
        $('.nav-menu').css('display', 'none');
    }
}
<<<<<<< HEAD
=======

// 底部固定
function fixBottom() {
    if($('.transform-body').height() < '640') {
        $('#footer').addClass('footer-fix');
    } else{
        $('#footer').removeClass('footer-fix');
    }
}
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
