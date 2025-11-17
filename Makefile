# Install dependencies
install:
	pnpm install

# Start development server
dev:
	pnpm dev

# Build the project
build:
	pnpm build

# Start the production server
start:
	pnpm start

# Run database migrations
migrate:
	npx prisma migrate dev

# Format all files
format:
	npx prettier --write .

# Lint the code
lint:
	pnpm lint

# Remove build artifacts and dependencies
clean:
	rm -rf node_modules .next

# Clean and reinstall everything
reset: clean
	pnpm install
