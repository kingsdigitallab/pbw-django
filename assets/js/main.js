// Main
require([
    'requirejs',
    'jquery',
    'fn',
    'ga',
    'cookie',
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
        console.log(source);
        $("a:contains('" + source + "')").focus()
    }

    $(document).ready(function () {
        var gets = getQueryVars();
        if (gets["source"]) {
            focusOnSource(decodeURI(gets["source"]).replace("\"",""));
        }

        //Accordion Toggles for person detail
        $("#openAll").click(function (e) {
            e.preventDefault();
            if ($('a.accordion-title.async').length > 0){
                $('a.accordion-title.async').click();
            }else{
                $("ul.accordion").foundation('down', $(".accordion-content"));
            }


        });
        $("#closeAll").click(function (e) {
            e.preventDefault();
            $("ul.accordion").foundation('up', $(".accordion-content"));
        });

        //Async loads for very large numbers of factoids in person detail

        $('a.accordion-title.async').click(function (e) {
            e.preventDefault();
            var factoidTypeKey = $(this).data('factoidtype');
            var personid = $(this).data('personid');
            var title = this;
            if ($(title).data("load") == 1 &&factoidTypeKey > 0 && personid > 0) {
                $.get("/factoidgroup/" + personid + "/" + factoidTypeKey + "/", function (data) {
                    var ul = $(title).next().children('ul');
                    if (ul.length > 0) {
                        var content = ul[0];
                        $(content).html(data);
                        $(title).data("load",0);
                    }
                });
            }
        });

    });


});
