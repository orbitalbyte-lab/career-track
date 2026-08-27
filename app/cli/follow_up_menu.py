from datetime import datetime

from app.database.connection import SessionLocal
from app.models.follow_up import FollowUp
from app.services.follow_up_service import FollowUpService


def add_follow_up() -> None:
    print("\n--- Add Follow-Up ---")

    try:
        application_id = int(
            input("Application ID: ").strip()
        )
    except ValueError:
        print("Application ID must be a number.")
        return

    date_text = input(
        "Follow-up date and time "
        "(YYYY-MM-DD HH:MM): "
    ).strip()

    try:
        follow_up_at = datetime.strptime(
            date_text,
            "%Y-%m-%d %H:%M",
        )
    except ValueError:
        print(
            "Invalid date format. "
            "Use YYYY-MM-DD HH:MM."
        )
        return

    note = input(
        "Follow-up note: "
    ).strip()

    try:
        follow_up = FollowUp(
            application_id=application_id,
            follow_up_at=follow_up_at,
            note=note,
        )
    except ValueError as error:
        print(f"Error: {error}")
        return

    with SessionLocal() as session:
        service = FollowUpService(session)

        result = service.create_follow_up(
            follow_up
        )

        print(
            "\nFollow-up created successfully!"
        )
        print(f"Follow-Up ID: {result.id}")


def list_follow_ups() -> None:
    print("\n--- Follow-Ups ---")

    with SessionLocal() as session:
        service = FollowUpService(session)

        follow_ups = service.get_follow_ups()

        if not follow_ups:
            print("No follow-ups found.")
            return

        for follow_up in follow_ups:
            status = (
                "Completed"
                if follow_up.completed
                else "Pending"
            )

            print(
                f"[{follow_up.id}] "
                f"Application ID: "
                f"{follow_up.application_id} | "
                f"Date: {follow_up.follow_up_at} | "
                f"Status: {status} | "
                f"Note: {follow_up.note}"
            )


def view_follow_up() -> None:
    print("\n--- View Follow-Up ---")

    try:
        follow_up_id = int(
            input("Follow-Up ID: ").strip()
        )
    except ValueError:
        print("Follow-Up ID must be a number.")
        return

    with SessionLocal() as session:
        service = FollowUpService(session)

        follow_up = service.get_follow_up(
            follow_up_id
        )

        if follow_up is None:
            print("Follow-up not found.")
            return

        status = (
            "Completed"
            if follow_up.completed
            else "Pending"
        )

        print("\nFollow-Up Details")
        print("-" * 30)
        print(f"ID:             {follow_up.id}")
        print(
            f"Application ID: "
            f"{follow_up.application_id}"
        )
        print(
            f"Date:           "
            f"{follow_up.follow_up_at}"
        )
        print(f"Status:         {status}")
        print(f"Note:           {follow_up.note}")
        print("-" * 30)


def complete_follow_up() -> None:
    print("\n--- Complete Follow-Up ---")

    try:
        follow_up_id = int(
            input("Follow-Up ID: ").strip()
        )
    except ValueError:
        print("Follow-Up ID must be a number.")
        return

    with SessionLocal() as session:
        service = FollowUpService(session)

        result = service.complete_follow_up(
            follow_up_id
        )

        if result is None:
            print("Follow-up not found.")
            return

        print(
            "Follow-up marked as completed."
        )


def reopen_follow_up() -> None:
    print("\n--- Reopen Follow-Up ---")

    try:
        follow_up_id = int(
            input("Follow-Up ID: ").strip()
        )
    except ValueError:
        print("Follow-Up ID must be a number.")
        return

    with SessionLocal() as session:
        service = FollowUpService(session)

        result = service.reopen_follow_up(
            follow_up_id
        )

        if result is None:
            print("Follow-up not found.")
            return

        print(
            "Follow-up marked as pending."
        )


def delete_follow_up() -> None:
    print("\n--- Delete Follow-Up ---")

    try:
        follow_up_id = int(
            input("Follow-Up ID: ").strip()
        )
    except ValueError:
        print("Follow-Up ID must be a number.")
        return

    with SessionLocal() as session:
        service = FollowUpService(session)

        result = service.delete_follow_up(
            follow_up_id
        )

        if not result:
            print("Follow-up not found.")
            return

        print(
            "Follow-up deleted successfully."
        )


def upcoming_follow_ups() -> None:
    print("\n--- Upcoming Follow-Ups ---")

    with SessionLocal() as session:
        service = FollowUpService(session)

        follow_ups = service.get_upcoming_follow_ups()

        if not follow_ups:
            print("No upcoming follow-ups.")
            return

        for follow_up in follow_ups:
            print(
                f"[{follow_up.id}] "
                f"Application ID: "
                f"{follow_up.application_id} | "
                f"Date: {follow_up.follow_up_at} | "
                f"Note: {follow_up.note}"
            )


def list_pending_follow_ups() -> None:
    print("\n--- Pending Follow-Ups ---")

    with SessionLocal() as session:
        service = FollowUpService(session)

        follow_ups = service.get_pending_follow_ups()

        if not follow_ups:
            print("No pending follow-ups.")
            return

        for follow_up in follow_ups:
            print(
                f"[{follow_up.id}] "
                f"Application ID: "
                f"{follow_up.application_id} | "
                f"Date: {follow_up.follow_up_at} | "
                f"Note: {follow_up.note}"
            )


def list_completed_follow_ups() -> None:
    print("\n--- Completed Follow-Ups ---")

    with SessionLocal() as session:
        service = FollowUpService(session)

        follow_ups = (
            service.get_completed_follow_ups()
        )

        if not follow_ups:
            print("No completed follow-ups.")
            return

        for follow_up in follow_ups:
            print(
                f"[{follow_up.id}] "
                f"Application ID: "
                f"{follow_up.application_id} | "
                f"Date: {follow_up.follow_up_at} | "
                f"Note: {follow_up.note}"
            )
