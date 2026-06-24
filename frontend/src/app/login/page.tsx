"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { loginUser } from "@/services/auth";

export default function LoginPage() {
    const router = useRouter();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleLogin = async (
        e: React.FormEvent
    ) => {
        e.preventDefault();

        setError("");
        setLoading(true);

        try {
            const data = await loginUser(
                email,
                password
            );

            console.log(data);
            localStorage.setItem(
                "token",
                data.access_token
            );

            window.location.href = "/events";
        } catch (err: any) {
            setError(
                err?.response?.data?.detail ||
                "Login failed"
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
                <h1 className="text-3xl font-bold text-center mb-6 text-black">
                    EventFlow AI
                </h1>

                <form
                    onSubmit={handleLogin}
                    className="space-y-4"
                >
                    <div>
                        <label className="block mb-1 text-black">
                            Email
                        </label>

                        <input
                            type="email"
                            value={email}
                            onChange={(e) =>
                                setEmail(e.target.value)
                            }
                            className="w-full border rounded-lg p-3 text-black"
                            required
                        />
                    </div>

                    <div>
                        <label className="block mb-1 text-black">
                            Password
                        </label>

                        <input
                            type="password"
                            value={password}
                            onChange={(e) =>
                                setPassword(
                                    e.target.value
                                )
                            }
                            className="w-full border rounded-lg p-3 text-black"
                            required
                        />
                    </div>

                    {error && (
                        <p className="text-red-500 text-sm">
                            {error}
                        </p>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-black text-white p-3 rounded-lg"
                    >
                        {loading
                            ? "Logging in..."
                            : "Login"}
                    </button>
                </form>

                <p className="text-center mt-6">
                    Don't have an account?{" "}
                    <button
                        className="text-blue-600 underline"
                        onClick={() => router.push("/signup")}
                    >
                        Sign Up
                    </button>
                </p>
            </div>
        </div>


    );
}
