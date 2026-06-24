export interface Event {
  id: number;
  title: string;
  description: string;
  capacity: number;
  creator_id: number;
  registration_open: boolean;
  status: string;
  event_date: string;
}