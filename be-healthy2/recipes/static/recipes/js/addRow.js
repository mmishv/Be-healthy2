function addRow(e, parent, container, child, pref='', post='') {
    if (e.classList.contains('disabled')) {
        e.parentElement.remove();
    } else {
        let temp = e.parentElement.cloneNode(true);
        e.classList.add('disabled');
        e.style.backgroundColor = '#114630a8';
        e.innerHTML = '-';
        temp.children[1].value = '';
        document.getElementById(parent).appendChild(temp);
    }
    let ingredients = document.getElementsByClassName(container);
    let quantity = "quantity";
    let measure = "measure";
    if (parent === 'cur-products') {
        quantity = "cur-quantity";
        measure = "cur-measure";
    }
    for (let i = 0; i < ingredients.length; i++) {
        const c = i + 1;
        ingredients[i].id = container + c;
        ingredients[i].name = container + c;
        let ch = ingredients[i].children;
        ch[0].id = child + c;
        ch[1].id = pref+quantity+post + c;
        ch[2].id = pref+measure+post + c;
        ch[0].name = child + c;
        ch[1].name = pref+quantity+post + c;
        ch[2].name = pref+measure+post + c;
    }
}