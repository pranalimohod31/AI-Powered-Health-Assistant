import joblib

model = joblib.load("models/health_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
symptoms = joblib.load("models/symptoms.pkl")

print("Model loaded successfully!")
print("Number of symptoms:", len(symptoms))
print("First few symptoms:", symptoms[:10])
print("Number of diseases:", len(label_encoder.classes_))
print("Diseases:", label_encoder.classes_)

print("\nEverything is working!")