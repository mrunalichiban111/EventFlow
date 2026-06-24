import api from "./api";

export const getEvents = async () => {
  const response = await api.get("/events");
  return response.data;
};

export const getEvent = async (id: number) => {
  const response = await api.get(`/events/${id}`);
  return response.data;
};

export const registerForEvent = async (eventId: number) => {
  const response = await api.post("/register", {
    event_id: eventId,
  });

  return response.data;
};