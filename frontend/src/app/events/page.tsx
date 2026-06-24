"use client";

import { useEffect, useState } from "react";
import { getEvents } from "@/services/events";
import { Event } from "@/types/event";
import { useRouter } from "next/navigation";

export default function EventsPage() {
    const [events, setEvents] = useState<Event[]>([]);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const data = await getEvents();
                setEvents(data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchEvents();
    }, []);

    if (loading) {
        return <h1 className="p-10">Loading...</h1>;
    }

    return (
        <div className="min-h-screen bg-black-100 p-10">
            <h1 className="text-4xl font-bold mb-8">
                All Events
            </h1>

            <div className="space-y-6">

                {events.map((event: any) => (
                    <div
                        key={event.id}
                        className="bg-white rounded-xl shadow p-6"
                    >
                        <h2 className="text-2xl font-semibold">
                            {event.title}
                        </h2>

                        <p className="mt-2">
                            {event.description}
                        </p>

                        <p className="mt-3">
                            Capacity: {event.capacity}
                        </p>

                        <p>
                            Status: {event.status}
                        </p>

                        <p>
                            Event Date:
                            {" "}
                            {new Date(event.event_date).toLocaleString()}
                        </p>

                        <button
                            onClick={() => router.push(`/events/${event.id}`)}
                            className="mt-5 bg-black text-white px-5 py-2 rounded-lg"
                        >
                            View Details
                        </button>
                    </div>
                ))}

            </div>
        </div>
    );
}