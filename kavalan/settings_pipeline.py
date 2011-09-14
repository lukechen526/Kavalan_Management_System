from kavalan.settings import *
import os

DIRNAME = os.path.dirname(__file__)

PIPELINE = True
STATICFILES_FINDERS = ('pipeline.finders.PipelineFinder',) + STATICFILES_FINDERS
PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.closure.ClosureCompressor'
PIPELINE_YUI_BINARY = os.path.join('C:\\yuicompressor')
PIPELINE_CLOSURE_BINARY = os.path.join('C:\\closure')


PIPELINE_CSS = {
    'all': {
        'source_filenames': (
          'css/bootstrap-1.1.1.min.css',
          'css/chosen.css',
          'css/custom-theme/jquery-ui-1.8.14.custom.css',
          'css/base.css',
          'stream/css/stream.css',
          'accounts/css/accounts.css',
          'doc_engine/css/doc-engine.css',
          'custom_notification/css/notification.css'
        ),
        'output_filename': 'css/all_compressed.css',
    },

}


PIPELINE_JS = {

    'project': {
        'source_filenames': (
            'js/base.js',
            'custom_notification/js/notification.js',
            'doc_engine/js/doc-engine.js',
            'stream/js/stream.js'
        ),
        'output_filename': 'js/project_compressed.js'
    }
}
