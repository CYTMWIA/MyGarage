// ==UserScript==
// @name         添加网站域名到标题
// @version      2020.8.4
// @description  添加网站域名到标题, 便于Keepass等软件捕获
// @author       CYTMWIA
// @include      *
// ==/UserScript==

(function() {
    'use strict';

    setInterval(function(){
        if (!document.title.includes(window.location.host))
            document.title += ' - ' + window.location.host
    },500)

})();