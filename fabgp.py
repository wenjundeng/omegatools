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


This file provides a class FabGP for building gnuplot plots using
fabricate <https://code.google.com/p/fabricate/>.
'''

from fabricate import *

class FabGP:
    '''Class for building gnuplot plots using fabricate.
    
    Usage example:
    Suppose there are dir1/a.gp and dir2/b.gp to be built, use:

    from fabgp import *
    list_fig = ['dir1/a', 'dir2/b']
    fgp = FabGP(list_fig)
    fgp.build_mps() # use this line to build mps figures
    fgp.build_eps() # use this line to build eps figures
    fgp.build_pdf() # use this line to build pdf figures
    '''

    VERSION='2013-03-14 11:07:10-04:00'

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
            self.mp2mps(fig)

    def build_eps(self):
        '''Build eps figures'''
        self.build_mps()
        for fig in self.list_fig:
            self.mps2eps(fig)

    def build_pdf(self):
        '''Build pdf figures'''
        self.build_mps()
        for fig in self.list_fig:
            self.mps2pdf(fig)

