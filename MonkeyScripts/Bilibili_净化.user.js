// ==UserScript==
// @name         Bilibili_净化
// @version      2020.8.8
// @description  清理 Bilibili 中的推广及广告
// @author       CYTMWIA
// @match        https://www.bilibili.com/*
// @match        https://www.bilibili.com/?*
// @require      https://code.jquery.com/jquery-3.4.1.min.js
// @run-at       document-body
// ==/UserScript==

(function() {
    'use strict';

    setInterval(function(){
        // 首页头部的 banner
        $('.bili-banner').css('background-image','none');

        // 广告
        $('.first-screen').css('display', 'none');
        $('.banner-card.b-wrap').css('display', 'none');
        $('#bannerAd').css('display','none');
        $('#slide_ad').css('display','none');
    },100)
})();