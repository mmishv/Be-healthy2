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