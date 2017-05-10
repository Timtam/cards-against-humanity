import platform

_system = platform.system()

if _system == 'Windows':
 from jaws import Jaws
 from nvda import NVDA
 from sa import SystemAccess
 from we import WindowEyes
 from virgo import Virgo
 
 __all__ = ["Jaws", "NVDA", "SystemAccess", "WindowEyes","Virgo"]
else:
 __all__ = []
