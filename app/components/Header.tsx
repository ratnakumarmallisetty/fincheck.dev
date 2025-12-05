"use client";

import { useSession, signOut } from "next-auth/react";
import { useRouter } from "next/navigation";

export default function Header() {
  const router = useRouter();
  const { data: session } = useSession();

  const isLoggedIn = !!session?.user;

  return (
    <nav className="fixed top-0 inset-x-0 z-30">
      <div className="w-full max-w-7xl mx-auto px-8 py-4 flex items-center justify-between">

        {/* Logo */}
        <button
          type="button"
          onClick={() => router.push("/")}
          className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent 
                     transition-all duration-300 hover:scale-105"
        >
          FinCheck
        </button>

        {/* Right Buttons */}
        <div className="flex items-center gap-5 pr-4">

          {!isLoggedIn ? (
            <>
              {/* Sign In */}
              <button
                type="button"
                onClick={() => router.push("/sign-in")}
                className="btn btn-sm btn-outline btn-primary transition-all duration-300 
                           hover:scale-110 hover:-translate-y-0.5 hover:shadow-lg"
              >
                Sign In
              </button>

              {/* Sign Up */}
              <button
                type="button"
                onClick={() => router.push("/sign-up")}
                className="btn btn-sm btn-primary transition-all duration-300 
                           hover:scale-110 hover:-translate-y-0.5 hover:shadow-lg"
              >
                Sign Up
              </button>
            </>
          ) : (
            <>
              {/* Sign Out */}
              <button
                type="button"
                onClick={() => signOut({ callbackUrl: "/sign-in" })}
                className="btn btn-sm btn-error transition-all duration-300 
                           hover:scale-110 hover:-translate-y-0.5 hover:shadow-lg"
              >
                Sign Out
              </button>
            </>
          )}

        </div>
      </div>
    </nav>
  );
}
