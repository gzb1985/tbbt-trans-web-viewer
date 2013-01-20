jQuery(function( $ ) {
    'use strict';

    var Utils = {
    };

    var App = {
        init: function() {
            this.trans = [];
            this.shortSceneTitleLen = 6;
            this.sceneTmplName = 'sceneTmpl';
            this.speechRowTmplName = 'speechRowTmpl';
            this.sceneListTmplName = 'sceneListTmpl';
            this.default_avatars = ['Sheldon', 'Leonard', 'Howard', 'Raj', 
                'Penny', 'Amy', 'Bernadette', 'Stuart', 'Noavatar'];
            this.cacheElements();
            this.bindEvents();
            this.fetchTrans();
            this.render();
        },
        cacheElements: function() {
            this.$scene = $('#scene');
            this.$sceneList = $('#sceneList');
            this.$loading = $('#loading');
            $.template(this.sceneTmplName, $('#scene-tmpl')[0].innerHTML);//$('#scene-tmpl').text() not work in ie8 browser, use $('#scene-tmpl')[0].innerHTML instead.
            $.template(this.speechRowTmplName, $('#speech-tmpl')[0].innerHTML);
            $.template(this.sceneListTmplName, $('#scene-affix-tmpl')[0].innerHTML);
            // side bar
            $('.scene-select-sidenav').affix({
              offset: {
                top: function () { return $(window).width() <= 980 ? 290 : 230 }, 
                bottom: 230
              }
            });
        },
        bindEvents: function() {
        },
        fetchTrans: function() {
            $.ajax({
                // ie ajax support
                xhr:  (window.ActiveXObject) ?
                function() {
                    try {
                        return new window.ActiveXObject("Microsoft.XMLHTTP");
                    } catch(e) {}
                } :
                function() {
                    return new window.XMLHttpRequest();
                },
                url: '/trans/' + season.toString() + '/' + episode.toString(),
                type: "GET",
                dataType: "json",
                success: this.fetchTransResult
            });
        },
        fetchTransResult: function(obj, textStatus, xhr) {
            xhr = null;
            if (obj.status && obj.status === 'success') {
                if (obj.trans.hasOwnProperty('scenes')) {
                    App.trans = obj.trans.scenes;
                } else {
                    App.trans = obj.trans;
                }
                App.render();
            }
        },
        renderTrans: function() {
            this.$scene.empty();
            this.$sceneList.empty();
            for (var i = 0; i < this.trans.length; i++) {
                this.renderScene(i);
                this.renderSceneList(i);
            };
            if (this.trans.length > 0) {
                this.$loading.hide();
            }
        },
        prepareSectionId: function(){
            var buf = [];
            for (var i = 0; i < this.trans.length; i++) {
                var sectionid = this.sectionId(this.trans[i].scene);
                var times = this.counteStr(buf, sectionid);
                if (times === 0) {
                    this.trans[i]['sectionid'] = sectionid;
                } else {
                    this.trans[i]['sectionid'] = sectionid + '-' + (times).toString();
                }
                buf.push(sectionid);
            }
        },
        counteStr: function(buf, str) {
            var count = 0;
            for (var i = 0; i < buf.length; i++) {
                if (str === buf[i]){
                    count += 1;
                }
            }
            return count;
        },
        shortScene: function(scene) {
            var shortScene = scene;
            var words = shortScene.split(' ');
            if (words.length > this.shortSceneTitleLen) {
                var shortwords = []
                for (var i = 0; i < this.shortSceneTitleLen; i++) {
                    shortwords.push(words[i]);
                }
                shortwords[shortwords.length-1] += '...';
                shortScene = shortwords.join(' ');
            }
            return shortScene;
        },
        sectionId: function(scene){
            var id = this.shortScene(scene);
            return id.split(',').join('').split('.').join('').split('(').join('').split(')').join('')
                        .split('\'').join('-').split(' ').join('-');
        },
        renderSceneList: function(idx) {
            var speeches = this.trans[idx].speeches;
            $.tmpl(this.sceneListTmplName, {
                href: this.trans[idx]['sectionid'], 
                scene: this.shortScene(this.trans[idx].scene)
            }, this.trans[idx]).appendTo(this.$sceneList);
        },
        renderScene: function(idx) {
            var orientIdx = 0;
            var colorIdx = 0;
            var orient = ['left', 'right'];
            var color = ['gray', 'red', 'blue', 'green'];

            var $section = $('<section/>', {
                id: this.trans[idx]['sectionid']
            });
            $section.appendTo(this.$scene);
            var $ul = $('<ul/>');
            $ul.appendTo($section);

            var speeches = this.trans[idx].speeches;
            $.tmpl(this.sceneTmplName, this.trans[idx]).appendTo($ul);
            for (var j = 0; j < speeches.length; j++) {
                if (!this.isDefaultAvatar(speeches[j].figure))
                    speeches[j].figure = 'Noavatar';
                $.tmpl(this.speechRowTmplName, {
                    speech: speeches[j], 
                    orient: orient[orientIdx], 
                    color: color[colorIdx]
                }).appendTo($ul);
                orientIdx = 1 - orientIdx;
                colorIdx = (colorIdx === 3)? 0 : colorIdx + 1;
            }
        },
        isDefaultAvatar: function(elem) {
            for (var i = 0; i < this.default_avatars.length; i++) {
                if (this.default_avatars[i] === elem)
                    return true;
            }
            return false;
        },
        render: function() {
            this.prepareSectionId();
            this.renderTrans();
        }
    };

    App.init();

});