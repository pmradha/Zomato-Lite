import { FormEvent, useEffect, useState } from "react";
import { MapPin, Pencil, Star, Trash2, Utensils } from "lucide-react";
import { api, Rating, Review } from "./api";

type ReviewFormProps = {
  initialRating?: number;
  initialComment?: string;
  submitLabel: string;
  onSubmit: (rating: number, comment: string) => Promise<void>;
  onCancel?: () => void;
};

function Stars({ value, interactive = false, onChange }: { value: number; interactive?: boolean; onChange?: (value: number) => void }) {
  return (
    <div className="stars" aria-label={`${value} out of 5 stars`}>
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          type="button"
          className={interactive ? "star-button" : "star-button static"}
          aria-label={`${star} star${star === 1 ? "" : "s"}`}
          key={star}
          onClick={() => onChange?.(star)}
        >
          <Star size={interactive ? 22 : 16} fill={star <= value ? "currentColor" : "none"} />
        </button>
      ))}
    </div>
  );
}

function ReviewForm({ initialRating = 5, initialComment = "", submitLabel, onSubmit, onCancel }: ReviewFormProps) {
  const [rating, setRating] = useState(initialRating);
  const [comment, setComment] = useState(initialComment);
  const [saving, setSaving] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!comment.trim()) return;
    setSaving(true);
    try {
      await onSubmit(rating, comment.trim());
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="review-form" onSubmit={submit}>
      <div className="form-heading">
        <div>
          <p className="eyebrow">Your table, your take</p>
          <h2>{submitLabel === "Post review" ? "Leave a review" : "Edit your review"}</h2>
        </div>
        <Stars value={rating} interactive onChange={setRating} />
      </div>
      <label>
        <span className="sr-only">Review</span>
        <textarea value={comment} onChange={(event) => setComment(event.target.value)} placeholder="What should another diner know?" maxLength={2000} rows={4} />
      </label>
      <div className="form-actions">
        {onCancel && <button type="button" className="button quiet" onClick={onCancel}>Cancel</button>}
        <button type="submit" className="button primary" disabled={saving || !comment.trim()}>{saving ? "Saving..." : submitLabel}</button>
      </div>
    </form>
  );
}

export function App() {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [rating, setRating] = useState<Rating | null>(null);
  const [editing, setEditing] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    try {
      const [loadedReviews, loadedRating] = await Promise.all([api.getReviews(), api.getRating()]);
      setReviews(loadedReviews);
      setRating(loadedRating);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "Unable to load reviews");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { void load(); }, []);

  async function createReview(reviewRating: number, comment: string) {
    await api.createReview(reviewRating, comment);
    await load();
  }

  async function updateReview(id: string, reviewRating: number, comment: string) {
    await api.updateReview(id, reviewRating, comment);
    setEditing(null);
    await load();
  }

  async function deleteReview(id: string) {
    await api.deleteReview(id);
    await load();
  }

  return (
    <main>
      <header className="topbar"><span className="brand-mark">ZL</span><span>zomato-lite</span><span className="topbar-note">Local tables, honest takes</span></header>
      <section className="restaurant-hero">
        <div className="hero-copy">
          <div className="tag"><Utensils size={14} /> Dine-in · Indian</div>
          <h1>Ludhiana<br /><em>Burrito</em></h1>
          <p className="location"><MapPin size={17} /> Sector 32</p>
        </div>
        <div className="rating-block">
          <p className="eyebrow">Community rating</p>
          <strong>{rating?.average_rating == null ? "—" : Number(rating.average_rating).toFixed(1)}</strong>
          <Stars value={Math.round(Number(rating?.average_rating ?? 0))} />
          <span>{rating?.review_count ?? 0} {rating?.review_count === 1 ? "review" : "reviews"}</span>
        </div>
      </section>
      <section className="content-grid">
        <div className="reviews-column">
          <div className="section-heading"><div><p className="eyebrow">From the community</p><h2>Reviews</h2></div><span className="review-count">{reviews.length.toString().padStart(2, "0")}</span></div>
          {loading && <p className="state">Loading reviews...</p>}
          {!loading && !reviews.length && <p className="state">No reviews yet. Be the first voice at the table.</p>}
          {error && <p className="state error">{error}</p>}
          <div className="review-list">
            {reviews.map((review) => (
              <article className="review" key={review.review_id}>
                {editing === review.review_id ? <ReviewForm initialRating={review.rating} initialComment={review.comment} submitLabel="Save changes" onSubmit={(newRating, comment) => updateReview(review.review_id, newRating, comment)} onCancel={() => setEditing(null)} /> : <>
                  <div className="review-meta"><Stars value={review.rating} /><time>{new Date(review.created_at).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" })}</time></div>
                  <p>{review.comment}</p>
                  <div className="review-actions"><button type="button" onClick={() => setEditing(review.review_id)}><Pencil size={14} /> Edit</button><button type="button" onClick={() => void deleteReview(review.review_id)}><Trash2 size={14} /> Delete</button></div>
                </>}
              </article>
            ))}
          </div>
        </div>
        <aside><ReviewForm submitLabel="Post review" onSubmit={createReview} /><p className="anonymous-note">Reviews are anonymous. Keep it kind and useful for the next diner.</p></aside>
      </section>
    </main>
  );
}
