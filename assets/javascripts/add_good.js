plural = []

$("#unit > option").each(function() {
	if ($(this).text().endsWith('(s)')) {
		plural.push($(this).val());
	}
});

for (var i = 0; i < plural.length; i++) {
	key = plural[i]
	option = $('#unit > option[value=' + key + ']')
    option.text(option.text().substring(0, option.text().length - 3) + 's')
}

$('#quantity').on('input propertychange paste', function() {
	for (var i = 0; i < plural.length; i++) {
		key = plural[i]
		option = $('#unit > option[value=' + key + ']')
		if ($(this).val() == '1') {
			if (option.text().endsWith('s')) {
				option.text(option.text().substring(0, option.text().length - 1))
			}
		} else {
			if (!option.text().endsWith('s')) {
				option.text(option.text() + 's')
			}
		}
	}
});

$('#unit').on('input', function() {
	let quantity_for = "quantity";
	let quantity_label = $('label[for=' + quantity_for + ']');
	let value_for = "value";
	let value_label = $('label[for=' + value_for + ']');

	let optional_quantity = $('label[for=' + quantity_for + '-optional' + ']');
	let optional_value = $('label[for=' + value_for + '-optional' + ']');


	// if Intangible is selected, add (optional) to the quantity and value titles
	if ($(this).val() === 'ITG') {
		if (optional_quantity) {
			quantity_label.wrap('<span></span>');
			quantity_label.css('display', 'inline-block');
			$('<label class="govuk-label lite-form-optional" for="quantity-optional" style="display: inline-block">' +
				'(optional)</label>').insertAfter(quantity_label);

			value_label.wrap('<span></span>');
			value_label.css('display', 'inline-block');
			$('<label class="govuk-label lite-form-optional" for="value-optional" style="display: inline-block">' +
				'(optional)</label>').insertAfter(value_label);
		}
	} else {
		// remove the (optional) if any other type of unit is selected
		if (optional_quantity) {
			if (quantity_label.parent().is('span')) {
				quantity_label.unwrap();
				value_label.unwrap();
			}
			quantity_label.removeAttr('style');
			value_label.removeAttr('style');
			optional_quantity.remove();
			optional_value.remove();
		}
	}
});
