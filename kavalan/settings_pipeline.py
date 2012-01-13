from kavalan.settings import *
import os, sys

PIPELINE_VERSION = True
PIPELINE_AUTO = DEBUG #Disable PIPLELINE auto-regeneration for production environment

STATICFILES_FINDERS = ('pipeline.finders.PipelineFinder',) + STATICFILES_FINDERS
PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.closure.ClosureCompressor'

PIPELINE_COMPILERS = (
  'pipeline.compilers.less.LessCompiler',
)

if sys.platform == 'win32' :
    PIPELINE_YUI_BINARY = os.path.join('C:\\yuicompressor')
    PIPELINE_CLOSURE_BINARY = os.path.join('C:\\closure')

PIPELINE_CSS = {
    'all': {
        'source_filenames': (
          'css/chosen.css',
          'css/custom-theme/jquery-ui-1.8.14.custom.css',
          'css/base.css',
          'accounts/css/accounts.css',
          'doc_engine/css/doc-engine.css'
        ),
        'output_filename': 'css/all_compressed.r?.css',
    },


    'iphone':{
        'source_filenames':(
            'css/base-iphone.css'
        ,),
        'output_filename': 'css/phone_compressed.r?.css',
        'extra_context': {
            'media': 'all and (max-device-width: 480px)'
        }

    }

}

PIPELINE_JS = {
    'project': {
        'source_filenames': (
            'js/base.js',
            'doc_engine/js/doc-engine.js',
        ),
        'output_filename': 'js/project_compressed.r?.js'
    }
}
