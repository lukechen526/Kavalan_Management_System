#Views for the front page goes here.
from stream.views import StreamIndexView

class IndexView(StreamIndexView):
    """
    The frontpage serves a Stream
    """
    template_name = 'index.html'
    
  