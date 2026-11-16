
from models import (
    Genre,
    Movie,
    Series,
    SeriesStatus,
    Rating
)

from algorithms import (
    merge_sort,
    binary_search,
    brute_force_similar,
    greedy_recommendations
)


# ==========================================
# CONFIGURACIÓN VISUAL
# ==========================================

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GRAY = "\033[90m"


def clear_screen():
    print("\033[2J\033[H", end="")


def print_header():
    print(Colors.CYAN + Colors.BOLD)
    print("╔══════════════════════════════════════════════╗")
    print("║                                              ║")
    print("║          CINEMATCH - RECOMMENDER             ║")
    print("║                                              ║")
    print("║       Sistema de películas y series          ║")
    print("║                                              ║")
    print("╚══════════════════════════════════════════════╝")
    print(Colors.RESET)


def print_section(title):
    print(f"\n{Colors.CYAN}{Colors.BOLD}── {title} ──{Colors.RESET}")


def pause():
    input(f"\n{Colors.GRAY}Presiona ENTER para continuar...{Colors.RESET}")


def print_option(number, description):
    print(
        f"  {Colors.GREEN}{number}{Colors.RESET}."
        f" {description}"
    )


# ==========================================
# DATOS DEL SISTEMA
# ==========================================

def create_genres():
    return {
        "action": Genre(1, "Acción"),
        "scifi": Genre(2, "Ciencia ficción"),
        "drama": Genre(3, "Drama"),
        "romance": Genre(4, "Romance"),
        "thriller": Genre(5, "Suspenso"),
        "comedy": Genre(6, "Comedia")
    }


def create_catalog(genres):

    movies = [
        Movie(
            id=1,
            title="Inception",
            description="Un ladrón que invade los sueños.",
            release_year=2010,
            genres={genres["action"], genres["scifi"]},
            popularity=95.5,
            duration_minutes=148
        ),
        Movie(
            id=2,
            title="Interstellar",
            description="Un viaje a través del espacio.",
            release_year=2014,
            genres={genres["scifi"], genres["drama"]},
            popularity=98.2,
            duration_minutes=169
        ),
        Movie(
            id=3,
            title="Titanic",
            description="Una historia de amor en el Titanic.",
            release_year=1997,
            genres={genres["romance"], genres["drama"]},
            popularity=90.0,
            duration_minutes=195
        ),
        Movie(
            id=4,
            title="The Dark Knight",
            description="Batman enfrenta a uno de sus enemigos.",
            release_year=2008,
            genres={genres["action"], genres["thriller"]},
            popularity=96.8,
            duration_minutes=152
        ),
        Movie(
            id=5,
            title="The Matrix",
            description="Un programador descubre la realidad.",
            release_year=1999,
            genres={genres["action"], genres["scifi"]},
            popularity=94.0,
            duration_minutes=136
        )
    ]

    series = [
        Series(
            id=6,
            title="Breaking Bad",
            description="Un profesor comienza a fabricar drogas.",
            release_year=2008,
            genres={genres["drama"], genres["thriller"]},
            popularity=97.0,
            number_of_seasons=5,
            status=SeriesStatus.COMPLETED
        ),
        Series(
            id=7,
            title="Stranger Things",
            description="Un grupo de amigos descubre fenómenos extraños.",
            release_year=2016,
            genres={genres["scifi"], genres["thriller"]},
            popularity=94.5,
            number_of_seasons=5,
            status=SeriesStatus.COMPLETED
        )
    ]

    return movies + series


def create_ratings(catalog):
    return [
        Rating(catalog[0], 5),
        Rating(catalog[1], 5),
        Rating(catalog[2], 2),
        Rating(catalog[3], 4)
    ]


# ==========================================
# FUNCIONES DE PRESENTACIÓN
# ==========================================

def show_media(media, index=None):

    if isinstance(media, Movie):
        media_type = "Película"
    else:
        media_type = "Serie"

    genres = ", ".join(
        genre.name for genre in media.genres
    )

    if index is not None:
        print(f"\n{Colors.YELLOW}{index}.{Colors.RESET} ", end="")
    else:
        print("\n", end="")

    print(f"{Colors.BOLD}{media.title}{Colors.RESET}")
    print(f"   ID: {media.id} | Tipo: {media_type}")
    print(f"   Año: {media.release_year}")
    print(f"   Géneros: {genres}")
    print(f"   Popularidad: {media.popularity}/100")

    if isinstance(media, Movie):
        print(f"   Duración: {media.duration_minutes} minutos")
    else:
        print(f"   Temporadas: {media.number_of_seasons}")
        print(f"   Estado: {media.status.value}")


def show_catalog(catalog):

    print_section("CATÁLOGO DE CONTENIDOS")

    print(f"Total de contenidos: {len(catalog)}")

    for index, media in enumerate(catalog, start=1):
        show_media(media, index)


def show_ratings(ratings):

    print_section("VALORACIONES REGISTRADAS")

    if not ratings:
        print("Todavía no existen valoraciones.")
        return

    for rating in ratings:
        print(
            f"  {rating.media.title:<22} "
            f"{rating.score}/5"
        )


def find_media(catalog, title):

    ordered_catalog = merge_sort(
        catalog,
        key=lambda media: media.title.casefold()
    )

    return binary_search(ordered_catalog, title)


# ==========================================
# OPCIONES DEL SISTEMA
# ==========================================

def option_show_catalog(catalog):

    clear_screen()
    print_header()

    show_catalog(catalog)
    pause()


