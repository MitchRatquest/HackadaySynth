################################################################################
#
# trx
#
################################################################################

TRX_VERSION =  0.3
TRX_SOURCE = trx-$(TRX_VERSION).tar.gz
TRX_SITE= http://www.pogo.org.uk/~mark/trx/releases
TRX_INSTALL_STAGING = YES
TRX_INSTALL_TARGET = YES
TRX_AUTORECONF = YES 
#TRX_CONF_OPTS = --disable-portaudio --disable-portmidi --no-recursion

TRX_DEPENDENCIES = opus ortp


define TRX_BUILD_CMDS
     $(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D) all
endef

define TRX_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/tx $(TARGET_DIR)/usr/bin
	$(INSTALL) -D -m 0755 $(@D)/tx $(TARGET_DIR)/usr/bin
endef


$(eval $(generic-package))
