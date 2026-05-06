from datetime import date, timedelta
from pyecore.ecore import EDate
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
        for m in self.meetings.meetings:
            if m.id == meetingId:
                meeting = m
                break
        
        if not meeting:
            raise ValueError('Meeting does not exist.')
        
        # Find member
        member = None
        for m in self.meetings.members:
            if m.id == memberId:
                member = m
                break
        
        if not member:
            raise ValueError('Member does not exist.')
        
        # Check if member is an attendee
        attendee = None
        for a in self.meetings.meetingAttendees:
            if a.meeting == meeting and a.attendee == member:
                attendee = a
                break
        
        if not attendee:
            raise ValueError('Member is not an attendee of the meeting.')
        
        # Check if guest number exceeds limit
        if guestNumber > meeting.meetingLimit.guestsLimit:
            raise ValueError("The guestNumber exceeds the meeting's guestsLimit.")
        
        # Set guest number
        attendee.guestNumber = guestNumber


    def addMemberToMeeting(self, memberId: int, meetingId: int):
        # Find meeting
        meeting = None
        for m in self.meetings.meetings:
            if m.id == meetingId:
                meeting = m
                break
        
        if not meeting:
            raise ValueError('Meeting does not exist.')
        
        # Find member
        member = None
        for m in self.meetings.members:
            if m.id == memberId:
                member = m
                break
        
        if not member:
            raise ValueError('Member does not exist.')
        
        # Check if member is already part of the meeting (attendee, waitlist, or not-attendee)
        for a in self.meetings.meetingAttendees:
            if a.meeting == meeting and a.attendee == member:
                raise ValueError('Member is already part of the meeting.')
        
        for w in self.meetings.meetingWaitlistMembers:
            if w.meeting == meeting and w.member == member:
                raise ValueError('Member is already part of the meeting.')
        
        for na in self.meetings.meetingNotAttendees:
            if na.meeting == meeting and na.member == member:
                raise ValueError('Member is already part of the meeting.')
        
        # Count current attendees
        attendeeCount = sum(1 for a in self.meetings.meetingAttendees if a.meeting == meeting)
        
        # Get current date from system
        currentDate = EDate.from_string(date.today().strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        
        # Check if attendees limit is reached
        if attendeeCount >= meeting.meetingLimit.attendeesLimit:
            # Add to waitlist
            waitlist = MeetingWaitlistMember(
                meeting=meeting,
                member=member,
                decisionDate=currentDate
            )
            self.meetings.meetingWaitlistMembers.append(waitlist)
        else:
            # Add as attendee
            attendee = MeetingAttendee(
                meeting=meeting,
                attendee=member,
                guestNumber=0,
                role=MeetingAttendeeRole.Attendee,
                decisionDate=currentDate
            )
            self.meetings.meetingAttendees.append(attendee)


    def addMemberToMeetingGroup(self, memberId: int, meetingGroupId: int):
        # Find meeting group
        meetingGroup = None
        for mg in self.meetings.meetingGroups:
            if mg.id == meetingGroupId:
                meetingGroup = mg
                break
        
        if not meetingGroup:
            raise ValueError('Meeting group does not exist.')
        
        # Find member
        member = None
        for m in self.meetings.members:
            if m.id == memberId:
                member = m
                break
        
        if not member:
            raise ValueError('Member does not exist.')
        
        # Check if member is already part of the meeting group
        for mgMember in meetingGroup.members:
            if mgMember.member == member:
                raise ValueError('Member is already part of the meeting group.')
        
        # Get current date
        currentDate = EDate.from_string(date.today().strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        
        # Add member to meeting group
        mgMember = MeetingGroupMember()
        mgMember.meetingGroup = meetingGroup
        mgMember.member = member
        mgMember.joinedDate = currentDate
        mgMember.role = MeetingGroupMemberRole.Member
        mgMember.isActive = True
        meetingGroup.members.append(mgMember)


    def addSubscriptionPaymentToMember(self, memberId: int, value: float, currency: str, subscriptionPeriod: str):
        # Validate inputs
        if value <= 0:
            raise ValueError('The value must be positive.')
        
        if not currency:
            raise ValueError('The currency must not be empty.')
        
        if not subscriptionPeriod:
            raise ValueError('The subscriptionPeriod must not be empty.')
        
        # Find member
        member = None
        for m in self.meetings.members:
            if m.id == memberId:
                member = m
                break
        
        if not member:
            raise ValueError('Member does not exist.')
        
        # Check if member already has a subscription
        for s in self.payments.subscriptions:
            if s.subscriber == member:
                raise ValueError('Member already has a subscription.')
        
        # Create subscription payment
        periodEnum = getattr(SubscriptionPeriod, subscriptionPeriod)
        
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

        expirationDate = EDate.from_string(expirationDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        
        # Create subscription
        subscription = Subscription(
            subscriber=member,
            countryCode='ca',
            expirationDate=expirationDate,
            subscriptionPeriod=periodEnum,
            status=SubscriptionStatus.Active
        )
        self.payments.subscriptions.append(subscription)
        
        # Create subscription payment
        payment = SubscriptionPayment(
            countryCode='ca',
            subscriptionPeriod=periodEnum,
            status=SubscriptionPaymentStatus.WaitingForPayment,
            payer=member,
            value=MoneyValue(value=value, currency=currency)
        )
        self.payments.subscriptionPayments.append(payment)


    def addSubscriptionRenewalPaymentToMember(self, memberId: int, value: float, currency: str):
        # Validate inputs
        if value <= 0:
            raise ValueError('The value must be positive.')
        
        if not currency:
            raise ValueError('The currency must not be empty.')
        
        # Find member
        member = None
        for m in self.meetings.members:
            if m.id == memberId:
                member = m
                break
        
        if not member:
            raise ValueError('Member does not exist.')
        
        # Check if member has a subscription
        subscription = None
        for s in self.payments.subscriptions:
            if s.subscriber == member:
                subscription = s
                break
        
        if not subscription:
            raise ValueError('Member does not have a subscription.')
        
        # Check if subscription is active
        if subscription.status != SubscriptionStatus.Active:
            raise ValueError('Member does not have an active subscription.')
        
        # Create subscription renewal payment
        payment = SubscriptionRenewalPayment(
            countryCode=subscription.countryCode,
            subscriptionPeriod=subscription.subscriptionPeriod,
            status=SubscriptionRenewalPaymentStatus.WaitingForPayment,
            payer=member,
            value=MoneyValue(value=value, currency=currency)

        )
        self.payments.subscriptionRenewalPayments.append(payment)


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
        for m in self.meetings.members:
            if m.id == memberId:
                member = m
                break
        
        if not member:
            raise ValueError('Member does not exist.')
        
        # Create meeting location
        location = MeetingLocation()
        location.name = locationName
        location.address = locationAddress
        location.city = locationCity
        location.countryCode = locationCountryCode
        self.meetings.meetingLocations.append(location)
        
        # Create meeting term
        term = MeetingTerm(
            startDate=EDate.from_string(startDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z')),
            endDate=EDate.from_string(endDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        )
        
        # Create RSVP term
        rsvpTerm = Term(
            startDate=EDate.from_string(rsvpStartDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z')),
            endDate=EDate.from_string(rsvpEndDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        )
        
        # Create meeting limit
        limit = MeetingLimit()
        limit.attendeesLimit = attendeesLimit
        limit.guestsLimit = guestsLimit
        
        # Create meeting
        meeting = Meeting(
            id=self._get_next_meeting_id(),
            title=title,
            description=description,
            location=location,
            term=term,
            rsvpTerm=rsvpTerm,
            meetingLimit=limit,
            creator=member,
        )
        self.meetings.meetings.append(meeting)
        
        return meeting


    def _get_next_meeting_id(self):
        """Helper method to generate unique meeting ID"""
        if not self.meetings.meetings:
            return 1
        return max(m.id for m in self.meetings.meetings) + 1


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
        for m in self.meetings.members:
            if m.id == memberId:
                member = m
                break
        
        if not member:
            raise ValueError('Member does not exist.')
        
        # Check if member has an active subscription
        hasActiveSubscription = False
        for s in self.payments.subscriptions:
            if s.subscriber == member and s.status == SubscriptionStatus.Active:
                hasActiveSubscription = True
                break
        
        if not hasActiveSubscription:
            raise ValueError('Must have an active subscription to create a meeting group proposal.')
        
        # Count how many meeting groups the member is an organizer of
        organizerCount = 0
        for mg in self.meetings.meetingGroups:
            for mgMember in mg.members:
                if mgMember.member == member and mgMember.role == MeetingGroupMemberRole.Organizer:
                    organizerCount += 1
                    break
        
        # Count the member's pending proposals
        pendingCount = 0
        for p in self.meetings.meetingGroupProposals:
            if p.member == member and p.status == MeetingGroupProposalStatus.ToVerify:
                pendingCount += 1
        
        if organizerCount + pendingCount >= 3:
            raise ValueError('A maximum of 3 meeting groups can be covered by a subscription.')
        
        # Get current date
        currentDate = EDate.from_string(date.today().strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        
        # Create meeting group location
        location = MeetingGroupLocation(
            countryCode=countryCode,
            city=city,
        )
        
        # Create meeting group proposal
        proposal = MeetingGroupProposal(
            id=self._get_next_meeting_group_proposal_id(),
            name=name,
            description=description,
            meetingGroupLocation=location,
            member=member,
            status=MeetingGroupProposalStatus.ToVerify,
            proposalDate=currentDate
        )
        self.meetings.meetingGroupProposals.append(proposal)
        
        return proposal


    def _get_next_proposal_id(self):
        """Helper method to generate unique proposal ID"""
        maxId = 0
        for p in self.meetings.meetingGroupProposals:
            if p.id > maxId:
                maxId = p.id

        for p in self.meetings.meetingGroups:
            if p.id > maxId:
                maxId = p.id
        return maxId + 1


    def createMeetingGroupProposalDecision(self, adminId: int, proposalId: int, decisionCode: str, rejectReason: str):
        # Find proposal
        proposal = None
        for p in self.meetings.meetingGroupProposals:
            if p.id == proposalId:
                proposal = p
                break
        
        if not proposal:
            raise ValueError('Proposal does not exist.')
        
        # Get the member who created the proposal
        member = proposal.member
        
        # If accepting, check if member has an active subscription and does not already have 3 meeting groups
        if decisionCode == 'Accept':
            hasActiveSubscription = False
            for s in self.payments.subscriptions:
                if s.subscriber == member and s.status == SubscriptionStatus.Active:
                    hasActiveSubscription = True
                    break
            
            if not hasActiveSubscription:
                raise ValueError('Member does not have an active subscription')
            
            organizerCount = 0
            for mg in self.meetings.meetingGroups:
                for mgMember in mg.members:
                    if mgMember.member.id == member.id and mgMember.role == MeetingGroupMemberRole.Organizer:
                        organizerCount += 1
                        break
            
            if organizerCount >= 3:
                raise ValueError('A maximum of 3 meeting groups can be covered by a subscription.')
        
        # Get current date
        currentDate = date.today()
        currentDate = EDate.from_string(currentDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        
        # Create decision
        codeEnum = getattr(MeetingGroupProposalDecisionCode, decisionCode)
        admin = None

        for a in self.administration.administrators:
            if a.id == adminId:
                admin = a
                break

        decision = MeetingGroupProposalDecision(
            code=codeEnum,
            rejectReason=rejectReason,
            date=currentDate,
            administrator=admin
        )
        proposal.decisions.append(decision)
        
        # Update proposal status
        if decisionCode == 'Accept':
            proposal.status = MeetingGroupProposalStatus.Verified
            
            # Create meeting group
            meetingGroup = MeetingGroup(
                id=proposal.id,
                name=proposal.name,
                description=proposal.description,
                meetingGroupLocation=proposal.meetingGroupLocation,
                creator=member,
                createDate=currentDate
            )
            self.meetings.meetingGroups.append(meetingGroup)
            
            # Add member as organizer
            mgMember = MeetingGroupMember(
                meetingGroup=meetingGroup,
                member=member,
                joinedDate=currentDate,
                role=MeetingGroupMemberRole.Organizer,
                isActive=True
            )
            meetingGroup.members.append(mgMember)
        elif decisionCode == 'Reject':
            proposal.status = MeetingGroupProposalStatus.Rejected


    def _get_next_meeting_group_proposal_id(self):
        """Helper method to generate unique meeting group ID"""
        if not self.meetings.meetingGroupProposals:
            return 1
        return max(mg.id for mg in self.meetings.meetingGroupProposals) + 1


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
        currentDate = EDate.from_string(date.today().strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        
        # Create user registration
        userRegistration = UserRegistration(
            id=self._get_next_user_registration_id(),
            login=login,
            email=email,
            firstName=firstName,
            lastName=lastName,
            name=name,
            status=UserRegistrationStatus.WaitingForConfirmation,
            registerDate=currentDate,
            confirmedDate=None
        )
        self.userAccess.userRegistrations.append(userRegistration)
        
        return userRegistration


    def _get_next_user_registration_id(self):
        """Helper method to generate unique user registration ID"""
        maxId = 0
        for ur in self.userAccess.userRegistrations:
            if ur.id > maxId:
                maxId = ur.id
        for u in self.userAccess.users:
            if u.id > maxId:
                maxId = u.id
        return maxId + 1


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
        
        # Convert dates from strings
        
        if startDate > endDate:
            raise ValueError('The startDate must be before or equal to endDate.')
        
        if rsvpStartDate > rsvpEndDate:
            raise ValueError('The rsvpStartDate must be before or equal to rsvpEndDate.')
        
        if attendeesLimit <= 0:
            raise ValueError('The attendeesLimit must be greater than 0.')
        
        if guestsLimit <= 0:
            raise ValueError('The guestsLimit must be greater than 0.')
        
        # Find meeting
        meeting = None
        for m in self.meetings.meetings:
            if m.id == meetingId:
                meeting = m
                break
        
        if not meeting:
            raise ValueError('Meeting does not exist.')
        
        # Find member
        member = None
        for m in self.meetings.members:
            if m.id == memberId:
                member = m
                break
        
        if not member:
            raise ValueError('Member does not exist.')
        
        # Check if member is the creator of the meeting
        if meeting.creator != member:
            raise ValueError('Only the creator of the meeting can edit it.')
        
        # Update meeting
        meeting.title = title
        meeting.description = description
        
        # Update location
        location = meeting.location
        location.name = locationName
        location.address = locationAddress
        location.city = locationCity
        location.countryCode = locationCountryCode
        
        # Update term
        term = meeting.term
        term.startDate = EDate.from_string(startDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        term.endDate = EDate.from_string(endDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        
        # Update RSVP term
        rsvpTerm = meeting.rsvpTerm
        rsvpTerm.startDate = EDate.from_string(rsvpStartDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        rsvpTerm.endDate = EDate.from_string(rsvpEndDate.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
        
        # Update limit
        limit = meeting.meetingLimit
        limit.attendeesLimit = attendeesLimit
        limit.guestsLimit = guestsLimit


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
        userRegistration = None
        for ur in self.userAccess.userRegistrations:
            if ur.id == registrationId:
                userRegistration = ur
                break
        
        if not userRegistration:
            raise ValueError('User registration does not exist.')
        
        # Check if already confirmed or expired
        if userRegistration.status == UserRegistrationStatus.Confirmed:
            raise ValueError('Cannot update a confirmed user registration.')
        
        if userRegistration.status == UserRegistrationStatus.Expired:
            raise ValueError('Cannot update an expired user registration.')
        
        # Update user registration
        userRegistration.login = login
        userRegistration.email = email
        userRegistration.firstName = firstName
        userRegistration.lastName = lastName
        userRegistration.name = name
        
        # Handle status change
        statusEnum = getattr(UserRegistrationStatus, status)
        userRegistration.status = statusEnum
        
        # If confirmed, create user and set confirmed date
        if status == 'Confirmed':
            currentDate = EDate.from_string(date.today().strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
            userRegistration.confirmedDate = currentDate
            
            # Create user
            user = User()
            user.id = userRegistration.id
            user.login = login
            user.email = email
            user.firstName = firstName
            user.lastName = lastName
            user.name = name
            user.createDate = currentDate
            self.userAccess.users.append(user)
