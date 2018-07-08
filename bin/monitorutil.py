# # uses screeninfo package from PyPl
# from screeninfo import get_monitors
# for m in get_monitors():
#     print(str(m))

# native method
import subprocess
output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
print output
