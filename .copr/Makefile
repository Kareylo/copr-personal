# Called by COPR (SCM source, "make_srpm" method):
#   make -f .copr/Makefile srpm outdir=<dir> spec=<path/to/pkg.spec>
#
# Sources are gathered into a scratch dir, then rpmbuild -bs makes the SRPM.
# If the package dir has a fetch-sources.sh, it produces the sources instead
# of the generic "download every SourceN URL" step.

spec ?=
outdir ?= .

PKGDIR := $(abspath $(dir $(spec)))
# COPR runs make from inside the package dir, so keep scratch files out of it.
WORK := $(or $(TMPDIR),/tmp)/copr-personal-srpm
SRCDIR := $(WORK)/SOURCES

.PHONY: srpm clean

srpm:
	test -n "$(spec)"
	rm -rf "$(WORK)"
	mkdir -p "$(SRCDIR)" "$(outdir)"
	cp -a "$(PKGDIR)/." "$(SRCDIR)/"
	if [ -x "$(PKGDIR)/fetch-sources.sh" ]; then \
		"$(PKGDIR)/fetch-sources.sh" "$(spec)" "$(SRCDIR)"; \
	else \
		rpmspec -P "$(spec)" | sed -n 's/^Source[0-9]*:[[:space:]]*//p' | while read -r src; do \
			case "$$src" in \
				*://*) curl -fL --retry 3 -o "$(SRCDIR)/$$(basename "$$src")" "$$src" ;; \
			esac; \
		done; \
	fi
	rpmbuild -bs "$(spec)" \
		--define "_topdir $(WORK)" \
		--define "_sourcedir $(SRCDIR)" \
		--define "_srcrpmdir $(outdir)"

clean:
	rm -rf "$(WORK)"
