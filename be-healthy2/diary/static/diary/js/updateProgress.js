function updateProgressCalories(v1, v2) {
    let node = document.getElementsByClassName('progress-bar')[0];
    const v = parseFloat(v1) / parseFloat(v2) * 100;
    node.ariaValuenow = v;
    node.style.width = v + '%';
}
function updateProgressProteins(v1, v2) {
    let node = document.getElementsByClassName('progress-bar')[1];
    const v = parseFloat(v1) / parseFloat(v2) * 100;
    node.ariaValuenow = v;
    node.style.width = v + '%';
}
function updateProgressFats(v1, v2) {
    let node = document.getElementsByClassName('progress-bar')[2];
    const v = parseFloat(v1) / parseFloat(v2) * 100;
    node.ariaValuenow = v;
    node.style.width = v + '%';
}
function updateProgressCarbs(v1, v2) {
    let node = document.getElementsByClassName('progress-bar')[3];
    const v = parseFloat(v1) / parseFloat(v2)  * 100;
    node.ariaValuenow = v;
    node.style.width = v + '%';
}