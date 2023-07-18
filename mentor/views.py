from django.shortcuts import redirect, render, HttpResponse
from Tree import *
from Hashmap import *
from queue_meeting import *
from imports import all_meeting_requests, mentor_meeting_history, tree, queue, announcements_list
from datetime import date
import csv

def mentor_home(request):
    mentor = request.session.get('mentor')
    return render(request, 'mentorhome.html', {"mentor": mentor})

def csv_writer(file_name, word1, word2, word3):
    with open(f"{file_name}", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([word1, word2, word3])
    pass

def add_mentee(request):
    mentor = request.session.get("mentor")
    if request.method == "GET":
        return render(request, "add_mentee.html")
    if request.method == "POST":
        mentee_name = request.POST.get("mentee_name")
        mentee_department = request.POST.get("mentee_department")
        
        csv_writer("logindetails.csv", mentee_name, "0099", "mentee")

        tree.add_mentee(mentor, mentee_name, mentee_department)
        print(tree)
        return redirect("/mentor/mentor")


def show_mentor_details(request):
    if request.method == "GET":
        mentor = request.session.get('mentor')
        mentor_node = tree.find_node_by_name(mentor)
        mentor_node.skills = {"Programming Language":"Python"}
        mentor_node.education = {"Secondary Education": "HC school", "UG B.Tech" : "SSLV College"}
        mentor_node.achievements = {"Project management":"HSV certified"}
        print(mentor)
        print(mentor_node)
        print(mentor_node.name)
        print("MENTOR")

        return render(request, 'mentordetails.html',
                      {"mentor": mentor_node,
                       "skills": mentor_node.skills.items(),
                       "education": mentor_node.education.items(),
                       "achievements": mentor_node.achievements.items(),
                       "readonly_state": True})
    return HttpResponse("No mentor available")


def show_mentee_details(request):
    if request.method == "GET":
        mentee = request.session.get('mentee')
        mentee_node = tree.find_node_by_name(mentee)
        mentee_node.skills = {"Programming Language":"Python"}
        mentee_node.education = {"Secondary Education": "Holy Cross school"}
        mentee_node.achievements = {"Spelling Bee":"Top 3 in ISB"}

        print(mentee)
        print(mentee_node)
        print(mentee_node.name)
        print("mentee")

        return render(request, 'menteedetails.html',
                      {"mentee": mentee_node,
                       "skills": mentee_node.skills.items(),
                       "education": mentee_node.education.items(),
                       "achievements": mentee_node.achievements.items(),
                       "readonly_state": True})
    return HttpResponse("No mentee available")


def update_mentee_details(request):
    if request.method == "GET":
        mentee = request.GET.get('name')
        mentee_node = tree.find_node_by_name(mentee)
        mentee_node.skills = {"Programming Language":"Python"}
        mentee_node.education = {"Secondary Education": "Holy Cross school"}
        mentee_node.achievements = {"Spelling Bee":"Top 3 in ISB"}
        print(mentee)
        print("mentee")

        return render(request, 'menteedetails.html',
                      {"mentee": mentee_node,
                       "skills": mentee_node.skills.items(),
                       "education": mentee_node.education.items(),
                       "achievements": mentee_node.achievements.items(),
                       "readonly_state": False})
    elif request.method == "POST":
        print("POSTTTTTT")

        # Name, photo, dept, exp, description
        name = request.POST.get('name')
        profile_picture = request.POST.get('profile_picture')
        department = request.POST.get('department')
        description = request.POST.get('description')

        # Skills
        dep_skill = request.POST.getlist('department[]')
        part_skill = request.POST.getlist("skill[]")
        skills = dict(zip(dep_skill, part_skill))
        print(skills)
        # Education
        part_education = request.POST.getlist('education[]')
        institution = request.POST.getlist("institution[]")
        education = dict(zip(institution, part_education))
        print(education)
        # Achievements
        part_achievement = request.POST.getlist('achievements[]')
        year = request.POST.getlist("year[]")
        achievements = dict(zip(year, part_achievement))
        print(achievements)
        # availability & contact info
        contact_info = request.POST.get('contact-info')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        nationality = request.POST.get('Nationality')
        religion = request.POST.get('religion')
        community = request.POST.get('Community')
        remarks = request.POST.get('remarks')
        mentee = tree.find_node_by_name(name)

        fields = {
            "name": name,
            "department": department,
            "profile_picture": profile_picture,
            "skills": skills,
            "description": description,
            "contact_info": contact_info,
            "education": education,
            "achievements": achievements,
            "dob": dob,
            "gender": gender,
            "nationality": nationality,
            "religion": religion,
            "community": community,
            "remarks": remarks
        }

        for field_name, field_value in fields.items():
            update_method = getattr(mentee, f"update_{field_name}", None)
            if update_method is not None:
                update_method(field_value)
            else:
                setattr(mentee, field_name, field_value)
            print(getattr(mentee, field_name))
        print(mentee)

        return redirect("mentor_home")


# def update_mentor_details(request):
#     if request.method == "GET":
#         mentor = request.session.get('mentor')
#         mentor_node = tree.find_node_by_name(mentor)
#         mentor_node.skills = {"Programming Language":"Python"}
#         mentor_node.education = {"Secondary Education": "HC school", "UG B.Tech" : "SSLV College"}
#         mentor_node.achievements = {"Project management":"HSV certified"}
#         print("MENTOR")

#         return render(request, 'mentordetails.html',
#                       {"mentor": mentor_node,
#                        "skills": mentor_node.skills.items(),
#                        "education": mentor_node.education.items(),
#                        "achievements": mentor_node.achievements.items(),
#                        "readonly_state": False})
#     elif request.method == "POST":
#         print("POSTTTTTT")
#         # Name, photo, dept, exp, description
#         name = request.POST.get('name')
#         profile_picture = request.POST.get('profile_picture')
#         department = request.POST.get('department')
#         experience = request.POST.get('experience')
#         description = request.POST.get('description')

#         # Skills
#         dep_skill = request.POST.getlist('department[]')
#         part_skill = request.POST.getlist("skill[]")
#         skills = dict(zip(dep_skill, part_skill))
#         print(skills)
#         # Education
#         part_education = request.POST.getlist('education[]')
#         institution = request.POST.getlist("institution[]")
#         education = dict(zip(institution, part_education))
#         print(education)
#         # Achievements
#         part_achievement = request.POST.getlist('achievements[]')
#         year = request.POST.getlist("year[]")
#         achievements = dict(zip(year, part_achievement))
#         print(achievements)
#         # availability & contact info
#         availability = request.POST.get('availability')
#         contact_info = request.POST.get('contact-info')

#         # Update mentor details
#         # mentor = MentorNode(name, department, profile_picture, experience, skills, description, availability,
#         #                     # contact_info, education, achievements)

#         for fields in [name, department, profile_picture, experience, skills, description, availability,
#                        contact_info, education, achievements]:
#             mentor_node.update_profile_image(f"{fields}")

#         return HttpResponse("Mentor details updated successfully!")

def update_mentor_details(request):
    if request.method == "GET":
        mentor = request.session.get('mentor')
        mentor_node = tree.find_node_by_name(mentor)
        mentor_node.skills = {"Programming Language": "Python"}
        mentor_node.education = {"Secondary Education": "HC school", "UG B.Tech": "SSLV College"}
        mentor_node.achievements = {"Project management": "HSV certified"}
        print("MENTOR")

        return render(request, 'mentordetails.html',
                      {"mentor": mentor_node,
                       "skills": mentor_node.skills.items(),
                       "education": mentor_node.education.items(),
                       "achievements": mentor_node.achievements.items(),
                       "readonly_state": False})
    elif request.method == "POST":
        print("POSTTTTTT")
        # Name, photo, dept, exp, description
        name = request.POST.get('name')
        profile_picture = request.POST.get('profile_picture')
        department = request.POST.get('department')
        experience = request.POST.get('experience')
        description = request.POST.get('description')

        # Skills
        dep_skill = request.POST.getlist('department[]')
        part_skill = request.POST.getlist("skill[]")
        skills = dict(zip(dep_skill, part_skill))
        print(skills)
        # Education
        part_education = request.POST.getlist('education[]')
        institution = request.POST.getlist("institution[]")
        education = dict(zip(institution, part_education))
        print(education)
        # Achievements
        part_achievement = request.POST.getlist('achievements[]')
        year = request.POST.getlist("year[]")
        achievements = dict(zip(year, part_achievement))
        print(achievements)
        # Availability & contact info
        availability = request.POST.get('availability')
        contact_info = request.POST.get('contact-info')

        mentor = tree.find_node_by_name(name)

        fields = {
            "name": name,
            "department": department,
            "profile_picture": profile_picture,
            "experience": experience,
            "description": description,
            "skills": skills,
            "education": education,
            "achievements": achievements,
            "availability": availability,
            "contact_info": contact_info
        }

        for field_name, field_value in fields.items():
            update_method = getattr(mentor, f"update_{field_name}", None)
            if update_method is not None:
                update_method(field_value)
            else:
                setattr(mentor, field_name, field_value)
            print(getattr(mentor, field_name))
        print(mentor)

        return redirect("mentor_home")


def search_mentee(request):
    mentor = request.session.get("mentor")
    if request.method == "GET":
        return render(request, "search_mentee.html")
    if request.method == "POST":
        mentee_name = request.POST.get("mentee_name")
        request.session["mentee"] = mentee_name
        print(mentee_name)
        mentee = request.session.get("mentee")
        print(tree.get_mentees(mentor))
        if mentee in tree.get_mentees(mentor):
            mentee_node = tree.find_node_by_name(mentee)
            print(mentee)
            print(mentee_node.name)
            return render(request, "display_mentee.html", {"mentee": mentee_node})
    return render(request, "display_mentee.html")


# def add_meeting(request):
#     mentor = request.session.get('mentor')
#     meetings = mentor_meeting_history.get_meeting_records(mentor)
#     mentor = tree.find_node_by_name(mentor)
#     if request.method == "POST":
#         date = request.POST.get('date')
#         link = request.POST.get('link')
#         details = request.POST.get('details')
#         participants = request.POST.get('participants')

#         meeting = Meeting(date=date, link=link,
#                           details=details, participants=participants)
#         meetings.append(meeting)
#         mentor_meeting_history.add_meeting_record(mentor, meeting)
#         print(participants)
#         return render(request, 'meeting_history.html', {'meetings': meetings, 'mentor': mentor, 'mentor_meeting_history': mentor_meeting_history})

#     return render(request, 'meeting_history.html', {'meetings': meetings, 'mentor': mentor, 'mentor_meeting_history': mentor_meeting_history})

def add_meeting(request):
    mentor = request.session.get('mentor')
    meetings = mentor_meeting_history.get_meeting_records(mentor)
    mentor_name = mentor
    mentor = tree.find_node_by_name(mentor)

    if request.method == "POST":
        date = request.POST.get('date')
        link = request.POST.get('link')
        details = request.POST.get('details')
        # Use getlist() to retrieve multiple selected values
        participants = request.POST.getlist('participants')

        meeting = Meeting(date=date, link=link,
                          details=details, participants=participants)
        meetings.append(meeting)
        mentor_meeting_history.add_meeting_record(mentor_name, meeting)
        
        return render(request, 'meeting_history.html', {'meetings': meetings, 'mentor': mentor, 'mentor_meeting_history': mentor_meeting_history})

    return render(request, 'meeting_history.html', {'meetings': meetings, 'mentor': mentor, 'mentor_meeting_history': mentor_meeting_history})


def list_of_mentees(request):
    mentor = request.session.get('mentor')
    print(mentor)
    mentor_node = tree.find_node_by_name(mentor)
    mentor_children = mentor_node.children
    
    return render(request, "list_of_all_mentees.html", {"mentor": mentor, "mentees": mentor_children})


# def search_meeting(request):
#     meeting_date = request.POST.get("meeting-search")
#     mentor = request.session.get("mentor")
#     meeting_info = mentor_meeting_history.get_meeting_records(mentor)
#     meeting_searched = None
#     if request.method == "GET":
#         for meeting in meeting_info:
#             if meeting_date == meeting.date:
#                 print(meeting_date)
#                 print(meeting.date)
#                 request.session["meeting_searched"] = meeting
#         return render(request, "meeting_search_edit.html", {"meeting": meeting})
#     if request.method == "POST":
#         meeting = request.session.get("meeting_searched")
#         meeting.date = request.POST.get("date")
#         meeting.link = request.POST.get("link")
#         meeting.details = request.POST.get("details")
#         meeting.participants = request.POST.get("participants")

# def search_meeting(request):
#     mentor_name = request.session.get("mentor")
#     meeting_info = mentor_meeting_history.get_meeting_records(mentor_name)
#     meeting_searched = None

#     if request.method == "POST":
#         meeting_date = request.POST.get("meeting-search")

#         for meeting in meeting_info:
#             if meeting_date == meeting.date:
#                 meeting_searched = meeting
#                 break

#     if request.method == "GET" or not meeting_searched:
#         return render(request, "meeting_search_edit.html")

#     if request.method == "POST":
#         meeting_searched.date = request.POST.get("date")
#         meeting_searched.link = request.POST.get("link")
#         meeting_searched.details = request.POST.get("details")
#         meeting_searched.participants = request.POST.get("participants")
#         print("participantssssss:", meeting_searched.participants)
#         return redirect('search_meeting')

#     return render(request, "meeting_search_edit.html", {"meeting": meeting_searched})

def search_meeting(request):
    mentor_name = request.session.get("mentor")
    meeting_info = mentor_meeting_history.get_meeting_records(mentor_name)
    meeting_searched = None

    if request.method == "POST":
        meeting_date = request.POST.get("meeting-search")
        print ("POST")
        for meeting in meeting_info:
            print (meeting)
            print (meeting_date)
            print (".",meeting.date)
            if meeting_date == meeting.date:
                print ("dasdasd", meeting_date)
                print (".",meeting.date)

                meeting_searched = meeting
                break

    if request.method == "GET" or not meeting_searched:
        print ("GETETEt")
        return render(request, "meeting_search_edit.html")

    if request.method == "POST" and meeting_searched:
        meeting_searched.date = request.POST.get("date")
        meeting_searched.link = request.POST.get("link")
        meeting_searched.details = request.POST.get("details")
        meeting_searched.participants = request.POST.get("participants")
        print("participantssssss:", meeting_searched.participants)
        return render(request, "meeting_search_edit.html", {"meeting": meeting_searched})
    print ("dasdasda")
    return render(request, "meeting_search_edit.html", {"meeting": meeting_searched})

def mentor_meeting_request(request):
    """
    View for the mentor home page.
    """
    mentor = request.session.get("mentor")
    mentor_meeting_requests_queue = all_meeting_requests.get_meeting_request_queue(
        mentor)
    print(mentor_meeting_requests_queue)
    meeting_requests = mentor_meeting_requests_queue.list()
    print(meeting_requests)
    return render(request, 'request_meeting.html', {'meeting_requests': meeting_requests})

def delete_mentee(request):
    
    print (request.method)
    if request.method == "GET":
        return render(request, "deletementee.html")
    if request.method == "POST":
        mentee = request.POST.get("name")
        mentor = request.session.get("mentor")
        tree.remove_mentee(mentor, mentee)
        return render(request, "mentorhome.html")
    
def announcement_mentor(request):
    if request.method == 'POST':
        announcement = request.POST.get('announcement')
        announcements_list.append(announcement)
        request.session["today_date"] = date.today().isoformat()
        print(announcements_list)
        return redirect('announcement_mentor')  # Redirect back to the mentor announcement page

    return render(request, 'announcement_mentor.html')
