'''
Copyright (C) <2012> <Olav Groenaas Gjerde>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Created on Dec 8, 2012

@Author: Olav Groenaas Gjerde
'''

class Config(object):
    '''
    Default config for application
    '''

    DEBUG = False
    TESTING = False
    HOST = u"0.0.0.0"
    PORT = 18080
    PROTOCOL = u'http'
    LOGFILE = u'debug.log'
    AUTH_TOKEN = u'test123456'
    DBFILE = u'bb_filechunk.db'
    
    @staticmethod
    def set_app_password(password):
        ''' Set new application password'''
        Config.APPPW = password
        
    @staticmethod
    def set_zfs_path(path):
        ''' Set new path to ZFS binary'''
        Config.ZFS = path

class ProductionConfig(Config):
    '''
    Production config
    '''

    LOGFILE = 'production.log'
    PORT = 443
    PROTOCOL = u'https'
    
    @staticmethod
    def set_app_password(password):
        ''' Set new application password'''
        ProductionConfig.APPPW = password
        
    @staticmethod
    def set_zfs_path(path):
        ''' Set new path to ZFS binary'''
        ProductionConfig.ZFS = path

class DevelopmentConfig(Config):
    '''
    Development config
    '''
    DEBUG = True
    LOGFILE = u'debug.log'
    
    @staticmethod
    def set_app_password(password):
        ''' Set new application password'''
        DevelopmentConfig.APPPW = password
        
    @staticmethod
    def set_zfs_path(path):
        ''' Set new path to ZFS binary'''
        DevelopmentConfig.ZFS = path

class TestingConfig(Config):
    '''
    Test config
    '''

    TESTING = True
    LOGFILE = u'test.log'
    
    @staticmethod
    def set_app_password(password):
        ''' Set new application password'''
        TestingConfig.APPPW = password
        
    @staticmethod
    def set_zfs_path(path):
        ''' Set new path to ZFS binary'''
        TestingConfig.ZFS = path
    
