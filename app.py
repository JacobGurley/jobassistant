import database_operations as db_ops
import datetime

def main_menu():
    while True:
        print("\nJob Application Assistant")
        print("1. Add New Job Application")
        print("2. Update Application Status")
        print("3. View Applications")
        print("4. Check Follow-Ups")
        print("5. Delete a Job Application")
        print("6. Add New Company")
        print("7. Delete a Company")
        print("8. Add New Contact")
        print("9. Delete a Contact")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_new_application()
        elif choice == '2':
            update_application_status()
        elif choice == '3':
            view_applications()
        elif choice == '4':
            check_follow_ups()
        elif choice == '5':
            delete_job_application()
        elif choice == '6':
            add_new_company()
        elif choice == '7':
            delete_company()
        elif choice == '8':
            add_new_contact()
        elif choice == '9':
            delete_contact()
        elif choice =='10':
            break
        else:
            print("Invalid choice. Please try again.")

# Implement the functions called in the main menu
def confirm_action(prompt):
    confirmation = input(prompt + " Are you sure? (yes/no): ").lower()
    return confirmation == 'yes'


def validate_date(date_text):
    try:
        # Assuming the desired format is YYYY-MM-DD
        return datetime.datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError:
        print("Incorrect date format. Should be YYYY-MM-DD.")
        return None

def validate_response_received(response_text):
    if response_text.lower() in ['true', 'false']:
        return response_text.lower() == 'true'
    print("Invalid input. Enter True or False.")
    return None

def validate_numeric_input(input_text, input_type="number"):
    if input_text.isdigit():
        return int(input_text)
    print(f"Invalid input. The {input_type} should be a number.")
    return None

def validate_status(status_text):
    valid_statuses = ["applied", "interviewing", "offered", "rejected"]  # Add more as needed
    if status_text.lower() in valid_statuses:
        return status_text.capitalize()  # Capitalize for consistency
    print("Invalid status. Valid statuses are: " + ", ".join(valid_statuses).capitalize() + ".")
    return None

def mark_follow_up_complete(application_id):
    print(f"\nAddressing follow-up for Application ID: {application_id}")
    action = input("Enter 'reschedule' to set a new follow-up date, or 'complete' to mark this follow-up as addressed: ").lower()

    if action == 'reschedule':
        new_follow_up_date = None
        while new_follow_up_date is None:
            new_follow_up_input = input("Enter a new follow-up date (YYYY-MM-DD): ")
            new_follow_up_date = validate_date(new_follow_up_input)
            if new_follow_up_date:
                try:
                    db_ops.update_follow_up_date(application_id, new_follow_up_date)  # Assumes you have this function in your database_operations.py
                    print("Follow-up date updated.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                    new_follow_up_date = None  # Reset to allow re-entry

    elif action == 'complete':
        print("Marking follow-up as complete. (Consider implementing logic to update the application status or remove the follow-up date in the database.)")
    else:
        print("Invalid action. No changes made.")


def add_new_application():
    print("\n--- Add New Job Application ---")
    while True:
        company_id = None
        while company_id is None:
            company_input = input("Enter Company ID: ")
            company_id = validate_numeric_input(company_input, "Company ID")

        position = input("Enter Position: ")

        date_applied = None
        while date_applied is None:
            date_input = input("Enter Date Applied (YYYY-MM-DD): ")
            date_applied = validate_date(date_input)

        status = None
        while status is None:
            status_input = input("Enter Status (e.g., Applied, Interviewing): ")
            status = validate_status(status_input)

        follow_up_date = None
        while follow_up_date is None:
            follow_up_input = input("Enter Follow-Up Date (YYYY-MM-DD): ")
            follow_up_date = validate_date(follow_up_input)

        response_received = None
        while response_received is None:
            response_input = input("Response Received? Enter True or False: ")
            response_received = validate_response_received(response_input)

        notes = input("Enter any additional notes: ")

        if confirm_action("You're about to add a new job application"):
            try:
                db_ops.insert_job_application(company_id, position, date_applied, status, follow_up_date,
                                              response_received, notes)
                print("Job application added successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Action canceled.")

        if input("\nAdd another application? (yes/no): ").lower() != 'yes':
            break


def update_application_status():
    print("\n--- Update Application Status ---")

    while True:
        application_id = None
        while application_id is None:
            application_input = input("Enter the Application ID to update: ")
            application_id = validate_numeric_input(application_input, "Application ID")

        new_status = None
        while new_status is None:
            status_input = input("Enter the new status: ")
            new_status = validate_status(status_input)

        if confirm_action("You're about to update the application status"):
            try:
                db_ops.update_application_status(application_id, new_status)
                print("Application status updated successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Action canceled.")

        if input("\nUpdate another status? (yes/no): ").lower() != 'yes':
            break



def view_applications():
    print("\n--- View All Job Applications ---")
    try:
        applications = db_ops.get_all_job_applications()
        for app in applications:
            print(f"ID: {app[0]}, CompanyID: {app[1]}, Position: {app[2]}, Date Applied: {app[3]}, Status: {app[4]}, Follow-Up Date: {app[5]}, Response Received: {app[6]}, Notes: {app[7]}")
    except Exception as e:
        print(f"An error occurred: {e}")


def check_follow_ups():
    print("\n--- Check for Follow-Ups ---")
    try:
        due_follow_ups = db_ops.check_follow_ups()  # Fetch follow-ups due today or earlier
        for app in due_follow_ups:
            print(f"Follow up on application {app[0]} for position {app[1]} at company ID {app[2]}.")
            if confirm_action("Would you like to address this follow-up now?"):
                mark_follow_up_complete(app[0])  # Pass the Application ID to the function
    except Exception as e:
        print(f"An error occurred: {e}")


def delete_job_application():
    print("\n--- Delete a Job Application ---")

    while True:
        application_id = None
        while application_id is None:
            application_input = input("Enter the Application ID to delete: ")
            application_id = validate_numeric_input(application_input, "Application ID")

        if check_record_exists(application_id, 'JobApplications'):
            if confirm_action(f"You're about to delete the application with ID {application_id}"):
                try:
                    db_ops.delete_job_application(application_id)
                    print("Job application deleted successfully.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print("Action canceled.")
        else:
            print("No record found with the given Application ID.")

        if input("\nDelete another application? (yes/no): ").lower() != 'yes':
            break


def add_new_company():
    print("\n--- Add New Company ---")
    # ... Get company details from the user ...
    if confirm_action("You're about to add a new company"):
        try:
            db_ops.insert_company(company_name, industry, location, website, notes)
            print("Company added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Action canceled.")
    # ... Loop for continuous input ...

def delete_company():
    print("\n--- Delete a Company ---")
    # ... Get company ID from the user ...
    if confirm_action(f"You're about to delete the company with ID {company_id}"):
        try:
            db_ops.delete_company(company_id)
            print("Company deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Action canceled.")
    # ... Loop for continuous input ...

def add_new_contact():
    print("\n--- Add New Contact ---")
    # ... Get contact details from the user ...
    if confirm_action("You're about to add a new contact"):
        try:
            db_ops.insert_contact(company_id, name, position, email, phone, notes)
            print("Contact added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Action canceled.")
    # ... Loop for continuous input ...

def delete_contact():
    print("\n--- Delete a Contact ---")
    # ... Get contact ID from the user ...
    if confirm_action(f"You're about to delete the contact with ID {contact_id}"):
        try:
            db_ops.delete_contact(contact_id)
            print("Contact deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Action canceled.")
    # ... Loop for continuous input ...


if __name__ == "__main__":
    main_menu()