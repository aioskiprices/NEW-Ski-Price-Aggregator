# SkiSniper - GitHub Pages Branch

This branch contains the static website version of SkiSniper, optimized for GitHub Pages deployment. The site allows users to search and compare ski prices across multiple retailers.

## Features

- Search for skis across multiple retailers
- Compare prices in real-time
- View detailed ski information and images
- Direct links to retailer pages

## Development

The main development branch contains the full Flask application. This branch (`gh-pages`) contains only the static assets needed for the GitHub Pages deployment.

To update the ski prices:

1. Run the price update script from the main branch
2. Copy the updated `ski_prices.json` to this branch
3. Commit and push the changes

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to this branch. You can view the live site at: [https://[username].github.io/Ski-Price-Aggregator](https://[username].github.io/Ski-Price-Aggregator) 