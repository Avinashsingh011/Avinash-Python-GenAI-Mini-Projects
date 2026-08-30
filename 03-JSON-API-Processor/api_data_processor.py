import json
import csv
import urllib.request
import urllib.error
from datetime import datetime


API_URL = "https://jsonplaceholder.typicode.com/users"


def fetch_api_data(url):
    print(f"\nConnecting to API:\n{url}")

    try:
        with urllib.request.urlopen(url, timeout=10) as response:

            if response.status != 200:
                print(f"API returned HTTP status: {response.status}")
                return []

            data = response.read().decode("utf-8")
            return json.loads(data)

    except urllib.error.HTTPError as error:
        print(f"HTTP Error: {error.code}")

    except urllib.error.URLError as error:
        print(f"Connection Error: {error.reason}")

    except json.JSONDecodeError:
        print("ERROR: Invalid JSON received from API.")

    except Exception as error:
        print(f"Unexpected Error: {error}")

    return []


def display_users(users):
    print("\n" + "=" * 75)
    print("                PYTHON JSON / API DATA PROCESSOR")
    print("=" * 75)

    print(f"\nTotal Records Received: {len(users)}")

    print("\n--- USER DATA ---")

    for user in users:

        print(f"""
ID       : {user.get('id')}
Name     : {user.get('name')}
Username : {user.get('username')}
Email    : {user.get('email')}
Company  : {user.get('company', {}).get('name')}
City     : {user.get('address', {}).get('city')}
Phone    : {user.get('phone')}
Website  : {user.get('website')}
{"-" * 50}
""")


def filter_users(users):
    search_city = input(
        "\nEnter city to filter or press Enter to skip: "
    ).strip()

    if not search_city:
        return users

    filtered_users = []

    for user in users:

        city = user.get("address", {}).get("city", "")

        if search_city.lower() in city.lower():
            filtered_users.append(user)

    return filtered_users


def export_to_json(users):

    output_file = "processed_users.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

    print(f"JSON report created: {output_file}")


def export_to_csv(users):

    output_file = "processed_users.csv"

    fieldnames = [
        "id",
        "name",
        "username",
        "email",
        "company",
        "city",
        "phone",
        "website"
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for user in users:

            writer.writerow({
                "id": user.get("id"),
                "name": user.get("name"),
                "username": user.get("username"),
                "email": user.get("email"),
                "company": user.get(
                    "company", {}
                ).get("name"),
                "city": user.get(
                    "address", {}
                ).get("city"),
                "phone": user.get("phone"),
                "website": user.get("website")
            })

    print(f"CSV report created: {output_file}")


def create_summary(users):

    summary = {
        "generated_at": str(datetime.now()),
        "total_records": len(users),
        "unique_cities": list(
            {
                user.get("address", {}).get("city")
                for user in users
            }
        ),
        "companies": [
            user.get("company", {}).get("name")
            for user in users
        ]
    }

    with open(
        "api_summary.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(summary, file, indent=4)

    print("Summary report created: api_summary.json")


def main():

    print("=" * 75)
    print("          PYTHON JSON / REST API DATA PROCESSOR")
    print("=" * 75)

    users = fetch_api_data(API_URL)

    if not users:
        print("\nNo data received from API.")
        return

    display_users(users)

    filtered_users = filter_users(users)

    print(
        f"\nRecords selected for export: "
        f"{len(filtered_users)}"
    )

    if not filtered_users:
        print("No matching records found.")
        return

    export_to_json(filtered_users)

    export_to_csv(filtered_users)

    create_summary(filtered_users)

    print("\n" + "=" * 75)
    print("PROCESSING COMPLETED SUCCESSFULLY")
    print("=" * 75)


if __name__ == "__main__":
    main()