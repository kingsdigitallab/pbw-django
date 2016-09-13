/**
 * Created by elliotthall on 13/09/16.
 * Nicked from Luis' js in DPRR
 */
var autocomplete = {
    // options for the EasyAutocomplete API
    setUp: function(input) {
        $input = $(input);

        options = {
            data: autocompleteDict[$input.attr("name")],
            getValue: "name",
            template: {
                type: "custom",
                method: function(value, item) {
                    return value + ' <span class="label radius">' + item.count + '</span>';
                }
            },
            list: {
                match: {
                    enabled: true
                },
                sort: {
                    enabled: true
                },
                onChooseEvent: function() {
                    $input.closest('form').submit();
                },
                match: {
                    enabled: true,
                    method: function(element, phrase) {
                        if (element.indexOf(phrase) === 0) {
                            return true;
                        } else {
                            return false;
                        }
                    }
                }
            },
            placeholder: $input.attr("name")
        };

        $input.easyAutocomplete(options);
    },

    init: function() {
        self = this;
        $('input.autocomplete').each(function() {
            self.setUp(this);
        })
    }
}

$(document).ready(function() {
    autocomplete.init();
});