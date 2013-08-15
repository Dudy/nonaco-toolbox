#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'wiki'))

import webapp2
import blog_frontpage
import wiki_main
import user_handling
import logging

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

#FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"
#logging.basicConfig(format=FORMAT)
#logging.Logger.setLevel(logging.DEBUG)

# notice: order matters when defining routes, first one that's fitting will route
# so place the "'/wiki' + PAGE_RE" route at the end as it will fit the _edit route too
app = webapp2.WSGIApplication([
    #('/', blog_frontpage.Handler_blog_frontpage),
#    ('/wiki/flush', wiki_main.Handler_wiki_flush),
    
    ('/wiki/signup', user_handling.Handler_wiki_signup),
    ('/wiki/login', user_handling.Handler_wiki_login),
    ('/wiki/logout', user_handling.Handler_wiki_logout),
    
    ('/wiki/_edit' + PAGE_RE, wiki_main.Handler_wiki_edit),
    ('/wiki/_history' + PAGE_RE, wiki_main.Handler_wiki_history),
    
    ('/', wiki_main.Handler_wiki_showpage),
    ('/wiki', wiki_main.Handler_wiki_showpage),
    ('/wiki' + PAGE_RE, wiki_main.Handler_wiki_showpage),
    
    ('/blog', blog_frontpage.Handler_blog_frontpage),
    ('/blog/flush', blog_frontpage.Handler_blog_flush),
    ('/blog/.json', blog_frontpage.Handler_blog_json),
    ('/blog.json', blog_frontpage.Handler_blog_json),
    (r'/blog/(\d+).json', blog_frontpage.Handler_blog_json),
    ('/blog/signup', user_handling.Handler_blog_signup),
    ('/blog/login', user_handling.Handler_blog_login),
    ('/blog/logout', user_handling.Handler_blog_logout),
    ('/blog/newpost', blog_frontpage.Handler_blog_newpost),
    (r'/blog/(\d+)', blog_frontpage.Handler_blog_permalink),
    ('/blog/welcome', user_handling.Handler_blog_welcome)
    ], debug=True)
