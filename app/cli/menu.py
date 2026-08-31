from app.cli.company_menu import (
    add_company,
    list_companies,
    view_company,
    update_company,
    delete_company,
    search_companies,
)
from app.cli.application_menu import (
    add_application,
    list_applications,
    view_application,
    update_application,
    delete_application,
    search_applications,
    show_dashboard,
    filter_applications,
    export_applications,
    sort_applications,
    import_applications,
)
from app.cli.interview_menu import (
    add_interview,
    list_interviews,
    view_interview,
    update_interview,
    delete_interview,
    search_interviews,
    filter_interviews,
    sort_interviews,
    export_interviews,
)
from app.cli.follow_up_menu import (
    add_follow_up,
    list_follow_ups,
    view_follow_up,
    complete_follow_up,
    reopen_follow_up,
    delete_follow_up,
    upcoming_follow_ups,
    list_pending_follow_ups,
    list_completed_follow_ups,
)


def show_menu() -> None:
    print()
    print("=" * 40)
    print("          CAREERTRACK")
    print("=" * 40)
    print("1. Add company")
    print("2. List companies")
    print("3. View company")
    print("4. Update company")
    print("5. Delete company")
    print("6. Search companies")
    print("7. Add application")
    print("8. List applications")
    print("9. View application")
    print("10. Update application")
    print("11. Delete application")
    print("12. Search applications")
    print("13. Dashboard")
    print("14. Filter applications")
    print("15. Export applications to CSV")
    print("16. Sort applications")
    print("17. Import applications from CSV")
    print("18. Export interviews to CSV")
    print("19. Add interview")
    print("20. List interviews")
    print("21. View interview")
    print("22. Update interview")
    print("23. Delete interview")
    print("24. Search interviews")
    print("25. Filter interviews")
    print("26. Sort interviews")
    print("27. Add follow-up")
    print("28. List follow-ups")
    print("29. View follow-up")
    print("30. Complete follow-up")
    print("31. Reopen follow-up")
    print("32. Delete follow-up")
    print("33. Upcoming follow-ups")
    print("34. Pending follow-ups")
    print("35. Completed follow-ups")
    print("36. Exit")


def run() -> None:
    while True:
        show_menu()

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            add_company()

        elif choice == "2":
            list_companies()

        elif choice == "3":
            view_company()

        elif choice == "4":
            update_company()

        elif choice == "5":
            delete_company()

        elif choice == "6":
            search_companies()

        elif choice == "7":
            add_application()

        elif choice == "8":
            list_applications()

        elif choice == "9":
            view_application()

        elif choice == "10":
            update_application()

        elif choice == "11":
            delete_application()

        elif choice == "12":
            search_applications()

        elif choice == "13":
            show_dashboard()

        elif choice == "14":
            filter_applications()

        elif choice == "15":
            export_applications()

        elif choice == "16":
            sort_applications()

        elif choice == "17":
            import_applications()

        elif choice == "18":
            export_interviews()

        elif choice == "19":
            add_interview()

        elif choice == "20":
            list_interviews()

        elif choice == "21":
            view_interview()

        elif choice == "22":
            update_interview()

        elif choice == "23":
            delete_interview()

        elif choice == "24":
            search_interviews()

        elif choice == "25":
            filter_interviews()

        elif choice == "26":
            sort_interviews()

        elif choice == "27":
            add_follow_up()

        elif choice == "28":
            list_follow_ups()

        elif choice == "29":
            view_follow_up()

        elif choice == "30":
            complete_follow_up()

        elif choice == "31":
            reopen_follow_up()

        elif choice == "32":
            delete_follow_up()

        elif choice == "33":
            upcoming_follow_ups()

        elif choice == "34":
            list_pending_follow_ups()

        elif choice == "35":
            list_completed_follow_ups()

        elif choice == "36":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option. Please try again.")
