import re
# Genie
from genie.ops.base import Base


class Platform(Base):
    exclude = ['rp_uptime',
               'disk_free_space',
               'uptime',
               'switchover_reason',
               'disk_used_space',
               'total_free_bytes',
               'disk_total_space',
               'main_mem',
               'date',
               'index',
               'chassis_sn',
               'image',
               'sn',
               'rp_boot_image',
               'installed_packages',
               'version']
