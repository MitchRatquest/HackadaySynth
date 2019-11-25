################################################################################
#
# puredata
#
################################################################################

PUREDATA_VERSION = 0.50-2
ORCA_SITE = $(call github,pure-data,pure-data,$(PUREDATA_VERSION))
PUREDATA_INSTALL_STAGING = YES
PUREDATA_INSTALL_TARGET = YES
PUREDATA_AUTORECONF = YES 
PUREDATA_CONF_OPTS = --disable-portaudio --disable-portmidi --no-recursion

PUREDATA_DEPENDENCIES = alsa-utils gettext tcl tk

define PUREDATA_RUN_AUTOGEN
	cd $(@D) && PATH=$(BR_PATH) ./autogen.sh
endef
PUREDATA_PRE_CONFIGURE_HOOKS += PUREDATA_RUN_AUTOGEN

$(eval $(autotools-package))
