import os
import django
import json
import random
from faker import Faker

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paw.settings")  # <-- change if your settings module name is different
django.setup()

from accounts.models import Account
from pet_adoption.models import Doctor

fake = Faker()

# Config
TOTAL_USERS = 100
TOTAL_DOCTORS = 50
PASSWORD = "Test@123"  # fixed password for all users

# Real Gurugram pincodes
GURUGRAM_PINCODES = [
    "122001", "122002", "122003", "122004", "122005", "122006", "122007", "122008",
    "122009", "122010", "122011", "122012", "122013", "122014", "122015", "122016",
]

SPECIALIZATIONS = [
    "Veterinary Surgeon", "Animal Nutritionist", "Pet Dentist", "Dermatologist",
    "Pet Cardiologist", "Veterinary Radiologist", "Animal Behaviourist",
    "General Practitioner", "Emergency Vet", "Pet Orthopedic Specialist",
]

QUALIFICATIONS = [
    "B.V.Sc & A.H", "M.V.Sc", "PhD in Veterinary Science", "DVM",
]

CLINIC_NAMES = [
    "Happy Paws Clinic", "Furry Friends Vet Care", "Pet Wellness Center",
    "Animal Aid Clinic", "Vet4Pets Gurugram", "Pawfect Care Hospital",
]

mock_data = {
    "accounts": [],
    "doctors": []
}

# --- STEP 1: Create Accounts ---
print("Creating mock accounts...")
for i in range(TOTAL_USERS):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
    username = email.split("@")[0]
    phone_number = fake.numerify("9#########")

    user, created = Account.objects.get_or_create(
        email=email,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "phone_number": phone_number,
        },
    )
    if created:
        user.set_password(PASSWORD)
        user.save()

    mock_data["accounts"].append({
        "id": user.id,
        "name": f"{first_name} {last_name}",
        "email": email,
        "phone": phone_number,
    })

# --- STEP 2: Create Doctor Records ---
print("Assigning 50 doctors randomly...")
all_users = list(Account.objects.all())
doctor_users = random.sample(all_users, TOTAL_DOCTORS)

for user in doctor_users:
    specialization = random.choice(SPECIALIZATIONS)
    qualification = random.choice(QUALIFICATIONS)
    clinic_name = random.choice(CLINIC_NAMES)
    experience = random.randint(1, 20)
    consultation_fee = round(random.uniform(300, 1200), 2)
    pincode = random.choice(GURUGRAM_PINCODES)

    doctor, created = Doctor.objects.get_or_create(
        account=user,
        defaults={
            "specialization": specialization,
            "qualification": qualification,
            "experience": experience,
            "clinic_name": clinic_name,
            "pincode": pincode,
            "consultation_fee": consultation_fee,
        },
    )

    mock_data["doctors"].append({
        "doctor_id": doctor.id,
        "user_id": user.id,
        "specialization": specialization,
        "qualification": qualification,
        "experience": experience,
        "clinic_name": clinic_name,
        "pincode": pincode,
        "consultation_fee": consultation_fee,
    })

# --- STEP 3: Save to JSON ---
json_path = os.path.join(os.getcwd(), "mock_doctors.json")
with open(json_path, "w") as f:
    json.dump(mock_data, f, indent=4)

print(f"✅ Done! Created {TOTAL_USERS} users and {TOTAL_DOCTORS} doctors.")
print(f"JSON data saved at: {json_path}")
