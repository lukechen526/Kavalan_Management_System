from kavalan.settings import *
import os

DIRNAME = os.path.dirname(__file__)
PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'
PIPELINE = True
STATICFILES_FINDERS = ('pipeline.finders.PipelineFinder',) + STATICFILES_FINDERS
PIPELINE_YUI_BINARY = os.path.join('C:\\yuicompressor')

PIPELINE_CSS = {
    'all': {
        'source_filenames': (
          'css/bootstrap-1.1.1.min.css',
          'css/chosen.css',
          'css/custom-theme/jquery-ui-1.8.14.custom.css',
          'css/base.css',
        ),
        'output_filename': 'css/all_compressed.css',
    },
    # other CSS groups goes here
}

#PIPELINE_JS = {
#    'all': {
#        'source_filenames': (
#          'js/jquery-1.2.3.js',
#          'js/jquery-preload.js',
#          'js/jquery.pngFix.js',
#          'js/my_script.js',
#          'js/my_other_script.js'
#        ),
#        'output_filename': 'js/all_compressed.js',
#    }
#}
