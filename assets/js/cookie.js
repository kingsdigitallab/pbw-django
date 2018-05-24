define([
    'module',
    'jquery',
    'jscookie'
], function(module, $, cookie) {
    'use strict';

    $(document).ready(function() {
        if (!cookie.get('pbw-cookie')) {
            $("#cookie-disclaimer").removeClass('hide');
        }
        // Set cookie
        $('#cookie-disclaimer .set-cookie').on("click", function() {
            cookie.set('pbw-cookie', 'pbw-cookie-set', { expires: 30 });
        });
    });

    return module;
});
