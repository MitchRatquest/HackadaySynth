################################################################################
#
# orca
#
################################################################################

ORCA_VERSION =  df0e1276ec2ef795f8a072a6f6768cc7ef73647c
ORCA_SITE = $(call github,hundredrabbits,Orca-c,$(ORCA_VERSION))
ORCA_INSTALL_TARGET = YES

ORCA_DEPENDENCIES = ncurses


define ORCA_BUILD_CMDS
$(MAKE) CC="$(TARGET_CC)" LD=$(TARGET_LD) -C $(@D) release
endef

define ORCA_INSTALL_TARGET_CMDS
$(INSTALL) -D -m 0755 $(@D)/build/release/orca $(TARGET_DIR)/usr/bin
endef

#$(INSTALL) -D -m 0644 $(@D)/examples/* $(TARGET_DIR)/usr/share/orca

$(eval $(generic-package))
