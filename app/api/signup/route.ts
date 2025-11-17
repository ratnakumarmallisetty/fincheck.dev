import { prisma } from "../../../lib/prisma";
import bcrypt from "bcrypt";

export async function POST(req: Request) {
  try {
    const { username, password } = await req.json();

    const exists = await prisma.user.findUnique({
      where: { username },
    });

    if (exists) {
      return new Response("Username already exists", { status: 400 });
    }

    const hashed = await bcrypt.hash(password, 10);

    const user = await prisma.user.create({
      data: { username, password: hashed },
    });

    return Response.json({ success: true, userId: user.id });
  } catch (err) {
    console.error(err);
    return new Response("Error creating new user", { status: 500 });
  }
}
