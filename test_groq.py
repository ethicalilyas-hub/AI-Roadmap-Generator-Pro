from core.groq_client import test_groq_connection

try:
    print("Connecting to Groq...")

    result = test_groq_connection()

    print("\nSUCCESS!")
    print(result)

except Exception as error:
    print("\nCONNECTION FAILED!")
    print(error)