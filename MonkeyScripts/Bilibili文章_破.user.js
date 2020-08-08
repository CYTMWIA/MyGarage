// ==UserScript==
// @name         Bilibili文章_破
// @version      2020.8.8
// @description  解锁Bilibili文章的文字选中
// @author       CYTMWIA
// @match        http*://www.bilibili.com/read/cv*
// ==/UserScript==

(function() {
    'use strict';

    let article_elem = document.getElementsByClassName('article-holder')[0]
    article_elem.style['-moz-user-select'] = 'auto'
    article_elem.style['-webkit-user-select'] = 'auto'
    article_elem.style['user-select'] = 'auto'

})();