from queue_meeting import MeetingRequest, MeetingRequestQueue


class HashMap:
    def __init__(self):
        self.hash_map = {}

    def put(self, key, value):
        self.hash_map[key] = value

    def get(self, key):
        return self.hash_map.get(key)

    def contains_key(self, key):
        return key in self.hash_map

    def remove(self, key):
        if key in self.hash_map:
            del self.hash_map[key]

    def keys(self):
        return self.hash_map.keys()

    def values(self):
        return self.hash_map.values()

    def items(self):
        return self.hash_map.items()


class Meeting:
    def __init__(self, date, link, details, participants):
        self.date = date
        self.link = link
        self.details = details
        self.participants = participants


class MentorMeetingHistory:
    def __init__(self):
        self.meeting_history = HashMap()

    def add_meeting_record(self, mentor_name, meeting_record):
        if self.meeting_history.contains_key(mentor_name):
            self.meeting_history.get(mentor_name).append(meeting_record)
        else:
            self.meeting_history.put(mentor_name, [meeting_record])

    def get_meeting_records(self, mentor_name):
        if self.meeting_history.contains_key(mentor_name):
            return self.meeting_history.get(mentor_name)
        else:
            return []


class AllMeetingRequests:
    def __init__(self):
        self.meeting_requests = HashMap()

    def add_meeting_request(self, mentor_name, meeting_request):
        if self.meeting_requests.contains_key(mentor_name):
            queue = self.meeting_requests.get(mentor_name)
            queue.enqueue(meeting_request)
        else:
            queue = MeetingRequestQueue()
            queue.enqueue(meeting_request)
            self.meeting_requests.put(mentor_name, queue)

    def get_meeting_request_queue(self, mentor_name):
        if self.meeting_requests.contains_key(mentor_name):
            return self.meeting_requests.get(mentor_name)
        else:
            return None

    def remove_meeting_request_queue(self, mentor_name):
        if self.meeting_requests.contains_key(mentor_name):
            self.meeting_requests.remove(mentor_name)

class AllAnnouncements:
    def __init__(self):
        self.announcement = HashMap()

    def add_announcement(self, mentor_name, announcement):
        if self.announcement.contains_key(mentor_name):
            announcement_list = self.announcement.get(mentor_name)
            announcement_list.append(announcement)
        else:
            announcement_list = []
            announcement_list.append(announcement)
            self.announcement.put(mentor_name, announcement_list)

    def get_announcement(self, mentor_name):
        if self.announcement.contains_key(mentor_name):
            return self.announcement.get(mentor_name)
        else:
            return None

    def remove_announcement(self, mentor_name):
        if self.announcement.contains_key(mentor_name):
            self.announcement.remove(mentor_name)
























# Example usage:
def Hashmap_status():
    all_meeting_requests = AllMeetingRequests()

    # Add meeting requests for mentors
    all_meeting_requests.add_meeting_request(
        "Heisenberg", MeetingRequest("Chinrasu", "2023-06-01", "Meeting request 1"))
    all_meeting_requests.add_meeting_request(
        "Heisenberg", MeetingRequest("Chelladurai", "2023-06-10", "Meeting request 2"))
    all_meeting_requests.add_meeting_request(
        "Gopal", MeetingRequest("Ambi", "2023-06-05", "Meeting request 3"))
    all_meeting_requests.add_meeting_request(
        "Gopal", MeetingRequest("Remo", "2023-06-15", "Meeting request 4"))

    # Get meeting request queues for mentors
    heisenberg_queue = all_meeting_requests.get_meeting_request_queue("Heisenberg")
    Gopal_queue = all_meeting_requests.get_meeting_request_queue("Gopal")
    # Example usage:
    mentor_meeting_history = MentorMeetingHistory()

    # Add meeting records for mentors
    mentor_meeting_history.add_meeting_record("Heisenberg", Meeting(
        "2023-06-01", "https://example.com/meeting1", "Meeting 1 details", ["Chinrasu"]))
    mentor_meeting_history.add_meeting_record("Heisenberg", Meeting(
        "2023-06-10", "https://example.com/meeting2", "Meeting 2 details", ["Chinrasu", "Chelladurai"]))
    mentor_meeting_history.add_meeting_record("Gopal", Meeting(
        "2023-06-05", "https://example.com/meeting3", "Meeting 3 details", ["Ambi", "Remo"]))
    mentor_meeting_history.add_meeting_record("Gopal", Meeting(
        "2023-06-15", "https://example.com/meeting4", "Meeting 4 details", ["Ambi"]))

    # Retrieve meeting records for a mentor
    Heisenberg_meetings = mentor_meeting_history.get_meeting_records("Heisenberg")
    Gopal_meetings = mentor_meeting_history.get_meeting_records("Gopal")

    # Print meeting records for John Doe
    print("Meeting records for John Doe:")
    for meeting in Heisenberg_meetings:
        print("Date:", meeting.date)
        print("Link:", meeting.link)
        print("Details:", meeting.details)
        print("Participants:", meeting.participants)
        print()

    # Print meeting records for Gopal
    print("Meeting records for Gopal:")
    for meeting in Gopal_meetings:
        print("Date:", meeting.date)
        print("Link:", meeting.link)
        print("Details:", meeting.details)
        print("Participants:", meeting.participants)
        print()
    return all_meeting_requests, mentor_meeting_history 