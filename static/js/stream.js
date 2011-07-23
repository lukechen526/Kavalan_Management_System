$(function(){


Backbone.emulateJSON = true;
window.StreamPost = Backbone.Model.extend({
        defaults: {content:'', link:'', groups:[]}
       
    });


window.StreamCollection = Backbone.Collection.extend({
    model: StreamPost,
    url: '/api/stream/'
});

window.Stream = new StreamCollection;


















});