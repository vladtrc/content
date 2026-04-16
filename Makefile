SHELL := /usr/bin/bash

.PHONY: setup render-manim render-manim-all check-manim watch-manim dev build pdf pdfs clean

# Install dependencies
setup:
	uv sync --frozen

# Render only stale manim assets used by content pages
render-manim:
	uv run python scripts/render_manim.py --changed-only

# Force a full manim rebuild
render-manim-all:
	uv run python scripts/render_manim.py

# Render one specific manim scene file
# Usage: make check-manim FILE=courses/ais/b-tree/animations/btree_insert_progression_gif.py
check-manim:
	@test -n "$(FILE)" || (echo "usage: make check-manim FILE=path/to/scene.py" && exit 1)
	uv run python scripts/render_manim.py --source "$(FILE)"

# Watch manim sources and rebuild only changed assets
watch-manim:
	uv run python scripts/render_manim.py --watch --changed-only

# Live preview in browser
dev:
	@uv run python scripts/render_manim.py --changed-only
	@watcher_pid=; \
	preview_pid=; \
	cleanup() { \
		if [ -n "$$preview_pid" ]; then kill "$$preview_pid" 2>/dev/null || true; fi; \
		if [ -n "$$watcher_pid" ]; then kill "$$watcher_pid" 2>/dev/null || true; fi; \
		wait "$$preview_pid" "$$watcher_pid" 2>/dev/null || true; \
	}; \
	trap cleanup EXIT INT TERM; \
	uv run python scripts/render_manim.py --watch --changed-only & \
	watcher_pid=$$!; \
	uv run quarto preview & \
	preview_pid=$$!; \
	wait "$$preview_pid"

# Build static site
build: render-manim
	uv run quarto render

# Build PDF for a specific course (usage: make pdf COURSE=courses/ais/b-tree)
pdf: render-manim
	uv run quarto render $(COURSE)/index.qmd --to typst

# Build all PDFs (all .qmd files that have typst format configured)
pdfs: render-manim
	@find courses -name 'index.qmd' -exec grep -l 'typst' {} \; | while read f; do \
		echo "==> $$f"; \
		uv run quarto render "$$f" --to typst; \
	done

# Remove build artifacts
clean:
	rm -rf docs .quarto .manim courses/*/*/generated posts/*/*/*/generated
