#!/bin/sh

# Wait for DB to be ready
echo "⏳ Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

# Run Prisma DB push
echo "🚀 Running prisma db push..."
npx prisma db push

# Run seed
echo "🌱 Running prisma db seed..."
npx prisma db seed

# Start the Next.js app
echo "🌐 Starting Next.js app..."
npm run dev
