# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Roberto Alsina and others.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function, unicode_literals

import json
import os
import subprocess

from nikola import __version__
from nikola.plugin_categories import Command

GUARDFILE = """#!/usr/bin/env python
from livereload.task import Task

def f():
    os.system("nikola build")

for watch in {0}:
    Task.add(watch, f)
"""


class Auto(Command):
    """Start debugging console."""
    name = "auto"
    doc_purpose = "automatically detect site changes, rebuild and optionally refresh a browser"
    cmd_options = [
        {
            'name': 'browser',
            'short': 'b',
            'type': bool,
            'help': 'Start a web browser.',
            'default': False,
        }
    ]

    def _execute(self, options, args):
        """Start the watcher."""
        try:
            from livereload.task import Task
            from livereload.server import start
        except ImportError:
            print('To use the auto command, you need to install the '
                  '"livereload" package.')
            return

        # Create a Guardfile
        with open("Guardfile", "wb+") as guardfile:
            l = ["conf.py", "themes", "templates", self.site.config['GALLERY_PATH']]
            for item in self.site.config['post_pages']:
                l.append(os.path.dirname(item[0]))
            for item in self.site.config['FILES_FOLDERS']:
                l.append(os.path.dirname(item))
            guardfile.write(GUARDFILE.format(json.dumps(l)))

        out_folder = self.site.config['OUTPUT_FOLDER']

        os.chmod("Guardfile", 0o755)

        start(35729, out_folder, options and options.get('browser'))