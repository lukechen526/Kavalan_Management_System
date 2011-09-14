from kavalan.settings import *
import os, sys

PIPELINE = True
PIPELINE_VERSION = True
PIPELINE_AUTO = DEBUG #Disable PIPLELINE auto-regeneration for production environment

STATICFILES_FINDERS = ('pipeline.finders.PipelineFinder',) + STATICFILES_FINDERS
MIDDLEWARE_CLASSES += ('pipeline.middleware.MinifyHTMLMiddleware',)
PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.closure.ClosureCompressor'

if sys.platform == 'win32' :
    PIPELINE_YUI_BINARY = os.path.join('C:\\yuicompressor')
    PIPELINE_CLOSURE_BINARY = os.path.join('C:\\closure')

PIPELINE_CSS = {
    'all': {
        'source_filenames': (
          'css/chosen.css',
          'css/custom-theme/jquery-ui-1.8.14.custom.css',
          'css/base.css',
          'stream/css/stream.css',
          'accounts/css/accounts.css',
          'doc_engine/css/doc-engine.css',
          'custom_notification/css/notification.css'
        ),
        'output_filename': 'css/all_compressed.r?.css',
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
        'output_filename': 'js/project_compressed.r?.js'
    }
}
