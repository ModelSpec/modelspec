from datetime import date, timedelta
from ..generated_model_layer import *


class MeetingGroupsController:
    def __init__(self):
        self.userAccess: UserAccess = None
        self.administration: Administration = None
        self.meetings: Meetings = None
        self.payments: Payments = None


    def addGuestToMeetingAttendee(self, memberId: int, meetingId: int, guestNumber: int):
        # Validate guest number
        if guestNumber < 0:
            raise ValueError('The guestNumber must be zero or positive.')
        
        # Find meeting
        meeting = None
        for m in self.meetings.getMeetings():
            if m.getId() == meetingId:
                meeting = m
                break
        
        if not meeting:
            raise ValueError('Meeting does not exist.')
        
        # Find member
        member = None
        for m in self.meetings.getMembers():
            if m.getId() == memberId:
                member = m
                break

        if not member:
            raise ValueError('Member does not exist.')

        # Check if member is an attendee
        attendee = None
        for a in self.meetings.getMeetingAttendees():
            if a.getMeeting() == meeting and a.getAttendee() == member:
                attendee = a
                break

        if not attendee:
            raise ValueError('Member is not an attendee of the meeting.')

        # Check if guest number exceeds limit
        if guestNumber > meeting.getMeetingLimit().getGuestsLimit():
            raise ValueError("The guestNumber exceeds the meeting's guestsLimit.")

        # Set guest number
        attendee.setGuestNumber(guestNumber)


    def addMemberToMeeting(self, memberId: int, meetingId: int):
        # Find meeting
        meeting: Meeting = None
        for m in self.meetings.getMeetings():
            if m.getId() == meetingId:
                meeting = m
                break

        if not meeting:
            raise ValueError('Meeting does not exist.')

        # Find member
        member: Member = None
        for m in self.meetings.getMembers():
            if m.getId() == memberId:
                member = m
                break

        if not member:
            raise ValueError('Member does not exist.')

        # Check if member is already part of the meeting (attendee, waitlist, or not-attendee)
        for a in self.meetings.getMeetingAttendees():
            if a.getMeeting() == meeting and a.getAttendee() == member:
                raise ValueError('Member is already part of the meeting.')

        for w in self.meetings.getMeetingWaitlistMembers():
            if w.getMeeting() == meeting and w.getMember() == member:
                raise ValueError('Member is already part of the meeting.')

        for na in self.meetings.getMeetingNotAttendees():
            if na.getMeeting() == meeting and na.getMember() == member:
                raise ValueError('Member is already part of the meeting.')

        # Count current attendees
        attendeeCount = sum(1 for a in self.meetings.getMeetingAttendees() if a.getMeeting() == meeting)

        # Get current date from system
        currentDate = date.today()

        # Check if attendees limit is reached
        if attendeeCount >= meeting.getMeetingLimit().getAttendeesLimit():
            # Add to waitlist.
            self.meetings.addMeetingWaitlistMember(currentDate, member, meeting)
        else:
            # Add as attendee
            self.meetings.addMeetingAttendee(0, currentDate, MeetingAttendee.MeetingAttendeeRole.Attendee, member, meeting)


    def addMemberToMeetingGroup(self, memberId: int, meetingGroupId: int):
        # Find meeting group
        meetingGroup: MeetingGroup = None
        for mg in self.meetings.getMeetingGroups():
            if mg.getId() == meetingGroupId:
                meetingGroup = mg
                break

        if not meetingGroup:
            raise ValueError('Meeting group does not exist.')

        # Find member
        member = None
        for m in self.meetings.getMembers():
            if m.getId() == memberId:
                member = m
                break

        if not member:
            raise ValueError('Member does not exist.')

        # Check if member is already part of the meeting group
        for mgMember in meetingGroup.getMembers():
            if mgMember.getMember() == member:
                raise ValueError('Member is already part of the meeting group.')

        # Get current date
        currentDate = date.today()

        # Add member to meeting group
        member = meetingGroup.addMember(MeetingGroupMember.MeetingGroupMemberRole.Member, member)
        member.setJoinedDate(currentDate)
        member.setIsActive(True)


    def addSubscriptionPaymentToMember(self, memberId: int, value: float, currency: str, subscriptionPeriod: str):
        # Validate inputs
        if value <= 0:
            raise ValueError('The value must be positive.')

        if not currency:
            raise ValueError('The currency must not be empty.')

        if not subscriptionPeriod:
            raise ValueError('The subscriptionPeriod must not be empty.')

        # Find member
        member: Member = None
        for m in self.meetings.getMembers():
            if m.getId() == memberId:
                member = m
                break

        if not member:
            raise ValueError('Member does not exist.')

        # Check if member already has a subscription
        for s in self.payments.getSubscriptions():
            if s.getSubscriber() == member:
                raise ValueError('Member already has a subscription.')

        # Create subscription payment
        periodEnum = getattr(Subscription.SubscriptionPeriod, subscriptionPeriod)

        # Calculate expiration date
        currentDate = date.today()
        if subscriptionPeriod == 'Month':
            # End of current month
            if currentDate.month == 12:
                expirationDate = date(currentDate.year, 12, 31)
            else:
                nextMonth = currentDate.replace(month=currentDate.month + 1, day=1)
                expirationDate = nextMonth - timedelta(days=1)
        elif subscriptionPeriod == 'HalfYear':
            # 6 months from now, end of that month
            monthsToAdd = 6
            year = currentDate.year + (currentDate.month + monthsToAdd - 1) // 12
            month = (currentDate.month + monthsToAdd - 1) % 12
            if month == 12:
                expirationDate = date(year, 12, 31)
            else:
                nextMonth = date(year, month + 1, 1)
                expirationDate = nextMonth - timedelta(days=1)

        # Create subscription
        subscription = self.payments.addSubscription('ca', expirationDate, periodEnum, Subscription.SubscriptionStatus.Active, member)

        # Create subscription payment
        mv = MoneyValue(value, currency)
        payment: SubscriptionPayment = self.payments.addSubscriptionPayment('ca', periodEnum, member, mv)
        payment.setStatus(SubscriptionPayment.SubscriptionPaymentStatus.WaitingForPayment)


    def addSubscriptionRenewalPaymentToMember(self, memberId: int, value: float, currency: str):
        # Validate inputs
        if value <= 0:
            raise ValueError('The value must be positive.')

        if not currency:
            raise ValueError('The currency must not be empty.')

        # Find member
        member: Member = None
        for m in self.meetings.getMembers():
            if m.getId() == memberId:
                member = m
                break

        if not member:
            raise ValueError('Member does not exist.')

        # Check if member has a subscription
        subscription = None
        for s in self.payments.getSubscriptions():
            if s.getSubscriber() == member:
                subscription = s
                break

        if not subscription:
            raise ValueError('Member does not have a subscription.')

        # Check if subscription is active
        if subscription.getStatus() != Subscription.SubscriptionStatus.Active:
            raise ValueError('Member does not have an active subscription.')

        # Create subscription renewal payment
        mv = MoneyValue(value, currency)
        payment = self.payments.addSubscriptionRenewalPayment(
            'ca',
            subscription.getSubscriptionPeriod(),
            member,
            mv
        )
        payment.setStatus(SubscriptionRenewalPayment.SubscriptionRenewalPaymentStatus.WaitingForPayment)


    def createMeeting(self, memberId: int, title: str, description: str,
                      locationName: str, locationAddress: str, locationCity: str,
                      locationCountryCode: str, startDate: date, endDate: date,
                      rsvpStartDate: date, rsvpEndDate: date, attendeesLimit: int, guestsLimit: int):
        # Validate inputs
        if not title:
            raise ValueError('The title must not be empty.')

        if not description:
            raise ValueError('The description must not be empty.')

        if not locationName:
            raise ValueError('The locationName must not be empty.')

        if not locationAddress:
            raise ValueError('The locationAddress must not be empty.')

        if not locationCity:
            raise ValueError('The locationCity must not be empty.')

        if not locationCountryCode:
            raise ValueError('The locationCountryCode must not be empty.')

        if len(locationCountryCode) < 2 or len(locationCountryCode) > 3:
            raise ValueError('The locationCountryCode must be either 2 or 3 characters long.')

        if not startDate:
            raise ValueError('The startDate must not be empty.')

        if not endDate:
            raise ValueError('The endDate must not be empty.')

        if not rsvpStartDate:
            raise ValueError('The rsvpStartDate must not be empty.')

        if not rsvpEndDate:
            raise ValueError('The rsvpEndDate must not be empty.')

        if startDate > endDate:
            raise ValueError('The startDate must be before or equal to endDate.')

        if rsvpStartDate > rsvpEndDate:
            raise ValueError('The rsvpStartDate must be before or equal to rsvpEndDate.')

        if attendeesLimit <= 0:
            raise ValueError('The attendeesLimit must be greater than 0.')

        if guestsLimit <= 0:
            raise ValueError('The guestsLimit must be greater than 0.')

        # Find member
        member = None
        for m in self.meetings.getMembers():
            if m.getId() == memberId:
                member = m
                break

        if not member:
            raise ValueError('Member does not exist.')

        # Create meeting location
        location = self.meetings.addMeetingLocation(locationName, locationAddress, locationCity, locationCountryCode)

        # Create meeting term
        term = MeetingTerm(startDate, endDate)

        # Create RSVP term
        rsvpTerm = Term(rsvpStartDate, rsvpEndDate)

        # Create meeting limit
        limit = MeetingLimit(attendeesLimit, guestsLimit)

        # Create meeting
        meeting = self.meetings.addMeeting(title, description, term, location, limit, rsvpTerm, member)

        return meeting


    def createMeetingGroupProposal(self, memberId: int, name: str, description: str, city: str, countryCode: str):
        # Validate inputs
        if not name:
            raise ValueError('The name must not be empty.')

        if not description:
            raise ValueError('The description must not be empty.')

        if not city:
            raise ValueError('The city must not be empty.')

        if not countryCode:
            raise ValueError('The country code must not be empty.')

        if len(countryCode) < 2 or len(countryCode) > 3:
            raise ValueError('The country code must be either 2 or 3 characters long.')

        # Find member
        member = None
        for m in self.meetings.getMembers():
            if m.getId() == memberId:
                member = m
                break

        if not member:
            raise ValueError('Member does not exist.')

        # Check if member has an active subscription
        hasActiveSubscription = False
        for s in self.payments.getSubscriptions():
            if s.getSubscriber() == member and s.getStatus() == Subscription.SubscriptionStatus.Active:
                hasActiveSubscription = True
                break

        if not hasActiveSubscription:
            raise ValueError('Must have an active subscription to create a meeting group proposal.')

        # Count how many meeting groups the member is an organizer of
        organizerCount = 0
        for mg in self.meetings.getMeetingGroups():
            for mgMember in mg.getMembers():
                if mgMember.getMember() == member and mgMember.getRole() == MeetingGroupMember.MeetingGroupMemberRole.Organizer:
                    organizerCount += 1
                    break

        # Count the member's pending proposals
        pendingCount = 0
        for p in self.meetings.getMeetingGroupProposals():
            if p.getMember() == member and p.getStatus() == MeetingGroupProposal.MeetingGroupProposalStatus.ToVerify:
                pendingCount += 1

        if organizerCount + pendingCount >= 3:
            raise ValueError('A maximum of 3 meeting groups can be covered by a subscription.')

        # Get current date
        currentDate = date.today()

        # Create meeting group location
        location = MeetingGroupLocation(city, countryCode)

        # Create meeting group proposal
        proposal = self.meetings.addMeetingGroupProposal(name, description, location, member)
        proposal.setProposalDate(currentDate)
        proposal.setStatus(MeetingGroupProposal.MeetingGroupProposalStatus.ToVerify)

        return proposal


    def createMeetingGroupProposalDecision(self, adminId: int, proposalId: int, decisionCode: str, rejectReason: str):
        # Find proposal
        proposal: MeetingGroupProposal = None
        for p in self.meetings.getMeetingGroupProposals():
            if p.getId() == proposalId:
                proposal = p
                break

        if not proposal:
            raise ValueError('Proposal does not exist.')

        # Get the member who created the proposal
        member = proposal.getMember()

        # If accepting, check if member has an active subscription and does not already have 3 meeting groups
        if decisionCode == 'Accept':
            hasActiveSubscription = False
            for s in self.payments.getSubscriptions():
                if s.getSubscriber() == member and s.getStatus() == Subscription.SubscriptionStatus.Active:
                    hasActiveSubscription = True
                    break

            if not hasActiveSubscription:
                raise ValueError('Member does not have an active subscription')

            organizerCount = 0
            for mg in self.meetings.getMeetingGroups():
                for mgMember in mg.getMembers():
                    if mgMember.getMember() == member and mgMember.getRole() == MeetingGroupMember.MeetingGroupMemberRole.Organizer:
                        organizerCount += 1
                        break

            if organizerCount >= 3:
                raise ValueError('A maximum of 3 meeting groups can be covered by a subscription.')

        # Get current date
        currentDate = date.today()

        # Create decision
        codeEnum = getattr(MeetingGroupProposalDecision.MeetingGroupProposalDecisionCode, decisionCode)
        admin = None
        for a in self.administration.getAdministrators():
            if a.getId() == adminId:
                admin = a
                break

        decision = proposal.addDecision(rejectReason, codeEnum, admin)
        decision.setDate(currentDate)

        # Update proposal status
        if decisionCode == 'Accept':
            proposal.setStatus(MeetingGroupProposal.MeetingGroupProposalStatus.Verified)

            # Create meeting group
            meetingGroup: MeetingGroup = self.meetings.addMeetingGroup(
                proposal.getId(),
                proposal.getName(),
                proposal.getDescription(),
                proposal.getMeetingGroupLocation(),
                member
            )

            meetingGroup.setCreateDate(currentDate)

            # Add member as organizer
            mgMember = meetingGroup.addMember(
                MeetingGroupMember.MeetingGroupMemberRole.Organizer,
                member,
            )

            mgMember.setJoinedDate(currentDate)
            mgMember.setIsActive(True)

        elif decisionCode == 'Reject':
            proposal.setStatus(MeetingGroupProposal.MeetingGroupProposalStatus.Rejected)


    def createUserRegistration(self, login: str, email: str, firstName: str, lastName: str, name: str):
        # Validate inputs
        if not login:
            raise ValueError('The login must not be empty.')

        if not email:
            raise ValueError('The email must not be empty.')

        # Validate email format
        if email.count('@') != 1:
            raise ValueError('The email must contain exactly one "@" character.')

        atIndex = email.index('@')
        if '.' not in email[atIndex:]:
            raise ValueError('The email must contain a "." character after the "@" character.')

        if email.endswith('.'):
            raise ValueError('The email must not end with a "." character.')

        if not firstName:
            raise ValueError('The firstName must not be empty.')

        if not lastName:
            raise ValueError('The lastName must not be empty.')

        if not name:
            raise ValueError('The name must not be empty.')

        # Get current date
        currentDate = date.today()

        # Create user registration
        userRegistration: UserRegistration = self.userAccess.addUserRegistration(login, email, firstName, lastName)
        userRegistration.setName(name)
        userRegistration.setStatus(UserRegistration.UserRegistrationStatus.WaitingForConfirmation)
        userRegistration.setRegisterDate(currentDate)

        return userRegistration


    def editMeeting(self, memberId: int, meetingId: int, title: str, description: str,
                    locationName: str, locationAddress: str, locationCity: str,
                    locationCountryCode: str, startDate: date, endDate: date,
                    rsvpStartDate: date, rsvpEndDate: date, attendeesLimit: int, guestsLimit: int):
        # Validate inputs
        if not title:
            raise ValueError('The title must not be empty.')

        if not description:
            raise ValueError('The description must not be empty.')

        if not locationName:
            raise ValueError('The locationName must not be empty.')

        if not locationAddress:
            raise ValueError('The locationAddress must not be empty.')

        if not locationCity:
            raise ValueError('The locationCity must not be empty.')

        if not locationCountryCode:
            raise ValueError('The locationCountryCode must not be empty.')

        if len(locationCountryCode) < 2 or len(locationCountryCode) > 3:
            raise ValueError('The locationCountryCode must be either 2 or 3 characters long.')

        if not startDate:
            raise ValueError('The startDate must not be empty.')

        if not endDate:
            raise ValueError('The endDate must not be empty.')

        if not rsvpStartDate:
            raise ValueError('The rsvpStartDate must not be empty.')

        if not rsvpEndDate:
            raise ValueError('The rsvpEndDate must not be empty.')

        if startDate > endDate:
            raise ValueError('The startDate must be before or equal to endDate.')

        if rsvpStartDate > rsvpEndDate:
            raise ValueError('The rsvpStartDate must be before or equal to rsvpEndDate.')

        if attendeesLimit <= 0:
            raise ValueError('The attendeesLimit must be greater than 0.')

        if guestsLimit <= 0:
            raise ValueError('The guestsLimit must be greater than 0.')

        # Find meeting
        meeting: Meeting = None
        for m in self.meetings.getMeetings():
            if m.getId() == meetingId:
                meeting = m
                break

        if not meeting:
            raise ValueError('Meeting does not exist.')

        # Find member
        member: Member = None
        for m in self.meetings.getMembers():
            if m.getId() == memberId:
                member = m
                break
        
        if not member:
            raise ValueError('Member does not exist.')
        
        # Check if member is the creator of the meeting
        if meeting.getCreator() != member:
            raise ValueError('Only the creator of the meeting can edit it.')
        
        # Update meeting
        meeting.setTitle(title)
        meeting.setDescription(description)
        
        # Update location
        location = meeting.getLocation()
        location.setName(locationName)
        location.setAddress(locationAddress)
        location.setCity(locationCity)
        location.setCountryCode(locationCountryCode)
        
        # Update term
        term = meeting.getTerm()
        term.setStartDate(startDate)
        term.setEndDate(endDate)
        
        # Update RSVP term
        rsvpTerm = meeting.getRsvpTerm()
        rsvpTerm.setStartDate(rsvpStartDate)
        rsvpTerm.setEndDate(rsvpEndDate)
        
        # Update limit
        limit = meeting.getMeetingLimit()
        limit.setAttendeesLimit(attendeesLimit)
        limit.setGuestsLimit(guestsLimit)


    def updateUserRegistration(self, registrationId: int, login: str, email: str, firstName: str,
                                 lastName: str, name: str, status: str):
        # Validate inputs
        if not login:
            raise ValueError('The login must not be empty.')
        
        if not email:
            raise ValueError('The email must not be empty.')
        
        # Validate email format
        if email.count('@') != 1:
            raise ValueError('The email must contain exactly one "@" character.')
        
        atIndex = email.index('@')
        if '.' not in email[atIndex:]:
            raise ValueError('The email must contain a "." character after the "@" character.')
        
        if email.endswith('.'):
            raise ValueError('The email must not end with a "." character.')
        
        if not firstName:
            raise ValueError('The firstName must not be empty.')
        
        if not lastName:
            raise ValueError('The lastName must not be empty.')
        
        if not name:
            raise ValueError('The name must not be empty.')
        
        # Find user registration
        userRegistration: UserRegistration = None
        for ur in self.userAccess.getUserRegistrations():
            if ur.getId() == registrationId:
                userRegistration = ur
                break
        
        if not userRegistration:
            raise ValueError('User registration does not exist.')
        
        # Check if already confirmed or expired
        if userRegistration.getStatus() == UserRegistration.UserRegistrationStatus.Confirmed:
            raise ValueError('Cannot update a confirmed user registration.')
        
        if userRegistration.getStatus() == UserRegistration.UserRegistrationStatus.Expired:
            raise ValueError('Cannot update an expired user registration.')
        
        # Update user registration
        userRegistration.setLogin(login)
        userRegistration.setEmail(email)
        userRegistration.setFirstName(firstName)
        userRegistration.setLastName(lastName)
        userRegistration.setName(name)
        
        # Handle status change
        statusEnum = getattr(UserRegistration.UserRegistrationStatus, status)
        userRegistration.setStatus(statusEnum)
        
        # If confirmed, create user and set confirmed date
        if status == 'Confirmed':
            currentDate = date.today()
            userRegistration.setConfirmedDate(currentDate)
            
            # Create user
            user = self.userAccess.addUser(registrationId, login, email, firstName, lastName, name)
            user.setCreateDate(currentDate)
