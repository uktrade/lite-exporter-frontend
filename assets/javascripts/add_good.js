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

	// if Intangible is selected, add (optional) to the quantity and value titles
	if ($(this).val() === 'ITG') {
		if (!quantity_label.text().endsWith('(optional)')) {
			quantity_label.text(quantity_label.text() + " (optional)");
			value_label.text(value_label.text() + " (optional)");
		}
	} else {
		// remove the (optional) if any other type of unit is selected
		if (quantity_label.text().endsWith('(optional)')) {
			quantity_label.text(quantity_label.text().substring(0, quantity_label.text().indexOf(" (optional)", 0)));
			value_label.text(value_label.text().substring(0, value_label.text().indexOf(" (optional)", 0)));
		}
	}
});
