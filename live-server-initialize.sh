

echo "Initializing project environment..."
uv sync

echo
echo "Migrating database..."
uv run manage.py migrate

echo
echo "Starting frontend initialization..."
cd "$(dirname "$0")/frontend"

echo
echo "Initializing frontend dependencies..."
npm install

echo "Project Setup Complete!"
