import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";
import bcrypt from "bcryptjs";
import { prisma } from "@/lib/prisma";
import { RateLimiterMemory } from "rate-limiter-flexible";

const ipLimiter = new RateLimiterMemory({
  points: 20,
  duration: 60 * 15,
});

const usernameLimiter = new RateLimiterMemory({
  points: 5,
  duration: 60 * 15,
});

const handler = NextAuth({
  session: { strategy: "jwt" },

  providers: [
    Credentials({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
      },

      async authorize(credentials, req) {
        // ---- FIXED: Safe header + IP extraction ----
        const forwarded = req?.headers?.["x-forwarded-for"];
        const ip =
          (Array.isArray(forwarded) ? forwarded[0] : forwarded) ||
          (req as any)?.ip ||
          "0.0.0.0";

        const username = credentials?.username;

        try {
          await ipLimiter.consume(ip);
        } catch {
          return null;
        }

        try {
          if (username) await usernameLimiter.consume(username);
        } catch {
          return null;
        }

        if (!username || !credentials.password) return null;

        const user = await prisma.user.findUnique({
          where: { username },
        });

        if (!user) return null;

        const valid = await bcrypt.compare(
          credentials.password,
          user.password
        );

        if (!valid) return null;

        ipLimiter.delete(ip);
        usernameLimiter.delete(username);

        return {
          id: String(user.id),
          username: user.username,
        };
      },
    }),
  ],

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.username = user.username;
      }
      return token;
    },

    async session({ session, token }) {
      if (token) {
        session.user = {
          id: token.id,
          username: token.username,
        };
      }
      return session;
    },
  },
});

export { handler as GET, handler as POST };
