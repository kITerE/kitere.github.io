"""Tree-view for 'wt' debugger command results"""

import re
import os
import fnmatch

from PySide import QtCore, QtGui

# -----------------------------------------------------------------------------

class WtResEntry:
  """One wt-result parsed string"""

  rePattern = "[ ]*([0-9]*)[ ]+([0-9]*)[ ]+\[[ ]*([0-9]*)\][ ]+(.*)"

  def __init__(self, mObj):
    self.instrExec = int( mObj.group(1) )
    self.instrChild = int( mObj.group(2) )
    self.level = int( mObj.group(3) )
    self.funcName = mObj.group(4)

# -----------------------------------------------------------------------------

def parseWtResStrings(strings):
  """Parse debugger log strings"""
  wtResList = list()

  for line in strings:
    mObj = re.search( WtResEntry.rePattern, line.strip("\r\n") )
    if mObj:
      wtResList.append( WtResEntry(mObj) )

  return wtResList

# -----------------------------------------------------------------------------

class WtSearchContext:
  """Find context in wt results"""
  def __init__(self, funcMask):
    self.ind = 0
    self.funcMask = funcMask

  def match(self, funcName):
    return fnmatch.fnmatch( funcName.lower(), self.funcMask.lower() )

# -----------------------------------------------------------------------------

class WtSearchListItem:
  """Search list entry"""
  def __init__(self, item):
    self.item = item
    self.funcName = ""

  def setFuncName(self, funcName):
    """Set function name"""
    self.funcName = funcName

# -----------------------------------------------------------------------------

