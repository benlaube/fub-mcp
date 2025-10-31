#!/bin/bash
# Helper script to push to remote repository

echo "============================================"
echo "FUB MCP Server - Push to Remote Repository"
echo "============================================"
echo ""

# Check if remote exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "✅ Remote 'origin' is configured:"
    git remote get-url origin
    echo ""
    echo "📤 Pushing to remote..."
    git push -u origin main
    echo ""
    echo "✅ Successfully pushed to remote!"
else
    echo "❌ No remote repository configured."
    echo ""
    echo "Please add your remote repository first:"
    echo ""
    echo "  git remote add origin <your-repo-url>"
    echo ""
    echo "Examples:"
    echo "  git remote add origin https://github.com/username/fub-mcp.git"
    echo "  git remote add origin git@github.com:username/fub-mcp.git"
    echo ""
    echo "Then run this script again or:"
    echo "  git push -u origin main"
fi

