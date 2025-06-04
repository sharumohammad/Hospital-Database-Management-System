import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sharu@248",   # ← Replace with your password
        database="hospital_db"
    )

def list_patients(cursor):
    cursor.execute("SELECT * FROM Patients")
    rows = cursor.fetchall()
    print("\n--- Patient List ---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Gender: {row[3]}, Contact: {row[4]}, Address: {row[5]}")

def list_doctors(cursor):
    cursor.execute("SELECT * FROM Doctors")
    rows = cursor.fetchall()
    print("\n--- Doctor List ---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Specialization: {row[2]}, Contact: {row[3]}")

def list_appointments(cursor):
    query = """
        SELECT a.AppointmentID, p.Name, d.Name, a.AppointmentDate, a.AppointmentTime, a.Reason
        FROM Appointments a
        JOIN Patients p ON a.PatientID = p.PatientID
        JOIN Doctors d ON a.DoctorID = d.DoctorID
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    print("\n--- Appointments ---")
    for row in rows:
        print(f"ID: {row[0]}, Patient: {row[1]}, Doctor: {row[2]}, Date: {row[3]}, Time: {row[4]}, Reason: {row[5]}")

def filter_doctors_by_specialization(cursor):
    specialization = input("Enter specialization to filter: ")
    cursor.execute("SELECT * FROM Doctors WHERE Specialization = %s", (specialization,))
    rows = cursor.fetchall()
    print(f"\n--- Doctors Specialized in {specialization} ---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Contact: {row[3]}")

def add_new_patient(cursor, conn):
    name = input("Enter patient name: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")
    contact = input("Enter contact number: ")
    address = input("Enter address: ")
    cursor.execute("INSERT INTO Patients (Name, Age, Gender, ContactNumber, Address) VALUES (%s, %s, %s, %s, %s)",
                   (name, age, gender, contact, address))
    conn.commit()
    print("New patient added.")

def add_new_appointment(cursor, conn):
    patient_id = int(input("Enter patient ID: "))
    doctor_id = int(input("Enter doctor ID: "))
    date = input("Enter appointment date (YYYY-MM-DD): ")
    time = input("Enter appointment time (HH:MM:SS): ")
    reason = input("Enter reason: ")
    cursor.execute("INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate, AppointmentTime, Reason) VALUES (%s, %s, %s, %s, %s)",
                   (patient_id, doctor_id, date, time, reason))
    conn.commit()
    print("Appointment added.")

def main():
    conn = connect_db()
    cursor = conn.cursor()

    while True:
        print("\n----- Hospital Management Menu -----")
        print("1. List all patients")
        print("2. List all doctors")
        print("3. List all appointments")
        print("4. Filter doctors by specialization")
        print("5. Add new patient")
        print("6. Add new appointment")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            list_patients(cursor)
        elif choice == '2':
            list_doctors(cursor)
        elif choice == '3':
            list_appointments(cursor)
        elif choice == '4':
            filter_doctors_by_specialization(cursor)
        elif choice == '5':
            add_new_patient(cursor, conn)
        elif choice == '6':
            add_new_appointment(cursor, conn)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
