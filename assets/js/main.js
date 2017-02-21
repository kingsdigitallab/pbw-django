// Main
require([
    'requirejs',
    'jquery',
    'clipboard',
    'fn',
    'ga',
    'easyautocomplete',
    'browse'
], function (r, $) {
    'use strict';

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
    var focusOnSource = function (source) {
        $("a:contains('" + source + "')").focus()
    }

    $(document).ready(function () {
        var gets = getQueryVars();
        if (gets["source"]) {
            focusOnSource(gets["source"]);
        }

        //Accordion Toggles for person detail
         $("#openAll").click( function(e) {
            e.preventDefault();
            $("ul.accordion").foundation('down',$(".accordion-content"));
        });
        $("#closeAll").click( function(e) {
            e.preventDefault();
            $("ul.accordion").foundation('up',$(".accordion-content"));
        });



    });
});