def option_search(catalog):

    clear_screen()
    print_header()

    print_section("BÚSQUEDA BINARIA")

    title = input("\nIngresa el título: ").strip()

    if not title:
        print(f"\n{Colors.RED}El título no puede estar vacío.{Colors.RESET}")
        pause()
        return

    result = find_media(catalog, title)

    if result:
        print(f"\n{Colors.GREEN}Contenido encontrado:{Colors.RESET}")
        show_media(result)
    else:
        print(f"\n{Colors.RED}No se encontró el contenido.{Colors.RESET}")

    print("\nComplejidad de búsqueda: O(log n)")
    pause()


def option_sort_catalog(catalog):

    clear_screen()
    print_header()

    print_section("ORDENAMIENTO - MERGE SORT")

    print_option(1, "Popularidad (mayor a menor)")
    print_option(2, "Año (más reciente primero)")
    print_option(3, "Título (A-Z)")

    choice = input("\nSelecciona un criterio: ").strip()

    if choice == "1":
        ordered = merge_sort(
            catalog,
            key=lambda media: media.popularity,
            reverse=True
        )
        criterion = "Popularidad"

    elif choice == "2":
        ordered = merge_sort(
            catalog,
            key=lambda media: media.release_year,
            reverse=True
        )
        criterion = "Año de lanzamiento"

    elif choice == "3":
        ordered = merge_sort(
            catalog,
            key=lambda media: media.title.casefold()
        )
        criterion = "Título"

    else:
        print(f"\n{Colors.RED}Opción inválida.{Colors.RESET}")
        pause()
        return

    print_section(f"RESULTADO: {criterion.upper()}")

    for index, media in enumerate(ordered, start=1):
        show_media(media, index)

    print("\nAlgoritmo: Merge Sort")
    print("Complejidad temporal: O(n log n)")

    pause()


def option_similar(catalog):

    clear_screen()
    print_header()

    print_section("CONTENIDOS SIMILARES - FUERZA BRUTA")

    title = input("\nIngresa un título: ").strip()

    target = find_media(catalog, title)

    if target is None:
        print(f"\n{Colors.RED}Contenido no encontrado.{Colors.RESET}")
        pause()
        return

    results = brute_force_similar(target, catalog)

    print(f"\nContenidos similares a: {target.title}")

    if not results:
        print("\nNo se encontraron contenidos similares.")
    else:
        for index, (media, score) in enumerate(results, start=1):
            print(f"\n{index}. {media.title}")
            print(f"   Similitud: {score * 100:.2f}%")
            print(
                "   Géneros compartidos: "
                + ", ".join(
                    genre.name
                    for genre in media.genres & target.genres
                )
            )

    print("\nAlgoritmo: Fuerza bruta")
    print("Se comparó el contenido seleccionado con el catálogo.")

    pause()


def option_recommendations(catalog, ratings):

    clear_screen()
    print_header()

    print_section("RECOMENDACIONES - GREEDY")

    print("Preferencias obtenidas de las valoraciones de 4 y 5 estrellas.")

    recommendations = greedy_recommendations(
        catalog,
        ratings,
        limit=5
    )

    if not recommendations:
        print("\nNo hay suficientes datos para recomendar contenidos.")
        pause()
        return

    print("\nTus recomendaciones:\n")

    for index, recommendation in enumerate(recommendations, start=1):
        print(
            f"{Colors.GREEN}{index}. "
            f"{recommendation.media.title}{Colors.RESET}"
        )
        print(
            f"   Afinidad: "
            f"{recommendation.similarity_score * 100:.2f}%"
        )
        print(f"   Motivo: {recommendation.reason}")

    print("\nAlgoritmo: Greedy")
    print("Estrategia: maximizar afinidad y cobertura de géneros.")

    pause()


def option_show_ratings(ratings):

    clear_screen()
    print_header()

    show_ratings(ratings)

    pause()


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

def show_menu():

    clear_screen()
    print_header()

    print_section("MENÚ PRINCIPAL")

    print_option(1, "Mostrar catálogo")
    print_option(2, "Buscar contenido (Búsqueda binaria)")
    print_option(3, "Ordenar catálogo (Merge Sort)")
    print_option(4, "Encontrar similares (Fuerza bruta)")
    print_option(5, "Generar recomendaciones (Greedy)")
    print_option(6, "Consultar valoraciones")

    print("\n  0. Salir")

    print(
        f"\n{Colors.GRAY}"
        "Proyecto académico - Análisis y Diseño de Algoritmos"
        f"{Colors.RESET}"
    )


def main():

    genres = create_genres()
    catalog = create_catalog(genres)
    ratings = create_ratings(catalog)

    while True:

        show_menu()

        choice = input("\nSelecciona una opción: ").strip()

        if choice == "1":
            option_show_catalog(catalog)

        elif choice == "2":
            option_search(catalog)

        elif choice == "3":
            option_sort_catalog(catalog)

        elif choice == "4":
            option_similar(catalog)

        elif choice == "5":
            option_recommendations(catalog, ratings)

        elif choice == "6":
            option_show_ratings(ratings)

        elif choice == "0":
            clear_screen()
            print_header()
            print("\n¡Gracias por utilizar CineMatch!")
            print("Hasta pronto.\n")
            break

        else:
            print(f"\n{Colors.RED}Opción inválida.{Colors.RESET}")
            pause()


if __name__ == "__main__":
    main()
