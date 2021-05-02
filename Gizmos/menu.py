if __name__ == '__main__':
  # Just in case they didn't use the supplied init.py
  gizManager = globals().get('gizManager', None)
  if gizManager is None:
      print('Problem finding GizmoPathManager - check that init.py was setup correctly')
  else:
      gizManager.addGizmoMenuItems()
      # Don't need it no more...
      del gizManager
