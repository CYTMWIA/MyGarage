// ==UserScript==
// @name         Fanatical_KeyDumper
// @version      2021.4.24.2
// @description  F站提取Key
// @author       CYTMWIA
// @match        *://www.fanatical.com
// @match        *://www.fanatical.com/*
// @require      https://cdn.jsdelivr.net/npm/vue@2.6.12
// @grant        GM_setClipboard
// ==/UserScript==

(function() {
    'use strict';

    function initHtml() {
        if (window.location.pathname.match(/.*?\/orders\/.+/)===null) return false
        
        let title_containers = document.getElementsByClassName('title-container')
        if (title_containers.length === 0) return false

        let root = document.getElementById('KeyDumper')
        if (root !== null) return false

        let title_container = title_containers[0]
        title_container.innerHTML += ''
            +'<div id="KeyDumper">'
            +'<div class="btn btn-primary" style="margin-right: 1ch;" v-on:click="unlockKeys()">一键刮Key ({{unlock_keys_count}}/{{total_keys_count}})</div>'
            +'<div class="btn btn-primary" style="margin-right: 1ch;" v-on:click="copyKeys()">复制已刮Key</div>'
            +'</div>'

        return true
    }

    function initVue() {
        let ui = new Vue({
            el:'#KeyDumper',
            data: {
                unlock_keys_count: 0,
                total_keys_count: 0
            },
            methods: {
                unlockKeys: function () {
                    let key_containers = document.getElementsByClassName('key-container')
                    for (let kc of key_containers) {
                        let btn = kc.getElementsByTagName('button')[0]
                        console.log(btn)
                        btn.click()
                    }
                },
                copyKeys: function () {
                    let order_containers = document.getElementsByClassName('order-item-details-container')
                    let res = ''
                    for (let oc of order_containers) {
                        console.log(oc)
                        let key_elems = oc.getElementsByTagName('input')
                        if (key_elems.length === 0) continue

                        let game_name = oc.getElementsByClassName('game-name')[0]

                        let str_game = game_name.innerText
                        let str_key = key_elems[0].value
                        res += str_game + ': ' + str_key + '\n'
                    }
                    GM_setClipboard(res, 'text/plain')
                }
            }
        })
        setInterval(()=>{
            ui.unlock_keys_count = document.getElementsByClassName('key-input-field').length
            ui.total_keys_count = document.getElementsByClassName('order-item-details-container').length
        }, 100)
        return ui
    }

    // main
    let interval_id = setInterval(()=>{
        if (initHtml()) {
            initVue()
        }
    }, 100)
})();
