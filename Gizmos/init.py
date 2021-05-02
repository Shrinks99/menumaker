import os
import re

#If for whatever reason the toolset doesn't load and you want to hardcode the path instead comment out line 6, uncomment line 5, and change USERNAME to your username.  This path doesn't work on MacOS.
#CUSTOM_GIZMO_LOCATION = r'C:\Users\USERNAME\.nuke\Gizmos'
CUSTOM_GIZMO_LOCATION = os.path.dirname(os.path.realpath(__file__))

import nuke

class GizmoPathManager(object):
    def __init__(self, exclude=r'^\.', searchPaths=None):
        '''Used to add folders within the gizmo folder(s) to the gizmo path
        
        exclude: a regular expression for folders / gizmos which should NOT be
            added; by default, excludes files / folders that begin with a '.'
            
        searchPaths: a list of paths to recursively search; if not given, it
            will use the NUKE_GIZMO_PATH environment variable; if that is
            not defined, it will use the directory in which this file resides;
            and if it cannot detect that, it will use the pluginPath 
        '''
        if isinstance(exclude, str):
            exclude = re.compile(exclude)
        self.exclude = exclude
        if searchPaths is None:
            searchPaths = os.environ.get('NUKE_GIZMO_PATH', '').split(os.pathsep)
            if not searchPaths:
                import inspect
                thisFile = inspect.getsourcefile(lambda: None)
                if thisFile:
                    searchPaths = [os.path.dirname(os.path.abspath(thisFile))]
                else:
                    searchPaths = list(nuke.pluginPath())
        self.searchPaths = searchPaths
        self.reset()
        
    @classmethod
    def canonical_path(cls, path):
        return os.path.normcase(os.path.normpath(os.path.realpath(os.path.abspath(path))))
        
    def reset(self):
        self._crawlData = {}
        
    def addGizmoPaths(self):
        '''Recursively search searchPaths for folders to add to the nuke
        pluginPath.
        '''
        self.reset()
        self._visited = set()
        for gizPath in self.searchPaths:
            self._recursiveAddGizmoPaths(gizPath, self._crawlData,
                                         foldersOnly=True)
            
    def _recursiveAddGizmoPaths(self, folder, crawlData, foldersOnly=False):
        # If we're in GUI mode, also store away data in _crawlDatato to be used
        # later by addGizmoMenuItems
        if not os.path.isdir(folder):
            return
        
        if nuke.GUI:
            if 'files' not in crawlData:
                crawlData['gizmos'] = []
            if 'dirs' not in crawlData:
                crawlData['dirs'] = {}

        # avoid an infinite loop due to symlinks...
        canonical_path = self.canonical_path(folder)
        if canonical_path in self._visited:
            return
        self._visited.add(canonical_path)
        
        for subItem in sorted(os.listdir(canonical_path)):
            if self.exclude and self.exclude.search(subItem):
                continue
            subPath = os.path.join(canonical_path, subItem)
            if os.path.isdir(subPath):
                nuke.pluginAppendPath(subPath)
                subData = {}
                if nuke.GUI:
                    crawlData['dirs'][subItem] = subData
                self._recursiveAddGizmoPaths(subPath, subData)
            elif nuke.GUI and (not foldersOnly) and os.path.isfile(subPath):
                name, ext = os.path.splitext(subItem)
                #if ext == '.gizmo' or ext =='.nk':
                #    crawlData['gizmos'].append(name)
                if ext == '.gizmo':
                    crawlData['gizmos'].append(name)
                if ext == '.nk':
                    crawlData['gizmos'].append(name + '.nk')
                    
    def addGizmoMenuItems(self, toolbar=None, defaultTopMenu=None):
        '''Recursively create menu items for gizmos found on the searchPaths.
        
        Only call this if you're in nuke GUI mode! (ie, from inside menu.py)
        
        toolbar - the toolbar to which to add the menus; defaults to 'Nodes'
        defaultTopMenu - if you do not wish to create new 'top level' menu items,
            then top-level directories for which there is not already a top-level
            menu will be added to this menu instead (which must already exist)
        '''        
        if not self._crawlData:
            self.addGizmoPaths()
            
        if toolbar is None:
            toolbar = nuke.menu("Nodes")
        elif isinstance(toolbar, str):
            toolbar = nuke.menu(toolbar)
        self._recursiveAddGizmoMenuItems(toolbar, self._crawlData,
                                         defaultSubMenu=defaultTopMenu,
                                         topLevel=True)
    
    def _recursiveAddGizmoMenuItems(self, toolbar, crawlData,
                                    defaultSubMenu=None, topLevel=False):
        for name in crawlData.get('gizmos', ()):
            niceName = name
            if name.endswith(".nk"):
                niceName = name[:-3]
            if niceName.find('_v')==len(name) - 4:
                niceName = name[:-4]
            toolbar.addCommand(niceName,"nuke.createNode('%s')" % name)
            
        for folder, data in list(crawlData.get('dirs', {}).items()):
            import sys
            subMenu = toolbar.findItem(folder)
            if subMenu is None:
                if defaultSubMenu:
                    subMenu = toolbar.findItem(defaultSubMenu)
                else:
                    subMenu = toolbar.addMenu(folder, icon=folder + ".png")
            self._recursiveAddGizmoMenuItems(subMenu, data)
                    
if __name__ == '__main__':
    if CUSTOM_GIZMO_LOCATION and os.path.isdir(CUSTOM_GIZMO_LOCATION):
        gizManager = GizmoPathManager(searchPaths=[CUSTOM_GIZMO_LOCATION])
    else:
        gizManager = GizmoPathManager()
    gizManager.addGizmoPaths()
    if not nuke.GUI:
        # We're not gonna need it anymore, cleanup...
        del gizManager
