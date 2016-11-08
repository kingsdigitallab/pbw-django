/**
 * Javsascript for the main Facet browser
 * Created by elliotthall on 08/11/16.
 */
define(['module',
        'jquery',
        'easyautocomplete'
    ], function (module, $) {
        'use strict';

        /**Autocomplete settings
     * Created by elliotthall on 13/09/16.
     * Nicked from Luis' js in DPRR
     */
    var autocomplete = {
        // options for the EasyAutocomplete API
        setUp: function (input) {
            var $input = $(input);
            var qs = $input.data("qs");
            var options = {
                //data: autocompleteDict[$input.attr("name")],
                url: function (search) {
                    if (search.length > 1) {
                        return "/autocomplete/" + (qs && qs.length > 0 ? "?" + qs + "&" : "?") + "facet=" + $input.attr('name') + "&search=" + search;
                    }
                },

                listLocation: "Results",
                getValue: "name",
                template: {
                    type: "custom",
                    method: function (value, item) {
                        return value + ' <span class="label radius">' + item.count + '</span>';
                    }
                },
                list: {

                    sort: {
                        enabled: true
                    },
                    onChooseEvent: function () {
                        var sf = jQuery('input[name="selected_facets"]').val();
                        $input.closest('form').submit();
                    },
                    match: {
                        enabled: true,
                        method: function (element, phrase) {
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

        init: function (element) {
            //self = element;
            this.setUp(element);
        }
    }


    //Quick helper function to grab query vars
    var getQueryVars = function () {
        var vars = [], hash;
        var q = document.URL.split('?')[1];
        if (q != undefined) {
            q = q.split('&');
            for (var i = 0; i < q.length; i++) {
                hash = q[i].split('=');
                vars.push(hash[0]);
                vars[hash[0]] = hash[1];
            }
        }
        return vars;
    }

    //Used in the Bibliography page when it is passed a source to focus on on load.
    var focusOnSource=function(source){
        $("a:contains('"+source+"')").focus()
    }

    $(document).ready(function() {
        $('input.autocomplete').each(function () {
            autocomplete.init(this);
        });

        $('button.showhide').click(function () {
            $('.search-box').slideToggle();
        });

        var gets=getQueryVars();
        if (gets["source"]){
            focusOnSource(gets["source"]);
        }
    });

    }
);

