
import json
import urllib.parse
import urllib.request
import urllib.error

from cohort_database import save_cohort_concepts


# Public FHIR terminology server
BASE_URL = "https://r4.ontoserver.csiro.au/fhir"

# SNOMED CT implicit ValueSet
SNOMED_VALUESET = "http://snomed.info/sct?fhir_vs"


def expand_valueset(params):
    """Send a ValueSet expansion request to the FHIR server."""

    query = urllib.parse.urlencode(params)
    url = f"{BASE_URL}/ValueSet/$expand?{query}"

    request = urllib.request.Request(
        url,
        headers={"Accept": "application/fhir+json"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)

    if data.get("resourceType") == "OperationOutcome":
        raise ValueError(
            f"FHIR server error: {data.get('issue')}"
        )

    if "expansion" not in data:
        raise ValueError("No ValueSet expansion returned.")

    return data["expansion"]


def search_snomed(term):
    """Search SNOMED CT concepts by clinical term."""

    expansion = expand_valueset({
        "url": SNOMED_VALUESET,
        "filter": term,
        "count": 10
    })

    results = expansion.get("contains", [])

    print("\nMatching SNOMED CT concepts:\n")

    for index, concept in enumerate(results, start=1):
        name = concept.get("display", "Unknown")
        code = concept.get("code", "Unknown")

        inactive = (
            " [INACTIVE]"
            if concept.get("inactive")
            else ""
        )

        print(f"{index}. {name} ({code}){inactive}")

    return results


def get_descendants(concept_id):
    """
    Retrieve the selected concept and all its descendants
    using SNOMED CT ECL and pagination.
    """

    ecl = f"<<{concept_id}"

    page_size = 100
    offset = 0

    all_concepts = []
    seen_codes = set()

    print(f"\nRetrieving concepts using ECL: {ecl}")

    while True:
        expansion = expand_valueset({
            "url": f"{SNOMED_VALUESET}=ecl/{ecl}",
            "count": page_size,
            "offset": offset
        })

        concepts = expansion.get("contains", [])
        total = expansion.get("total")

        for concept in concepts:
            code = concept.get("code")

            if code and code not in seen_codes:
                all_concepts.append(concept)
                seen_codes.add(code)

        print(
            f"Retrieved {len(all_concepts)} unique concepts "
            f"(server total: {total})"
        )

        if not concepts:
            if total is not None and offset < total:
                raise RuntimeError(
                    "Server returned an empty page before "
                    "extraction completed."
                )
            break

        offset += len(concepts)

        if total is not None and offset >= total:
            break

        if total is None and len(concepts) < page_size:
            break

    if total is not None and len(all_concepts) != total:
        raise RuntimeError(
            f"Incomplete extraction: retrieved "
            f"{len(all_concepts)} unique concepts, "
            f"but server reported {total}."
        )

    print(
        f"\nExtraction completed: "
        f"{len(all_concepts)} concepts."
    )

    return all_concepts


def main():
    """Run the interactive clinical cohort explorer."""

    print("=== Clinical Cohort Explorer ===")

    term = input(
        "\nEnter a clinical condition: "
    ).strip()

    if not term:
        print("Please enter a clinical condition.")
        return

    # Step 1: Search SNOMED CT
    results = search_snomed(term)

    if not results:
        print("No matching concepts found.")
        return

    # Step 2: Researcher selects the intended concept
    choice = input(
        "\nSelect a concept number: "
    ).strip()

    if not choice.isdigit():
        print("Please enter a valid number.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(results):
        print("Selection is outside the available results.")
        return

    selected_concept = results[index]

    if selected_concept.get("inactive"):
        print(
            "This concept is inactive. "
            "Please select an active concept."
        )
        return

    # Step 3: Retrieve the selected concept ID dynamically
    concept_id = selected_concept["code"]
    concept_name = selected_concept["display"]

    print(f"\nSelected concept: {concept_name}")
    print(f"SNOMED CT ID: {concept_id}")

    # Step 4: Retrieve the complete concept set
    concepts = get_descendants(concept_id)

    # Step 5: Save the concept set into SQLite
    save_cohort_concepts(concept_id, concepts)

    print("\nClinical concept extraction completed!")


if __name__ == "__main__":
    try:
        main()

    except urllib.error.HTTPError as error:
        print(
            f"\nHTTP error: {error.code} "
            f"{error.reason}"
        )

    except urllib.error.URLError as error:
        print(f"\nConnection error: {error.reason}")

    except (ValueError, TimeoutError, RuntimeError) as error:
        print(f"\nError: {error}")

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
