function nextDay(cur_date) {
    const date = new Date(cur_date);
    date.setDate(date.getDate() + 1);
    location.href = '/diary/' + parseDate(date);
}

function prevDay(cur_date) {
    const date = new Date(cur_date);
    date.setDate(date.getDate() - 1);
    location.href = '/diary/' + parseDate(date);
}

function parseDate(date) {
    const year = date.getFullYear();
    let month = date.getMonth() + 1;
    let dt = date.getDate();
    if (dt < 10) {
        dt = '0' + dt;
    }
    if (month < 10) {
        month = '0' + month;
    }
    return year + '-' + month + '-' + dt;
}
