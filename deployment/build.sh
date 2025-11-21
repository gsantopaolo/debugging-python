#!/bin/bash
# ============================================================================
# Build script for DateTime API
# ============================================================================
# remember to: chmod +x build.sh
set -e

# Version configuration
VERSION="${VERSION:-1.0.3}"
IMAGE_NAME="gsantopaolo/challenge-datetime-api"

echo "🏗️  Building DateTime API Container..."
echo "📦 Image: ${IMAGE_NAME}:${VERSION}"
echo ""

# Build the image with multiple tags
echo "📦 Building Docker image..."
cd "$(dirname "$0")/.."

# Detect architecture and build for Azure (linux/amd64)
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
  echo "🍎 Detected Apple Silicon (ARM64)"
  echo "🔧 Building for linux/amd64 platform (required for Azure)"
  docker buildx build --platform linux/amd64 \
    -f src/Dockerfile \
    -t ${IMAGE_NAME}:${VERSION} \
    -t ${IMAGE_NAME}:latest \
    --load \
    src/
else
  echo "🖥️  Detected x86_64 architecture"
  docker build -f src/Dockerfile \
    -t ${IMAGE_NAME}:${VERSION} \
    -t ${IMAGE_NAME}:latest \
    src/
fi

echo ""
echo "✅ Build complete!"
echo ""
echo "🚀 To run the container:"
echo ""
echo "   docker run -d \\"
echo "     --name challenge-datetime-api \\"
echo "     -p 8000:8000 \\"
echo "     ${IMAGE_NAME}:${VERSION}"
echo ""
echo "🌐 Access URLs:"
echo "   API Endpoint: http://localhost:8000/datetime"
echo "   API Docs:     http://localhost:8000/docs"
echo "   Root:         http://localhost:8000"
echo ""
echo "📝 Example API usage:"
echo "   curl http://localhost:8000/datetime"
echo ""