class WtResWindow(QtGui.QMainWindow):
  """Window with results tree"""

  def __init__(self):
    super(WtResWindow, self).__init__()

    # prepare tree widget
    self.treeWidget = QtGui.QTreeWidget()
    self.treeWidget.header().setResizeMode( QtGui.QHeaderView.Interactive )
    self.treeWidget.setHeaderLabels( ("Instructions count (executed:child)",
                                      "Fuction name") )
    self.setCentralWidget( self.treeWidget )

    self.treeWidget.currentItemChanged.connect(self.treeItemChanged)

    self.clearTree()

    # create commands
    self.actFileOpen = QtGui.QAction( "&Open...", 
                                      self, 
                                      shortcut = "Ctrl+O",
                                      triggered = self.openFile)

    self.actFileExit = QtGui.QAction( "E&xit", 
                                      self, 
                                      shortcut = "Ctrl+X",
                                      triggered = self.close)

    self.actViewExpandAll = QtGui.QAction( "Exp&and all",
                                           self, 
                                           shortcut = "Ctrl+A",
                                           triggered = self.expandAll)

    self.actViewCollapsAll = QtGui.QAction( "Co&llaps all",
                                            self, 
                                            shortcut = "Ctrl+L",
                                            triggered = self.collapsAll)

    self.actViewExpandSelected = QtGui.QAction( "&Expand selected",
                                                self, 
                                                shortcut = "Ctrl+E",
                                                triggered = self.expandSelected)

    self.actViewCollapsSelected = QtGui.QAction( "Collap&s selected",
                                                 self, 
                                                 shortcut = "Ctrl+S",
                                                 triggered = self.collapsSelected)

    self.actViewFind = QtGui.QAction( "&Find...",
                                      self, 
                                      shortcut = "Ctrl+F",
                                      triggered = self.findByFuncName)

    self.actViewFindNext = QtGui.QAction( "Find next",
                                          self, 
                                          shortcut = "Ctrl+N",
                                          triggered = self.findNextByFuncName)

    # create menu
    self.menuFile = self.menuBar().addMenu("&File")
    self.menuFile.addAction( self.actFileOpen )
    self.menuFile.addAction( self.actFileExit )

    self.menuView = self.menuBar().addMenu("&View")
    self.menuView.addAction( self.actViewExpandAll )
    self.menuView.addAction( self.actViewCollapsAll )
    self.menuView.addSeparator()
    self.menuView.addAction( self.actViewExpandSelected )
    self.menuView.addAction( self.actViewCollapsSelected )
    self.menuView.addSeparator()
    self.menuView.addAction( self.actViewFind )
    self.menuView.addAction( self.actViewFindNext )

    self.statusBar().showMessage("Ready")

    self.setWindowTitle("wt-command results")
    self.resize(600, 400)

  def clearTree(self):
    """Clear all tree items"""
    self.root = None
    self.searchList = None
    self.searchContext = None
    self.treeWidget.clear()

  def setExpandedRecursive(self, item, expand):
    """Recursive expand/collps item and all child"""
    item.setExpanded(expand)
    for i in range(0, item.childCount()):
      self.setExpandedRecursive( item.child(i), expand )

  def expandAll(self):
    """Expand all tree items"""
    if self.root is None:
      return
    self.setExpandedRecursive(self.root, True)

  def expandSelected(self):
    """Expand selected tree items"""
    for item in self.treeWidget.selectedItems():
      self.setExpandedRecursive(item, True)

  def collapsAll(self):
    """Collapse all tree items"""
    if self.root is None:
      return
    self.setExpandedRecursive(self.root, False)

  def collapsSelected(self):
    """Collapse selected tree items"""
    for item in self.treeWidget.selectedItems():
      self.setExpandedRecursive(item, False)

  def findByFuncName(self):
    """Find first function by name mask"""
    if not self.searchList:
      return

    funcMask, ok = QtGui.QInputDialog.getText( self,
                                               "Find from selected", 
                                               "Function name (can use '*' and '?'):",
                                               QtGui.QLineEdit.Normal)
    if not ok:
      return

    self.searchContext = WtSearchContext(funcMask)
    if self.searchContext.match( self.searchList[0].funcName ):
      self.treeWidget.setCurrentItem( self.searchList[0].item )
      return

    return self.findNextByFuncName()

  def findNextByFuncName(self):
    """Find next function by name mask"""
    if not self.searchContext:
      return

    # search by searchList
    for i in range( self.searchContext.ind + 1, len(self.searchList) ):
      if self.searchContext.match( self.searchList[i].funcName ):
        self.treeWidget.setCurrentItem( self.searchList[i].item )

        # save find position
        self.searchContext.ind = i
        return

    # not found
    self.searchContext = None
    self.statusBar().showMessage(funcName + " not found...", 5000)

  def openFile(self):
    """View open file dialog and parse file content"""
    fileName = QtGui.QFileDialog.getOpenFileName( self,
                                                  "Open debugger log file",
                                                  QtCore.QDir.currentPath(),
                                                  "All files (*.*)")[0]
    if not fileName:
      return

    return self.parseFile( fileName )

  def parseFile(self, fileName):
    """Open and parse file content"""
    try:
      wtResList = parseWtResStrings( open(fileName, "r") )
    except IOError as (errno, strerror):
      self.clearTree()
      self.statusBar().showMessage("Read file data failed: " + strerror)
      return

    return self.parseResult(wtResList)

  def parseResult(self, wtResList):
    """Parse results and build tree"""
    self.clearTree()

    if not wtResList:
      self.statusBar().showMessage("Input does not contain the results of the command 'wt'")
      return

    # build tree
    self.searchList = list()
    self.root = self.createChilds( self.treeWidget, wtResList, 0 )
    self.treeWidget.addTopLevelItem( self.root )

    self.statusBar().showMessage("Data has been successfully parsed")

  def createChilds(self, parent, wtResList, startInRes):
    """Recursive tree building"""
    curLevel = wtResList[startInRes].level

    item = QtGui.QTreeWidgetItem(parent)
    item.setExpanded( curLevel == 0 )

    indexInSearch = len(self.searchList)
    self.searchList.append( WtSearchListItem(item) )

    wasCall = False
    funcName = ""

    for i in range(startInRes, len(wtResList)):
      level = wtResList[i].level
      if level < curLevel:
        break

      if level > curLevel:
        if (not wasCall) and ( (level - curLevel) == 1 ):
          wasCall = True
          self.createChilds( item, wtResList, i )
      else:
        wasCall = False
        # view only last: rewrite item data
        item.setData( 0,
                      QtCore.Qt.DisplayRole, 
                      str(wtResList[i].instrExec) + ":" + str(wtResList[i].instrChild) )

        funcName = wtResList[i].funcName
        item.setData( 1,
                      QtCore.Qt.DisplayRole,
                      ("  " * curLevel) + funcName )

    self.searchList[indexInSearch].setFuncName(funcName)

    return item

  def treeItemChanged(self, current, previous):
    """Current item changed notify: set status bar"""

    item = current
    callStr = ""
    while item:
      if len(callStr):
        callStr = item.data(1, QtCore.Qt.DisplayRole).lstrip() + "\\" + callStr
      else:
        callStr = item.data(1, QtCore.Qt.DisplayRole).lstrip()
      item = item.parent()

    self.statusBar().showMessage( callStr )

# -----------------------------------------------------------------------------

if __name__ == "__main__":
  import sys
  app = QtGui.QApplication(sys.argv)

  wndWtRes = WtResWindow()
  wndWtRes.show()

  if len(sys.argv) == 2:
    wndWtRes.parseFile( sys.argv[1] )
  else:
    wndWtRes.openFile()

  app.exec_()

# -----------------------------------------------------------------------------
