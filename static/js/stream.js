$(function(){

Backbone.emulateJSON = true;
window.StreamPost = Backbone.Model.extend({
    defaults: {content:'', link:'', groups:[]},
    validate: function(attrs){
        if(attrs.content == '' && attrs.link == ''){
            
            return 'Either content or link has to be non-empty';
        }
    }

});

window.StreamCollection = Backbone.Collection.extend({
    model: StreamPost,
    url: '/api/stream/',
    comparator: function(post){
        return post.get('rank');
    },
    setOffset: function(offset){this.url = '/api/stream/?offset='+offset.toString();},
    fetchNext: function(options){
        this.setOffset(this.length);
        this.fetch($({add: true}).extend(options));
    }
});

window.Stream = new StreamCollection;

window.PostView = Backbone.View.extend({

    tagName: "div",
    template: _.template($('#post-template').html()),
    initialize: function(){
        this.model.view = this;
        _.bindAll(this, 'render');
        this.model.bind('change', this.render);
    },

    render: function(){
        if(this.model.get('poster') !== undefined){
            $(this.el).html(this.template(this.model.toJSON()));
            return this;}
        else{
            return this;
        }
    }
});


window.StreamView = Backbone.View.extend({
    el: $('#stream'),
    events:{
        "click #post-button": "createNewPost"
    },
    initialize: function(){
        _.bindAll(this, 'addOne', 'addAll', 'refresh');
        Stream.bind('reset', this.refresh);
        Stream.bind('error', this.showError);
        Stream.fetch();
    },

    createNewPost: function(e){
        e.preventDefault();
        var groups = $("#id_groups").multiselect("getChecked").map(function(){return this.value;}).get();
        var post = Stream.create({
            content: this.$('#new-post-content').val(),
            link: this.$('#new-post-link').val(),
            groups: groups
        });

        if(post){
            this.addOne(post);
        }

    },

    showError: function(model, error){
        console.log(error);
    },

    addOne: function(post){

        var view = new PostView({model:post});
        this.$("#stream-posts").prepend(view.render().el);// Lower-ranked posts will be at the bottom
    },

    addAll: function(){
        Stream.each(this.addOne);
    },
    
    refresh: function(){
        $('#stream-posts').empty();
        this.addAll();
    },

    loadMore: function(){
        Stream.fetchNext({
            success:this.refresh,
            error: function(collection, response){console.log(response);}
        });
    }

});

window.StreamApp = new StreamView;

$('#id_groups').multiselect({
    noneSelectedText: gettext('Post to which groups?'),
    checkAllText: gettext('Select all groups'),
    uncheckAllText: gettext('Unselect all groups'),
    selectedText: gettext('# groups selected')
});

//The Post! button starts out disabled
$('#post-button').addClass("ui-state-disabled").attr('disabled', 'disabled');
    
$('#new-post-content, #new-post-link').bind('keyup change', function(){
    $('#post-button').addClass("ui-state-disabled").attr('disabled', 'disabled');

    //Re-enable the button if either content or link is non-empty
    if($('#new-post-content').val() != '' || $('#new-post-link').val() != ''){
        $('#post-button').removeAttr('disabled').removeClass('ui-state-disabled');
    }
})


});