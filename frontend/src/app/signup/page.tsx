"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signupUser } from "@/services/users";

export default function SignupPage() {
    const router = useRouter();

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("STUDENT");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSignup = async () => {
        setLoading(true);
        setError("");

        try {
            await signupUser(name, email, password, role);

            alert("Account created successfully!");

            window.location.href = "/login";
        } catch (err) {
            setError("Signup failed");
        }

        setLoading(false);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">

            <div className="bg-white p-10 rounded-xl shadow-lg w-[450px]">

                <h1 className="text-4xl font-bold mb-8 text-center text-black">
                    EventFlow AI
                </h1>

                <div className="space-y-5">

                    <input
                        type="text"
                        placeholder="Full Name"
                        className="w-full border p-3 rounded-lg text-black"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />

                    <input
                        type="email"
                        placeholder="Email"
                        className="w-full border p-3 rounded-lg text-black"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        className="w-full border p-3 rounded-lg text-black"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    <select
                        className="w-full border p-3 rounded-lg text-black"
                        value={role}
                        onChange={(e) => setRole(e.target.value)}
                    >
                        <option value="STUDENT">Student</option>
                        <option value="ORGANIZER">Organizer</option>
                    </select>

                    {error && (
                        <p className="text-red-500">
                            {error}
                        </p>
                    )}

                    <button
                        onClick={handleSignup}
                        disabled={loading}
                        className="w-full bg-black text-white py-3 rounded-lg"
                    >
                        {loading ? "Creating Account..." : "Create Account"}
                    </button>

                    <p className="text-center mt-6">
                        Already have an account?{" "}
                        <button
                            className="text-blue-600 underline"
                            onClick={() => router.push("/login")}
                        >
                            Login
                        </button>
                    </p>

                </div>

            </div>

        </div>
    );
}