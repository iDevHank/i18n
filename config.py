#!/usr/bin/env python3

# The format of your own localizable method.
# This is an example of '"string".localized'
SUFFIX = '.localized'
KEY = r'"(?:\\.|[^"\\])*"'
LOCALIZABLE_RE = r'%s%s' % (KEY, SUFFIX)

# Specify the path of localizable files in project.
LOCALIZABLE_FILE_PATH = ''
LOCALIZABLE_FILE_NAMES = ['Localizable']
LOCALIZABLE_FILE_TYPES = ['strings']

# File types of source file.
SEARCH_TYPES = ['swift', 'm', 'json']
SOURCE_FILE_EXCLUSIVE_PATHS = [
    'Assets.xcassets', 'Carthage', 'ThirdParty',
    'Pods', 'Media.xcassets', 'Framework', 'bin']
LOCALIZABLE_FILE_EXCLUSIVE_PATHS = ['Carthage', 'ThirdParty',
                                    'Pods', 'Framework', 'bin']

LOCALIZABLE_FORMAT_RE = r'"(?:\\.|[^"\\])*"\s*=\s*"(?:\\.|[^"\\])*";\n'
DEFAULT_TARGET_PATH = 'generated.strings'
