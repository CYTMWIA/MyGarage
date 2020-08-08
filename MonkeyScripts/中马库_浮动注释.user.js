// ==UserScript==
// @name         中马库_浮动注释
// @version      2020.8.4
// @description  浮动注释
// @author       CYTMWIA
// @match        https://www.marxists.org/chinese/*
// @require      https://code.jquery.com/jquery-3.5.1.min.js
// ==/UserScript==

(function() {
    'use strict';

    // 所有注释
    let NOTES = $('span')[0].innerText.match(/\[\d+\].*?($|\n\n)/g)
    for (let i=0;i<NOTES.length;i+=1)
        NOTES[i] = NOTES[i].trim()

    $('body')[0].innerHTML += '<div id="float_note" style="background-color: wheat;width: max-content;padding: 1ch; display: none; position: fixed; max-width: 33%;font-size: small;line-height: normal;"></div>'

    let BODY = $('body')[0]
    let FLOAT_NOTE = $('#float_note')[0]

    let as = $('a')
    for (let idx=0;idx<as.length;idx+=1){
        let ele = as[idx]
        if (ele.name.includes('_ftnref')) {
            ele.addEventListener('mouseenter',function(){
                let note_idx = parseInt(this.name.match(/\d+/g)[0])
                FLOAT_NOTE.innerText = NOTES[note_idx-1]

                FLOAT_NOTE.style.display = ''

                let fn_width = FLOAT_NOTE.offsetWidth
                let fn_height = FLOAT_NOTE.offsetHeight
                let ele_rect = this.getBoundingClientRect()
                // 距窗口顶部距离
                if (ele_rect.top + ele_rect.height + fn_height > window.innerHeight)
                    FLOAT_NOTE.style.top = (ele_rect.top - fn_height) + 'px'
                else
                    FLOAT_NOTE.style.top = (ele_rect.top + ele_rect.height) + 'px'
                // 距窗口左边距离
                if (ele_rect.left + fn_width > window.innerWidth)
                    FLOAT_NOTE.style.left = (ele_rect.left - fn_width + ele_rect.width) + 'px'
                else
                    FLOAT_NOTE.style.left = (ele_rect.left) + 'px'
            })
            ele.addEventListener('mouseout',function(){
                FLOAT_NOTE.style.display = 'none'
            })
        }
    }
})();