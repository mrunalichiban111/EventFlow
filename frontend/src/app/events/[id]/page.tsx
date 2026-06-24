"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getEvent } from "@/services/events";
import { Event } from "@/types/event";
import { registerForEvent } from "@/services/events";

export default function EventDetailsPage() {
    const [registering, setRegistering] = useState(false);
    const [message, setMessage] = useState("");

    const { id } = useParams();

    const [event, setEvent] = useState<Event | null>(null);

    const [loading, setLoading] = useState(true);



    useEffect(() => {

        const fetchEvent = async () => {

            try {

                const data = await getEvent(Number(id));

                setEvent(data);

            } finally {

                setLoading(false);

            }

        };

        fetchEvent();

    }, [id]);

    if (loading)
        return <h1 className="p-10">Loading...</h1>;

    if (!event)
        return <h1 className="p-10">Event not found</h1>;

    const handleRegister = async () => {

        setRegistering(true);
        setMessage("");

        try {

            const response = await registerForEvent(event.id);

            if (response.status === "CONFIRMED") {
                setMessage("Registration Confirmed 🎉");
            } else {
                setMessage("Added to Waitlist 🕒");
            }

        } catch (error: any) {

            if (error.response) {
                setMessage(error.response.data.detail);
            } else {
                setMessage("Something went wrong");
            }

        }

        setRegistering(false);
    };

    return (

        <div className="min-h-screen bg-gray-100 p-10">

            <div className="bg-white rounded-xl shadow-lg p-10">

                <h1 className="text-5xl font-bold">

                    {event.title}

                </h1>

                <p className="mt-6 text-lg">

                    {event.description}

                </p>

                <div className="mt-8 space-y-3">

                    <p>

                        <strong>Capacity:</strong> {event.capacity}

                    </p>

                    <p>

                        <strong>Status:</strong> {event.status}

                    </p>

                    <p>

                        <strong>Registration:</strong>{" "}

                        {event.registration_open ? "Open" : "Closed"}

                    </p>

                    <p>

                        <strong>Date:</strong>{" "}

                        {new Date(event.event_date).toLocaleString()}

                    </p>

                </div>

                <button
                    onClick={handleRegister}
                    disabled={registering}
                    className="mt-8 bg-black text-white px-8 py-3 rounded-lg"
                >
                    {registering ? "Registering..." : "Register"}
                </button>
                {
                    message && (
                        <p className="mt-4 text-lg">
                            {message}
                        </p>
                    )
                }

            </div>

        </div>

    );

}