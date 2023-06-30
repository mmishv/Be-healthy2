$(document).on('click', '.create-add-form-row', function(e){
    e.preventDefault();
    cloneMore('.form-row:last', 'product_amount', 'create-add-form-row', 'create-remove-form-row');
    return false;
});
$(document).on('click', '.create-remove-form-row', function(e){
    e.preventDefault();
    deleteForm('product_amount', $(this));
    return false;
});
function AddFormRowClick(selector, prefix) {
    const button = $(selector).find('.add-form-row-'+prefix);
    cloneMore(selector, prefix, 'add-form-row-'+prefix, 'remove-form-row-'+prefix, '-'+prefix);
    button[0].setAttribute('onclick','DeleteFormRowClick( this, "' + prefix + '")');
    return false;
}
function DeleteFormRowClick(selector, prefix) {
    const button = $(selector)
    deleteForm(prefix, button, '-'+prefix);
    return false;
}
