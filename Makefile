deploy:
	@echo "Optimizing images..."
	uv run python optimize_images.py

	@echo "Generating RSS feed..."
	uv run python generate_rss.py

	@echo "Deploying to Railway..."
	railway up --detach
