# Run Prisma DB push
Write-Host "🚀 Running prisma db push..."
npx prisma db push

# Run seed
Write-Host "🌱 Running prisma db seed..."
npx prisma db seed

# Start the Next.js app
Write-Host "🌐 Starting Next.js app..."
npm run dev
