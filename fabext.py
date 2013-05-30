'''
Copyright 2013 Wenjun Deng <wdeng@wdeng.info>

This file is part of Omega Tools.

Omega Tools is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Omega Tools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Omega Tools.  If not, see <http://www.gnu.org/licenses/>.


This file provides some classes to simply building of gnuplot plots and LaTeX
documents using fabricate <https://code.google.com/p/fabricate/>.
'''

__version__ = '2013-05-30 18:21:28-04:00'

import os
from fabricate import *

# make use of default_builder in fabricate
from fabricate import _set_default_builder
_set_default_builder()
from fabricate import default_builder

class FabGnuplot:
    '''Class for building gnuplot plots using fabricate. So far only supports
    mp terminal.
    
    Usage example:
    Suppose there are dir1/a.gp and dir2/b.gp to be built, use:

    from fabext import *
    list_fig = ['dir1/a', 'dir2/b']
    fg = FabGnuplot(list_fig)
    fg.build_mps() # use this line to build mps figures
    fg.build_eps() # use this line to build eps figures
    fg.build_pdf() # use this line to build pdf figures
    '''

    def __init__(self, list_fig):
        '''list_fig is a list of figure file names without extention,
        e.g., if dir1/a.gp and dir2/b.gp need to be built,
        use ['dir1/a', 'dir2/b'] as list_fig.'''
        self.list_fig = list_fig

    def gp2mp(self, filename):
        '''filename should have no .gp extension'''
        run('gnuplot_lmp', filename + '.gp')

    def mp2mps(self, filename):
        '''filename should have no .mp extension'''
        run('mpost_mps', filename + '.mp')

    def mps2eps(self, filename):
        '''filename should have no .mps extension'''
        run('mps2eps', filename + '.mps')
        
    def mps2pdf(self, filename):
        '''filename should have no .mps extension'''
        run('mptopdf_mps', filename + '.mps')

    def build_mps(self):
        '''Build mps figures'''
        for fig in self.list_fig:
            self.gp2mp(fig)
        after()
        for fig in self.list_fig:
            self.mp2mps(fig)

    def build_eps(self):
        '''Build eps figures'''
        self.build_mps()
        after()
        for fig in self.list_fig:
            self.mps2eps(fig)

    def build_pdf(self):
        '''Build pdf figures'''
        self.build_mps()
        after()
        for fig in self.list_fig:
            self.mps2pdf(fig)

    def clean(self):
        '''Remove temporary output files'''
        for fig in self.list_fig:
            for ext in ['.mp', '.mp~', '.mpx', '_mp.log', '.log']:
                try:
                    os.remove(fig + ext)
                except OSError, e:
                    default_builder.echo_delete(fig + ext, e)
                else:
                    default_builder.echo_delete(fig + ext)

    def cleanall(self):
        '''Remove all output files'''
        self.clean()
        for fig in self.list_fig:
            for ext in ['.mps', '.eps', '.pdf']:
                try:
                    os.remove(fig + ext)
                except OSError, e:
                    default_builder.echo_delete(fig + ext, e)
                else:
                    default_builder.echo_delete(fig + ext)


class FabLatex:
    '''Class for building LaTeX documents using fabricate. latexmk is needed.
    
    Usage example:
    Suppose there is main.tex to be built, use:

    from fabext import *
    fl = FabLatex(['main'])
    fl.build() # use this line to call latex to build dvi document
    fl.build_pdfdvi() # use this line to call latex then dvipdf to build pdf
    fl.build_pdf() # use this line to use pdflatex to build pdf document
    '''

    def __init__(self, list_tex):
        '''list_tex is a list of LaTeX file names without '.tex' extention,
        e.g., if main.tex needs to be built,
        use ['main'] as list_tex.'''
        self.list_tex = list_tex

    def _build(self, opt):
        for tex in self.list_tex:
            cmd = ('latexmk', ) + opt + (tex + '.tex', )
            run(*cmd)

    def build(self):
        self._build(())

    def build_pdfdvi(self):
        self._build(('-pdfdvi', ))

    def build_pdf(self):
        self._build(('-pdf', ))

    def clean(self):
        '''Remove temporary output files'''
        for tex in self.list_tex:
            for ext in ['.aux', '.bbl', '.blg', 'Notes.bib', '.out', \
                '.log', '.nav', '.snm', '.toc', '.fls', '.spl', \
                '.fdb_latexmk']:
                try:
                    os.remove(tex + ext)
                except OSError, e:
                    default_builder.echo_delete(tex + ext, e)
                else:
                    default_builder.echo_delete(tex + ext)

    def cleanall(self):
        '''Remove all output files'''
        self.clean()
        for tex in self.list_tex:
            for ext in ['.dvi', '.ps', '.pdf']:
                try:
                    os.remove(tex + ext)
                except OSError, e:
                    default_builder.echo_delete(tex + ext, e)
                else:
                    default_builder.echo_delete(tex + ext)

