import requests
import time

BASE_URL = "https://codeforces.com/api"

def get_user_info(handle):
    try:
        response = requests.get(f"{BASE_URL}/user.info?handles={handle}")
        data = response.json()
        if data['status'] == 'OK':
            return data['result'][0]
    except Exception as e:
        print(f"Error fetching user info: {e}")
    return None

def get_problem_info(contest_id, index):
    try:
        # We can't fetch a single problem directly, so we fetch all problems and filter
        # Or we just trust the user input and verify existence via problemset
        # For efficiency, let's just use problemset.problems with a tag or just assume valid for now
        # Better: use problemset.problems and cache? No, too big.
        # Let's try to fetch contest problems.
        response = requests.get(f"{BASE_URL}/contest.standings?contestId={contest_id}&from=1&count=1")
        data = response.json()
        if data['status'] == 'OK':
            problems = data['result']['problems']
            for p in problems:
                if p['index'] == index:
                    return p
    except Exception as e:
        print(f"Error fetching problem info: {e}")
    return None

def check_submission(handle, contest_id, index):
    try:
        response = requests.get(f"{BASE_URL}/user.status?handle={handle}&from=1&count=10")
        data = response.json()
        if data['status'] == 'OK':
            submissions = data['result']
            for sub in submissions:
                if sub.get('contestId') == int(contest_id) and sub['problem']['index'] == index:
                    if sub['verdict'] == 'OK':
                        return True, sub
    except Exception as e:
        print(f"Error checking submission: {e}")
    return False, None

def get_contest_standings(contest_id):
    # This is heavy, we might want to limit or cache
    try:
        response = requests.get(f"{BASE_URL}/contest.standings?contestId={contest_id}")
        data = response.json()
        if data['status'] == 'OK':
            return data['result']
    except Exception as e:
        print(f"Error fetching standings: {e}")
    return None

def get_contest_rating_changes(contest_id):
    """Fetches rating changes for a contest to get old ratings of participants."""
    url = f"https://codeforces.com/api/contest.ratingChanges?contestId={contest_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'OK':
            # Create a map of handle -> oldRating
            return {row['handle']: row['oldRating'] for row in data['result']}
        return {}
    except Exception as e:
        print(f"Error fetching rating changes: {e}")
        return {}

def get_solvers_for_problem(contest_id, problem_index):
    """
    Fetches comprehensive contest data:
    - Solvers of the target problem with their net times
    - ALL participants who solved at least one problem
    Enriches with rating data from rating changes.
    
    Returns: {
        'solvers': [{'handle', 'net_time', 'rating', 'solve_time'}],
        'all_participants': [{'handle', 'rating', 'problems_solved'}]
    }
    """
    # 1. Fetch rating changes to get ratings of all participants
    rating_map = get_contest_rating_changes(contest_id)
    
    # 2. Fetch standings (pagination to get ALL rows)
    solvers = []
    all_participants = []
    
    from_index = 1
    count = 5000
    
    while True:
        url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}&from={from_index}&count={count}&showUnofficial=false"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != 'OK':
                break
                
            rows = data['result']['rows']
            if not rows:
                break
                
            problems_meta = data['result']['problems'] # Problems meta is same for all pages
            
            # Process rows immediately to avoid storing huge raw data
            # Find target problem index (only need to do this once, but doing it here is fine)
            target_idx = -1
            for i, p in enumerate(problems_meta):
                if p['index'] == problem_index:
                    target_idx = i
                    break
            
            for row in rows:
                handle = row['party']['members'][0]['handle']
                problem_results = row['problemResults']
                rating = rating_map.get(handle)
                
                # Count how many problems this participant solved
                problems_solved = sum(1 for res in problem_results if res['points'] > 0)
                
                # Only include participants who solved at least 1 problem
                if problems_solved > 0 and rating is not None:
                    all_participants.append({
                        'handle': handle,
                        'rating': rating,
                        'problems_solved': problems_solved
                    })
                
                # Check if they solved the target problem
                if target_idx >= 0 and target_idx < len(problem_results):
                    target_result = problem_results[target_idx]
                    
                    if target_result['points'] > 0:
                        solve_time = target_result['bestSubmissionTimeSeconds']
                        
                        # Calculate Net Time
                        all_solve_times = []
                        for res in problem_results:
                            if res['points'] > 0:
                                all_solve_times.append(res['bestSubmissionTimeSeconds'])
                        
                        all_solve_times.sort()
                        
                        previous_solve_time = 0
                        try:
                            idx_in_sorted = all_solve_times.index(solve_time)
                            if idx_in_sorted > 0:
                                previous_solve_time = all_solve_times[idx_in_sorted - 1]
                        except ValueError:
                            pass
                        
                        net_time = solve_time - previous_solve_time
                        
                        if rating is not None:
                            solvers.append({
                                'handle': handle,
                                'net_time': net_time,
                                'solve_time': solve_time,
                                'rating': rating
                            })
            
            from_index += count
            time.sleep(0.2) # Be nice to API
            
        except Exception as e:
            print(f"Error fetching standings page starting at {from_index}: {e}")
            break
            
    return {
        'solvers': solvers,
        'all_participants': all_participants
    }

