# vim: set fileencoding=utf-8
# Pavel Odvody <podvody@redhat.com>
#
# libdoug - DOcker Update Guard
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# 02111-1307 USA
from libdoug.values import *
from libdoug.utils import flag_gen

class ReferenceType(object):
	(NONE, CHILDOF, PARENTOF) = flag_gen(3)


class DependencyType(object):
	(NONE, IMAGE, CONTAINER) = flag_gen(3)


class GraphNode(object):
	def __init__(self, parent, tid, children=None):
		self.parent = parent
		self.id = tid
		self.children = children if children else {}

	def getid(self):
		return self.id

	def getparent(self):
		return self.parent

	def getchildren(self):
		return self.children.itervalues()

	def addchild(self, nid):
		if nid not in self.children:
			node = GraphNode(self, nid) 
			self.children[nid] = node
			return node
		else:
			raise Exception('We already have this kid :?')


class TreeState(object):
	def __init__(self):
		self.numpushes = 0
		self.links = []

	def pushbranch(self, link):
		self.numpushes += 1
		self.links.append(link)

	def popbranch(self):
		return self.links.pop()

	def peek(self):
		if not self.links:
			return False
		return self.links[-1]

	def formatlinks(self):
		links = [u'│' if l else u' ' for l in self.links]
		if links:
			return  u' ' + u''.join(links[:-1])
		return u''

	def _boolindex(self, b):
		return 0 if b else 1

	def formatline(self, img, isleaf):
		horizontals, verticals = [u'├', u'└'], [u'─', u'┬']
		vert, horiz = u'╺' if self.numpushes == 0 else \
			horizontals[self._boolindex(self.peek())], \
			verticals[self._boolindex(isleaf)]
		treedeco = self.formatlinks() + vert + horiz
		return treedeco + u'%s %s' % (img['Id'], 
			img['RepoTags'] if img['RepoTags'][0] != EmptyTag else '')
