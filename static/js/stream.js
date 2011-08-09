$(function(){

//Prevents the browser (aka. IE) from caching the JSON response. 
$.ajaxSetup({ cache: false });

Backbone.emulateJSON = true;

window.StreamComment = Backbone.Model.extend({
    defaults: {content:''},
    validate: function(attrs){
        if(attrs.content =='')
            return 'The content must be non-empty.';
    }
});

window.StreamCommentCollection = Backbone.Collection.extend({
    model: StreamComment,
    setPostID: function(post_id){
     this.url = '/api/stream/'+post_id+'/comments/';
    }
});

//This is used as local storage for Stream comments to avoid having to fetch them again when the Stream refreshes
window.StreamComments = {};

window.CommentView = Backbone.View.extend({
    tagName: "div",
    template: _.template($('#post-comment-template').html()),
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

window.StreamPost = Backbone.Model.extend({
    defaults: {content:'', link:'', groups:[]},
    initialize: function(){
        _.bindAll(this,'refresh','setCommentCollection', 'loadComments');
        this.setCommentCollection();
    },

    refresh: function(){
        this.fetch();
    },
    validate: function(attrs){
        if(attrs.content == '' && attrs.link == ''){
            
            return 'Either content or link has to be non-empty.';
        }
    },

    setCommentCollection: function(){
        if(this.has('id') && window.StreamComments[this.id] !== undefined){
            this.set({comments: window.StreamComments[this.id]});
        }
        else{
            this.set({comments: undefined});
        }
    },
    
    loadComments: function(options){
        if(this.has('id')){
            //Check if a local collection of comments already exists. If not, create a new
             //StreamCommentCollection
             if(window.StreamComments[this.id] == undefined){
                    window.StreamComments[this.id] = new StreamCommentCollection;
                    window.StreamComments[this.id].setPostID(this.id);
             }
            
            this.setCommentCollection();
            window.StreamComments[this.id].fetch(options);
            window.StreamComments[this.id].bind('add', this.refresh);
            window.StreamComments[this.id].bind('remove', this.refresh);
        }
    }

});

window.PostView = Backbone.View.extend({

    tagName: "div",
    template: _.template($('#post-template').html()),
    initialize: function(){
        this.model.view = this;
        _.bindAll(this, 'loadComments','addOne', 'addOneAnimated', 'addAll','render');
        this.model.bind('change', this.render, this);
        //Reloads comments every 40 secs
        //setInterval(this.loadComments, 40*1000);
    },
    events: {
      "keydown .write-comment": "writeComment",
      "click .comment-count": "loadComments"
    },

    addOneAnimated: function(comment){
        var view = new CommentView({model:comment});
        el = view.render().el;
        $(el).css('display', 'none');
        this.$('.post-comments').append(el);
        $(el).fadeIn(3000);
    },
    addOne: function(comment){

        var view = new CommentView({model:comment});
        this.$(".post-comments").append(view.render().el);
    },
    addAll: function(){
        this.model.get('comments').each(this.addOne);
    },

    loadComments: function(){
      this.model.loadComments({success: this.render, error:this.render});
    },
    writeComment: function(e){
    //If Enter was pressed
        if(e.which == 13){
            //Create the comment object
            content = this.$('.write-comment').val();
            if(content !== ''){
                var comment = this.model.get('comments').create({
                    content: content
                });
                if(comment){
                    this.$('.write-comment').val('');
                    this.addOneAnimated(comment);
                }
            }
        }
    },
    render: function(){
        if(this.model.get('poster') !== undefined){
            $(this.el).html(this.template(this.model.toJSON()));

            //Load comments if they have been loaded
            if(this.model.has('comments') && this.model.get('comments') !== undefined){
                comment_list = $(this.el).find('.post-comments');
                comments = this.model.get('comments');
                comment_list.empty();
                var i = 0;
                while(i != comments.length){
                    view = new CommentView({model: comments.at(i)});
                    comment_list.append(view.render().el);
                    i++;
                }
                this.$('.comment-list').css('display', 'block');
            }
            return this;}
        
        else{
            return this;
        }
    }
});
window.StreamCollection = Backbone.Collection.extend({
    model: StreamPost,
    url: '/api/stream/',
    initialize: function(){
        _.bindAll(this, 'updateStream');
    },
    comparator: function(post){
        return post.get('rank');
    },
    setParams: function(offset, num_posts){
        this.url = '/api/stream/?offset='+offset.toString()+'&num_posts='+num_posts.toString();},

    fetchNext: function(options){
        this.setParams(this.length, 10);
        this.fetch($({add: true}).extend(options));
    },

    updateStream: function(options){
        this.setParams(0, this.length);
        this.fetch();
    }
});

window.Stream = new StreamCollection;


window.StreamView = Backbone.View.extend({
    el: $('#stream'),
    events:{
        "click #post-button": "createNewPost",
        "click #load-more a": "loadMorePost"
    },
    initialize: function(){
        _.bindAll(this, 'addOne', 'addOneAnimated', 'addAll', 'refresh');
        Stream.bind('reset', this.refresh);
        Stream.bind('error', this.showError);
        Stream.fetch();

         //Refresh the stream every 30 seconds
        //setInterval(Stream.updateStream, 30*1000);
    },
    createNewPost: function(e){
        e.preventDefault();
        var groups = $("#id_groups").multiselect("getChecked").map(function(){return this.value;}).get();

        //Validation
        $('#create-post-errors').empty();
        if(groups.length == 0){
            $('#create-post-errors').append(document.createTextNode(gettext('You must select at least one group to post to!')));
            return 0;
        }

        //Create the post object
        var post = Stream.create({
            content: this.$('#new-post-content').val(),
            link: this.$('#new-post-link').val(),
            groups: groups
        });

        if(post){
            this.$('#new-post-content').val('');
            this.$('#new-post-link').val('');
            post.setCommentCollection();
            this.addOneAnimated(post);
        }

    },

    loadMorePost: function(e){
        e.preventDefault();
        Stream.fetchNext({
            success:this.refresh,
            error: function(collection, response){console.log(response);}});
    },

    showError: function(model, error){
        console.log(error);
    },

    addOneAnimated: function(post){
        var view = new PostView({model:post});
        el = view.render().el;
        $(el).css('display', 'none');
        this.$("#stream-posts").prepend(el);
        $(el).fadeIn(5000);
    },

    addOne: function(post, isNew){

        var view = new PostView({model:post});
        this.$("#stream-posts").prepend(view.render().el);// Lower-ranked posts will be at the bottom
    },

    addAll: function(){
        Stream.each(this.addOne);
    },
    
    refresh: function(){
        $('#stream-posts').empty();
        this.addAll();
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