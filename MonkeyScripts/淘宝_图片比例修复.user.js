// ==UserScript==
// @name         淘宝_图片比例修复
// @version      2020.7.19
// @description  淘宝图片比例修复
// @author       CYTMWIA
// @match        http*://item.taobao.com/item.htm*
// @require      https://code.jquery.com/jquery-3.5.1.min.js
// ==/UserScript==

(function() {
    'use strict';

    // Your code here...
    setInterval(function(){
        let eles = $('img')
        for (let i=0;i<eles.length;i+=1) {
            let ele = eles[i]

            if (ele.style['max-width']==='') continue

            let max_width = parseInt(ele.style['max-width'])
            let ori_width = parseInt(ele.getAttribute('width'))
            let ori_height = parseInt(ele.getAttribute('height'))

            if (ori_width>max_width) {
                let fit_height = ori_height*max_width/ori_width
                ele.width = max_width
                ele.height = fit_height
            }
        }
    }, 500)
})();