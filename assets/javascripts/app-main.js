/**
 * Created by elliotthall on 14/09/16.
 */
requirejs.config({
    //By default load any module IDs from js/lib
    //baseUrl: 'js/lib',
    //except, if the module ID starts with "app",
    //load it from the js/app directory. paths
    //config is relative to the baseUrl, and
    //never includes a ".js" extension since
    //the paths config could be for a directory.
    baseUrl: '/static/javascripts',
    paths: {
        'jQuery': '../vendor/jquery/dist/jquery',
        'easyautocomplete': '../vendor/EasyAutocomplete/dist/jquery.easy-autocomplete',
        vendor: '../vendor',
        'es6': '../vendor/requirejs-babel/es6',
        'babel': '../vendor/requirejs-babel/babel-5.8.34.min',

        // Foundation
        'foundation': '../vendor/foundation/js/foundation.min',
        'foundation.core': '../vendor/foundation-sites/js/foundation.core',
        'foundation.accordionMenu': '../vendor/foundation-sites/js/foundation.accordionMenu',
        'foundation.drilldown': '../vendor/foundation-sites/js/foundation.drilldown',
        'foundation.dropdown': '../vendor/foundation-sites/js/foundation.dropdown',
        'foundation.dropdownMenu': '../vendor/foundation-sites/js/foundation.dropdownMenu',
        'foundation.equalizer': '../vendor/foundation-sites/js/foundation.equalizer',
        'foundation.magellan': '../vendor/foundation-sites/js/foundation.magellan',
        'foundation.sticky': '../vendor/foundation-sites/js/foundation.sticky',
        'foundation.responsiveMenu': '../vendor/foundation-sites/js/foundation.responsiveMenu',
        'foundation.responsiveToggle': '../vendor/foundation-sites/js/foundation.responsiveToggle',
        'foundation.util.box': '../vendor/foundation-sites/js/foundation.util.box',
        'foundation.util.keyboard': '../vendor/foundation-sites/js/foundation.util.keyboard',
        'foundation.util.mediaQuery': '../vendor/foundation-sites/js/foundation.util.mediaQuery',
        'foundation.util.motion': '../vendor/foundation-sites/js/foundation.util.motion',
        'foundation.util.nest': '../vendor/foundation-sites/js/foundation.util.nest',
        'foundation.util.timerAndImageLoader': '../vendor/foundation-sites/js/foundation.util.timerAndImageLoader',
        'foundation.util.touch': '../vendor/foundation-sites/js/foundation.util.touch',
        'foundation.util.triggers': '../vendor/foundation-sites/js/foundation.util.triggers',
        'requirejs': '../vendor/requirejs/require'
    },
    shim: {
        "easyautocomplete": ["jQuery"],
        "foundation":["jQuery"],
        "foundation.sticky": ["jQuery","foundation","foundation.util.triggers"]
    }

});
// Main

/**
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
                match: {
                    enabled: true
                },
                sort: {
                    enabled: true
                },
                onChooseEvent: function () {
                    var sf=jQuery('input[name="selected_facets"]').val();
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
        self = element;
        this.setUp(element);
    }
}

require(["requirejs", "jQuery", "easyautocomplete","foundation"], function (jQuery, eAuto) {
    //This function is called when scripts/helper/util.js is loaded.
    //If util.js calls define(), then this function is not fired until
    //util's dependencies have loaded, and the util argument will hold
    //the module value for "helper/util".
    'use strict';

    $(document).ready(function () {
        $('input.autocomplete').each(function () {
            autocomplete.init(this);
        });

        $('button.showhide').click(function(){
            $('.search-box').slideToggle();
        });

        //$(document).foundation();

    });


});

