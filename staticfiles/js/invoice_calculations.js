django.jQuery(function($) {
    function calculateLineTotal(row) {
        var quantity = parseFloat($(row).find('input[name$="-quantity"]').val()) || 0;
        var price = parseFloat($(row).find('input[name$="-price"]').val()) || 0;
        var total = quantity * price;
        $(row).find('input[name$="-total"]').val(total.toFixed(2));
        return total;
    }

    function updateTotals() {
        var subtotal = 0;
        $('.dynamic-items').each(function() {
            subtotal += calculateLineTotal(this);
        });

        var taxRate = parseFloat($('#id_tax_rate').val()) || 15;
        var taxAmount = subtotal * (taxRate / 100);
        var total = subtotal + taxAmount;

        // Update readonly fields
        $('#id_subtotal').val(subtotal.toFixed(2));
        $('#id_tax_amount').val(taxAmount.toFixed(2));
        $('#id_total').val(total.toFixed(2));
    }

    // Calculate on input change
    $(document).on('input', '.calc-trigger', updateTotals);

    // Calculate on form load
    updateTotals();

    // Recalculate when new inline form is added
    $(document).on('formset:added', function() {
        updateTotals();
    });
});
