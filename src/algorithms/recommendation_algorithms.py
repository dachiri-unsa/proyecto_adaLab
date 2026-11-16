from models import Recommendation
from .sorting import merge_sort


def genre_similarity(media_a, media_b):
    genres_a = media_a.genres
    genres_b = media_b.genres

    union = genres_a | genres_b

    if not union:
        return 0.0

    intersection = genres_a & genres_b

    return len(intersection) / len(union)


def brute_force_similar(target, catalog, limit=5):

    similarities = []

    for media in catalog:

        if media.id == target.id:
            continue

        score = genre_similarity(target, media)

        if score > 0:
            similarities.append((media, score))

    similarities = merge_sort(
        similarities,
        key=lambda item: item[1],
        reverse=True
    )

    return similarities[:limit]


def greedy_recommendations(catalog, ratings, limit=5):

    preferred_genres = {}
    rated_ids = set()

    # Identificar preferencias
    for rating in ratings:

        rated_ids.add(rating.media.id)

        if rating.score >= 4:

            for genre in rating.media.genres:
                preferred_genres[genre] = (
                    preferred_genres.get(genre, 0) + 1
                )

    if not preferred_genres:
        return []

    total_preferences = sum(preferred_genres.values())

    # Excluir contenidos ya valorados
    candidates = [
        media for media in catalog
        if media.id not in rated_ids
    ]

    selected = []
    covered_genres = set()

    # Selección Greedy
    while candidates and len(selected) < limit:

        best_media = None
        best_score = -1
        best_genres = set()

        for media in candidates:

            new_genres = (
                media.genres & preferred_genres.keys()
            ) - covered_genres

            preference_score = sum(
                preferred_genres[genre]
                for genre in new_genres
            ) / total_preferences

            popularity_score = media.popularity / 100

            score = (
                0.8 * preference_score
                + 0.2 * popularity_score
            )

            if score > best_score:
                best_score = score
                best_media = media
                best_genres = new_genres

        if best_media is None:
            break

        reason = (
            "Coincide con los géneros preferidos: "
            + ", ".join(
                genre.name for genre in best_genres
            )
            if best_genres
            else "Destaca por su popularidad."
        )

        selected.append(
            Recommendation(
                media=best_media,
                similarity_score=best_score,
                reason=reason
            )
        )

        covered_genres.update(best_genres)
        candidates.remove(best_media)

    return selected