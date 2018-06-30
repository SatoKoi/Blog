$(function(){
    var date_url = "/date/";
    var date = new Date();
    var dateHref = window.localStorage.getItem("date");
    if(dateHref === null){
        dateHref = [date.getFullYear(), date.getMonth()+1, date.getDate()].join('-');
    }
    if(window.location.pathname.indexOf(date_url) === -1) {
        dateHref = [date.getFullYear(), date.getMonth()+1, date.getDate()].join('-');
        window.localStorage.setItem('date', dateHref);
    }
    var mySchedule = new Schedule({
        el: '#date-box',
        date: dateHref,
        clickCb: function (y,m,d) {
            var date = [y, m, d].join('-');
            window.location.href = date_url + date;
            window.localStorage.setItem('date', date);
        },
        nextMonthCb: function (y,m,d) {
            var date = [y, m].join('-');
            window.location.href = date_url + date;
            window.localStorage.setItem('date', date + '-' + d);
        },
        nextYearCb: function (y,m,d) {
            var date = [y, m, d].join('-');
            window.location.href = date_url + y;
            window.localStorage.setItem('date', date);
        },
        prevMonthCb: function (y,m,d) {
            var date = [y, m].join('-');
            window.location.href = date_url + date;
            window.localStorage.setItem('date', date + '-' + d);
        },
        prevYearCb: function (y,m,d) {
            var date = [y, m, d].join('-');
            window.location.href = date_url + y;
            window.localStorage.setItem('date', date);
        }
    });
});