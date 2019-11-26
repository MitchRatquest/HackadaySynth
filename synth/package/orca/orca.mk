################################################################################
#
# orca
#
################################################################################

ORCA_VERSION = 996652ee82406485cfef4b5dbaeb2743c4a00db7 
ORCA_SITE = $(call github,hundredrabbits,Orca-c,$(ORCA_VERSION))
ORCA_INSTALL_TARGET = YES

ORCA_DEPENDENCIES = ncurses


define ORCA_BUILD_CMDS
$(MAKE) CC="$(TARGET_CC)" LD=$(TARGET_LD) -C $(@D) -std=c99 -pipe -finput-charset=UTF-8 -Wall -Wpedantic -Wextra -Wconversion -Wstrict-prototypes -Werror=implicit-function-declaration -Werror=implicit-int -Werror=incompatible-pointer-types -Werror=int-conversion -no-pie -fno-pie -DNDEBUG -O2 -g0 -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=0 -fno-stack-protector -flto -s -march=armv7 -lrt -lmenuw -lformw -lncursesw gbuffer.c field.c mark.c bank.c sim.c osc_out.c term_util.c tui_main.c -o build/release/orca
#release
endef

define ORCA_INSTALL_TARGET_CMDS
$(INSTALL) -D -m 0755 $(@D)/build/release/orca $(TARGET_DIR)/usr/bin
endef

#$(INSTALL) -D -m 0644 $(@D)/examples/* $(TARGET_DIR)/usr/share/orca

$(eval $(generic-package))
