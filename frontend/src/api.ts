export type Review = {
  review_id: number;
  rating: number;
  review_text: string;
  created_at: string;
};

export type Rating = {
  restaurant_name: string;
  average_rating: number | null;
  review_count: number;
};

const API_URL = import.meta.env.VITE_API_URL ?? "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? "Something went wrong");
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export const api = {
  getReviews: () => request<Review[]>("/reviews"),
  getRating: () => request<Rating>("/restaurant/rating"),
  createReview: (rating: number, comment: string) =>
    request<Review>("/reviews", {
      method: "POST",
      body: JSON.stringify({ rating, review_text: comment }),
    }),
  updateReview: (id: number, rating: number, comment: string) =>
    request<Review>(`/reviews/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ rating, review_text: comment }),
    }),
  deleteReview: (id: number) =>
    request<void>(`/reviews/${id}`, { method: "DELETE" }),
};
