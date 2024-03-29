function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function cloneMore(selector, prefix, from, to, suffix='') {
    var newElement = $(selector).clone(true);
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        var name = $(this).attr('name')
        if(name) {
            name = name.replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });
    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
          forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
          $(this).attr({'for': forValue});
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row'+suffix+':not(:last)');
    conditionRow.find('.btn.'+from)
    .removeClass('btn-primary').addClass('btn-secondary')
    .removeClass(from).addClass(to)
    .html('-');
    return false;
}
function deleteForm(prefix, btn, suffix='') {
        btn.closest('.form-row'+suffix).remove();
        var forms = $('.form-row'+suffix);
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    return false;
}

$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneMore('.form-row:last', 'ingredient_amount', 'add-form-row', 'remove-form-row');
    return false;
});
$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('ingredient_amount', $(this));
    return false;
});