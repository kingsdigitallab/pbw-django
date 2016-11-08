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
        'jquery': '../vendor/jquery/dist/jquery',
        'easyautocomplete': '../vendor/EasyAutocomplete/dist/jquery.easy-autocomplete',

        'es6': '../vendor/requirejs-babel/es6',
        'babel': '../vendor/requirejs-babel/babel-5.8.34.min',

        // Foundation
        'foundation': '../vendor/foundation-sites/js/foundation.core',
        'foundation.accordionMenu': '../vendor/foundation-sites/js/foundation.accordionMenu',
        'foundation.drilldown': '../vendor/foundation-sites/js/foundation.drilldown',
        'foundation.dropdown': '../vendor/foundation-sites/js/foundation.dropdown',
        'foundation.dropdownMenu': '../vendor/foundation-sites/js/foundation.dropdownMenu',
        'foundation.equalizer': '../vendor/foundation-sites/js/foundation.equalizer',
        'foundation.responsiveMenu': '../vendor/foundation-sites/js/foundation.responsiveMenu',
        'foundation.responsiveToggle': '../vendor/foundation-sites/js/foundation.responsiveToggle',
        'foundation.sticky': '../vendor/foundation-sites/js/foundation.sticky',
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
        "easyautocomplete": ["jquery"],

        'foundation': {
            deps: [
                'jquery'
            ],
            exports: 'Foundation'
        },
        'foundation.util.box': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.keyboard': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.mediaQuery': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.motion': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.nest': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.timerAndImageLoader': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.touch': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.triggers': {
            deps: [
                'foundation'
            ],
        },
        'foundation.accordionMenu': {
            deps: [
                'foundation',
                'foundation.util.keyboard',
                'foundation.util.motion',
                'foundation.util.nest'
            ],
        },
        'foundation.drilldown': {
            deps: [
                'foundation',
                'foundation.util.keyboard',
                'foundation.util.motion',
                'foundation.util.nest'
            ],
        },
        'foundation.dropdown': {
            deps: [
                'foundation',
                'foundation.util.box',
                'foundation.util.keyboard',
                'foundation.util.triggers'
            ],
        },
        'foundation.dropdownMenu': {
            deps: [
                'foundation',
                'foundation.util.box',
                'foundation.util.keyboard',
                'foundation.util.nest'
            ],
        },
        'foundation.equalizer': {
            deps: [
                'foundation',
                'foundation.util.mediaQuery'
            ],
        },
        'foundation.responsiveMenu': {
            deps: [
                'foundation',
                'foundation.util.triggers',
                'foundation.util.mediaQuery',
                'foundation.accordionMenu',
                'foundation.drilldown',
                'foundation.dropdownMenu'
            ],
        },
        'foundation.responsiveToggle': {
            deps: [
                'foundation',
                'foundation.util.mediaQuery'
            ],
        },
        'foundation.sticky': {
            deps: [
                'foundation',
                'foundation.util.triggers',
                'foundation.util.mediaQuery'
            ],
        },
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
        self = element;
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

require(["requirejs", "jquery", "easyautocomplete","foundation", "foundation.accordion"], function (jQuery, eAuto) {
    //This function is called when scripts/helper/util.js is loaded.
    //If util.js calls define(), then this function is not fired until
    //util's dependencies have loaded, and the util argument will hold
    //the module value for "helper/util".
    'use strict';

    $(document).ready(function () {
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

        // Expand / Collapse

        $('.panel-head h4').bind("click", function() {
            $(this).parent().next('.panel-body').slideToggle(400).removeClass("hide");
            $("i", this).toggleClass("fa-caret-down fa-caret-right");
            return false;
        });

        $('.expander').bind("click", function() {
            $(this).next('.collapsible').slideToggle(400).removeClass("hide");
            $("i", this).toggleClass("fa-caret-down fa-caret-right");
            return false;
        });

        $('button.options').bind("click", function() {
            var txt = $(".search-box").is(':visible') ? 'Show' : 'Hide';
            $('.search-box').slideToggle(400);
            $('#showhide').text(txt);
            // toggle extra-margin class to remove blank space when collapsing
            // the search box
            $('#search-results-box').toggleClass("extra-margin");
            return false;
        });

        // Printing search results
        $('#printme').bind("click", function() {
            // TODO: remove pagination and show full list of results
            window.print();
        });

        $(document).foundation();

    });


});

