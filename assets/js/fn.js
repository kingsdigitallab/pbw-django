define([
    'module',
    'jquery',
    'es6!foundation',
    'es6!foundation.accordionMenu',
    'es6!foundation.drilldown',
    'es6!foundation.dropdown',
    'es6!foundation.dropdownMenu',
    'es6!foundation.equalizer',
    'es6!foundation.responsiveMenu',
    'es6!foundation.responsiveToggle',
    'es6!foundation.sticky',
    'es6!foundation.util.box',
    'es6!foundation.util.keyboard',
    'es6!foundation.util.mediaQuery',
    'es6!foundation.util.motion',
    'es6!foundation.util.nest',
    'es6!foundation.util.timerAndImageLoader',
    'es6!foundation.util.touch',
    'es6!foundation.util.triggers',
    'es6!foundation.accordion'
], function(module, $) {
    'use strict';

    $(document).ready(function() {

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
        
        // loads foundation
        $(document).foundation();

        //Ajax events for person accordion
        $('[data-accordion]').on('down.zf.accordion', function(event) {
            //If placeholder visible
                //Load group
                    //Hide placeholder
                    //Add html
            console.log(event.target+'opened!');
        });

       
    });

    return module;
});
