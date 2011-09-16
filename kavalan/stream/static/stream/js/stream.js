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
     this.url = '/api/stream/'+post_id+'/comments';
    }
});

//This is used as local storage for Stream comments to avoid having to fetch them again when the Stream refreshes
window.StreamComments = {};

window.CommentView = Backbone.View.extend({
    tagName: "div",
    template: _.template($('.stream .post-comment-template').html()),
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
        _.bindAll(this,'setCommentCollection', 'loadComments', 'updateCommentCount');
        var options = {};
        this.setCommentCollection(options);
    },

    validate: function(attrs){
        if(attrs.content == '' && attrs.link == ''){
            
            return 'Either content or link has to be non-empty.';
        }
    },

    setCommentCollection: function(options){
        if(this.has('id') && window.StreamComments[this.id] !== undefined){

            window.StreamComments[this.id].bind('add', this.updateCommentCount);
            window.StreamComments[this.id].bind('remove', this.updateCommentCount);
            window.StreamComments[this.id].bind('reset', this.updateCommentCount);

            this.set({comments: window.StreamComments[this.id]});
            this.get('comments').fetch(options);
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
            
            this.setCommentCollection(options);
        }
    },

    updateCommentCount: function(){
        this.set({comment_count: window.StreamComments[this.id].length}) ;
    }

});

window.PostView = Backbone.View.extend({

    tagName: "div",
    template: _.template($('.stream .post-template').html()),
    initialize: function(){
        this.model.view = this;
        _.bindAll(this,'loadComments','refreshComments', 'addOne', 'addOneAnimated', 'addAll','render');
        this.model.bind('change', this.render, this);
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

    refreshComments: function(){
        if(this.model.get('comments') !== undefined){
            this.model.loadComments({success: this.render, error:this.render});
        }
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
    url: '/api/stream',
    initialize: function(){
        _.bindAll(this, 'updateStream');
    },
    comparator: function(post){
        return post.get('rank');
    },

    resetParams: function(){
        this.url = '/api/stream';
    },

    setParams: function(offset, num_posts){
        this.url = '/api/stream?offset='+offset.toString()+'&num_posts='+num_posts.toString();},

    fetchNext: function(options){
        this.setParams(this.length, 10);
        this.fetch($({add: true}).extend(options));
        this.resetParams();

    },

    updateStream: function(options){
        this.setParams(0, this.length);
        this.fetch();
        this.resetParams();
    }
});

window.Stream = new StreamCollection;


window.StreamView = Backbone.View.extend({
    el: $('.stream'),
    events:{
        "click .post-button": "createNewPost",
        "click .load-more a": "loadMorePost"
    },
    initialize: function(){

        //Initialize the UI elements

        //The Post! button starts out disabled
        this.$('.post-button').addClass("ui-state-disabled").attr('disabled', 'disabled');

        //Toggles the Post! button based on whether or not text is present in new-post-content or new-post-link
        this.$('.new-post-content, .new-post-link').bind('keyup change', function(){
            $(this).parents('.stream').find('.post-button').addClass("ui-state-disabled").attr('disabled', 'disabled');
            $('.create-post-errors').hide().empty();
            
            //Re-enable the button if either content or link is non-empty
            if($(this).parents('.stream').find('.new-post-content').val() != '' ||$(this).parents('.stream').find('.new-post-link').val() != ''){
                $(this).parents('.stream').find('.post-button').removeAttr('disabled').removeClass('ui-state-disabled');
            }
        });

        //Binds functions
        _.bindAll(this, 'addOne', 'addOneAnimated', 'addAll', 'refresh');
        Stream.bind('reset', this.refresh);
        Stream.bind('error', this.showError);

        //Initializes the Stream collection
        Stream.fetch();

         //Refresh the stream every 60 seconds
        setInterval(Stream.updateStream, 60*1000);
    },
    createNewPost: function(e){
        e.preventDefault();
        var groups = window.get_selected_groups();

        //Validation
        $('.create-post-errors').hide().empty();
        if(groups == null || groups.length == 0){
           this.$('.create-post-errors').append(document.createTextNode(gettext('You must select at least one group to post to!'))).show();
            return 0;
        }

        //Create the post object
        var post = Stream.create({
            content: this.$('.new-post-content').val(),
            link: this.$('.new-post-link').val(),
            groups: groups
        });

        if(post){
            this.$('new-post-content').val('');
            this.$('.new-post-link').val('');
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
        this.$(".stream-posts").prepend(el);
        $(el).fadeIn(5000);
    },

    addOne: function(post, isNew){

        var view = new PostView({model:post});
        this.$(".stream-posts").prepend(view.render().el);// Lower-ranked posts will be at the bottom
    },

    addAll: function(){
        Stream.each(this.addOne);
    },
    
    refresh: function(){
        this.$('.stream-posts').empty();
        this.addAll();
    }


});

window.StreamApp = new StreamView;


});