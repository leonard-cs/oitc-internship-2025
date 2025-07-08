import { SYSTEM } from "@/constants/chat";
import { PrismaClient } from "@prisma/client"

const prisma = new PrismaClient()

async function main() {
  await prisma.message.createMany({
    data: [
      {
        position: SYSTEM.position,
        name: SYSTEM.name,
        avatarUrl: SYSTEM.avatarUrl,
        time: new Date().toISOString(),
        content: "Welcome to the chat! How can I help you today?",
      },
      // {
      //   position: 'end',
      //   name: 'You',
      //   avatarUrl: 'https://img.daisyui.com/images/profile/demo/anakeen@192.webp',
      //   time: new Date().toISOString(),
      //   content: 'Hello!',
      // },
    ],
  });
}

main()
  .catch(e => {
    console.error(e);
    // process.exit(1);
  })
  .finally(() => prisma.$disconnect());
