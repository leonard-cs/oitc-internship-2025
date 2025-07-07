import { PrismaClient } from "@prisma/client"

const prisma = new PrismaClient()

async function main() {
  await prisma.message.createMany({
    data: [
      {
        position: 'start',
        name: 'Alice',
        avatarUrl: 'https://img.daisyui.com/images/profile/demo/kenobee@192.webp',
        time: new Date().toISOString(),
        content: 'Hi there!',
      },
      {
        position: 'end',
        name: 'Bob',
        avatarUrl: 'https://img.daisyui.com/images/profile/demo/anakeen@192.webp',
        time: new Date().toISOString(),
        content: 'Hello!',
      },
    ],
  });
}

main()
  .catch(e => {
    console.error(e);
    // process.exit(1);
  })
  .finally(() => prisma.$disconnect());
