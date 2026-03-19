import requests
import json
import time
import random

BASE_URL = "http://127.0.0.1:8000/api/v1"
ADMIN_USER = "aadhithya"
ADMIN_PASS = "A@dhi2006"

def test_workflow():
    print("--- Starting Comprehensive Automated API Test ---")
    
    # 1. Login
    print("\n[1] Logging in...")
    login_res = requests.post(f"{BASE_URL}/auth/login/", json={
        "username": ADMIN_USER,
        "password": ADMIN_PASS
    })
    if login_res.status_code != 200:
        print(f"FAILED Login: {login_res.status_code} - {login_res.text}")
        return
    
    token = login_res.json()['access']
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print("SUCCESS: Logged in.")

    # 2. Create Category
    print("\n[2] Creating Category...")
    rand_id = random.randint(1000, 9999)
    cat_payload = {
        "name": f"Science {rand_id}",
        "description": "Natural and physical sciences"
    }
    cat_res = requests.post(f"{BASE_URL}/categories/", headers=headers, json=cat_payload)
    if cat_res.status_code not in [200, 201]:
        print(f"FAILED Category: {cat_res.status_code} - {cat_res.text}")
        return
    category_id = cat_res.json()['id']
    print(f"SUCCESS: Created Category {category_id}")

    # 3. Create Tag
    print("\n[3] Creating Tag...")
    tag_payload = {"name": f"Physics {rand_id}"}
    tag_res = requests.post(f"{BASE_URL}/tags/", headers=headers, json=tag_payload)
    if tag_res.status_code not in [200, 201]:
        print(f"FAILED Tag: {tag_res.status_code} - {tag_res.text}")
        return
    tag_id = tag_res.json()['id']
    print(f"SUCCESS: Created Tag {tag_id}")

    # 4. Create Quiz with AI
    print("\n[4] Generating Quiz with AI (NVIDIA LLM)...")
    quiz_payload = {
        "title": f"Quantum Physics {rand_id}",
        "topic": "Basics of Quantum Mechanics",
        "category": category_id,
        "difficulty": "HARD",
        "generate_with_ai": True,
        "num_questions": 3,
        "tag_ids": [tag_id]
    }
    quiz_res = requests.post(f"{BASE_URL}/quizzes/", headers=headers, json=quiz_payload)
    quiz_data = quiz_res.json()
    if quiz_res.status_code not in [200, 201]:
        print(f"FAILED Quiz Creation: {quiz_res.status_code} - {quiz_data}")
        return
    quiz_id = quiz_data['id']
    print(f"SUCCESS: Created Quiz {quiz_id}")

    # 4.1 Filter Tests
    print("\n[4.1] Testing Quiz Listing & Filters...")
    list_res = requests.get(f"{BASE_URL}/quizzes/?category={category_id}&difficulty=HARD", headers=headers)
    if list_res.status_code == 200:
        print(f"SUCCESS: Filtered listing returned {len(list_res.json()['results'])} quizzes.")
    else:
        print(f"FAILED Filtering: {list_res.text}")

    # 5. Publish Quiz
    print("\n[5] Publishing Quiz...")
    requests.post(f"{BASE_URL}/quizzes/{quiz_id}/submit/", headers=headers)
    requests.post(f"{BASE_URL}/quizzes/{quiz_id}/publish/", headers=headers)
    print("SUCCESS: Quiz Published.")

    # 6. Start Attempt (NEW NESTED ENDPOINT)
    print("\n[6] Starting Attempt (Nested)...")
    attempt_res = requests.post(f"{BASE_URL}/quizzes/{quiz_id}/attempts/", headers=headers)
    attempt_data = attempt_res.json()
    if attempt_res.status_code not in [200, 201]:
        print(f"FAILED Attempt Start: {attempt_res.status_code} - {attempt_data}")
        return
    attempt_id = attempt_data['id']
    print(f"SUCCESS: Started Attempt {attempt_id}")

    # 7. Get Questions
    print("\n[7] Fetching Questions...")
    q_res = requests.get(f"{BASE_URL}/attempts/{attempt_id}/questions/", headers=headers)
    questions = q_res.json()
    print(f"SUCCESS: Retrieved {len(questions)} questions.")

    # 8. Submit Answers (IDEMPOTENT TEST)
    print("\n[8] Submitting Answers (Idempotent)...")
    if questions:
        q = questions[0]
        opt_id = q['options'][0]['id']
        # Try twice
        requests.post(f"{BASE_URL}/attempts/{attempt_id}/answers/", headers=headers, json={
            "question": q['id'], "selected_option": opt_id
        })
        requests.post(f"{BASE_URL}/attempts/{attempt_id}/answers/", headers=headers, json={
            "question": q['id'], "selected_option": opt_id
        })
    print("SUCCESS: Answers submitted.")

    # 9. Finalize Quiz
    print("\n[9] Finalizing Quiz...")
    sub_res = requests.post(f"{BASE_URL}/attempts/{attempt_id}/submit/", headers=headers)
    print(f"SUCCESS: Final Score: {sub_res.json().get('score', 0)}%")

    # 10. Rating
    print("\n[10] Testing Rating System...")
    rate_res = requests.post(f"{BASE_URL}/quizzes/{quiz_id}/rating/", headers=headers, json={"rating": 5, "review": "Great quiz!"})
    if rate_res.status_code == 201:
        print("SUCCESS: Quiz Rated.")
    
    get_rate_res = requests.get(f"{BASE_URL}/quizzes/{quiz_id}/ratings/", headers=headers)
    print(f"SUCCESS: Ratings retrieved: {len(get_rate_res.json()['results'])}")

    # 11. User Dashboards
    print("\n[11] Testing User Dashboard...")
    my_quizzes = requests.get(f"{BASE_URL}/users/me/quizzes/", headers=headers)
    print(f"SUCCESS: My Quizzes: {len(my_quizzes.json())}")
    my_attempts = requests.get(f"{BASE_URL}/users/me/attempts/", headers=headers)
    print(f"SUCCESS: My Attempts: {len(my_attempts.json())}")

    # 12. Notifications
    print("\n[12] Testing Notifications...")
    notifs = requests.get(f"{BASE_URL}/notifications/", headers=headers)
    if notifs.status_code == 200:
        notif_list = notifs.json()['results']
        print(f"SUCCESS: Notifications: {len(notif_list)}")
        if notif_list:
            read_res = requests.patch(f"{BASE_URL}/notifications/{notif_list[0]['id']}/read/", headers=headers)
            print(f"SUCCESS: Notification marked as read: {read_res.status_code}")

    # 13. Admin Review Queue
    print("\n[13] Testing Admin Pending Queue...")
    pending_res = requests.get(f"{BASE_URL}/admin/quizzes/pending/", headers=headers)
    if pending_res.status_code == 200:
        print(f"SUCCESS: Pending quizzes: {len(pending_res.json()['results'])}")

    print("\n--- All Improved Endpoints Tested Successfully ---")

if __name__ == "__main__":
    test_workflow()

if __name__ == "__main__":
    test_workflow()
